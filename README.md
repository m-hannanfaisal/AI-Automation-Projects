# AI Automation Portfolio — Hannan Faisal

> **n8n · Groq · OpenAI · Python · RAG **
>
> A collection of production-ready AI automation workflows and systems built to solve real business problems — from lead generation to invoice processing to autonomous hiring pipelines. Each project is importable, documented, and freelance-deployable.

---

## About This Repository

This repository documents my journey learning AI automation — from a first conditional workflow to multi-agent pipelines with LLM scoring, real-time API integrations, and RAG-powered chatbots. Every project here solves a real business problem that a paying client would care about.

**What you will find:**
- Importable n8n workflow JSON files ready to deploy
- Real architecture diagrams from working systems
- Documented setup guides for each integration
- Projects ranging from beginner logic to production-grade multi-flow pipelines

**Stack I work with:** n8n · Groq (LLaMA 3.3) · OpenAI (GPT-4o) · Google Gemini · Python · FastAPI · ChromaDB · Apify · HubSpot · Meta Cloud API · LinkedIn API · Google Workspace APIs · Twilio

---

## Project Index

| # | Project | Complexity | Stack | Business Use Case |
|---|---|---|---|---|
| 1 | [AI Cold Outreach System](#1-ai-cold-outreach-system) | ⭐⭐⭐⭐ | n8n · Gemini · Gmail · Sheets | Automated personalized sales emails |
| 2 | [Hiring Signal Lead Engine](#2-hiring-signal-lead-engine) | ⭐⭐⭐⭐⭐ | n8n · Apify · OpenAI · Sheets | Job posting intelligence → sales leads |
| 3 | [CV Screening Engine](#3-cv-screening-engine) | ⭐⭐⭐⭐⭐ | n8n · OpenAI · GitHub API · Sheets | Resume + GitHub scoring for HR teams |
| 4 | [WhatsApp AI Booking Bot](#4-whatsapp-ai-booking-bot) | ⭐⭐⭐⭐ | n8n · Groq · Meta API · Google Calendar | 24/7 appointment booking via WhatsApp |
| 5 | [AI Invoice Processor](#5-ai-invoice-processor) | ⭐⭐⭐ | n8n · Groq · Gmail · Sheets | PDF invoice extraction → structured data |
| 6 | [Lead Capture & CRM Pipeline](#6-lead-capture--crm-pipeline) | ⭐⭐⭐ | n8n · Groq · HubSpot · Slack | Inbound leads → scored → routed instantly |
| 7 | [Daily AI Social Media Pipeline](#7-daily-ai-social-media-pipeline) | ⭐⭐⭐ | n8n · Groq · LinkedIn · WordPress | Daily auto-published finance content |
| 8 | [Basic RAG Chatbot](#8-basic-rag-chatbot) | ⭐⭐⭐ | Python · FastAPI · ChromaDB · Gemini | Document-aware AI customer support |
| 9 | [Elsa Energy RAG Chatbot](#9-elsa-energy-rag-chatbot) | ⭐⭐⭐⭐ | Python · FastAPI · Gemini · SQLite · Vanilla JS | Production RAG chatbot built for a real client |
| 10 | [AI Code Summarizer](#10-ai-code-summarizer) | ⭐⭐ | n8n · OpenAI · Gmail | Email-triggered code commenting & summary bot |
| 11 | [Feedback Discount Decision](#11-feedback-discount-decision) | ⭐ | n8n · IF Node · Sheets | First automation — conditional logic |

---

## Projects

---

### 1. AI Cold Outreach System

📁 [`AI-Cold-Outreach-System/`](./AI-Cold-Outreach-System)

**The problem:** Sales teams spend hours writing personalized cold emails one by one. Generic templates get ignored. The gap between personalization and scale is where deals are lost.

**What it does:** Pulls `Pending` leads from a Google Sheet, sends each one to Gemini AI which writes a fully personalized subject line and email body based on that lead's company, role, and industry — then sends via Gmail, updates the sheet status, waits between sends to respect rate limits, and loops to the next lead. A separate webhook flow listens for replies and automatically updates the lead status to `Replied`.

```
Google Sheets (Pending leads)
        ↓
Validate lead data (email + name present?)
        ↓ yes                    ↓ no
AI Personalization          Flag as Invalid - Skipped
(Gemini writes email)              ↓
        ↓               Update sheet → stop
Send via Gmail
        ↓
Update sheet → Sent + timestamp
        ↓
Wait 30s (rate limit safe)
        ↓
Loop to next lead
        ↓ (separate webhook flow)
Reply received → Update sheet → Replied
        ↓ (error handler)
Any failure → Instant alert email
```

**Key engineering decisions:**
- Processes one lead at a time with a 30s delay — prevents Gmail rate limit bans
- Self-healing JSON parser handles AI responses even when wrapped in markdown code fences
- Two-way sheet sync: `Pending → Sent → Replied` or `Invalid - Skipped` — nothing falls silent
- Built-in error alerting: any node failure sends an email with the failing node name and execution ID

**Tech stack:** n8n · Google Gemini (gemini-1.5-flash) · Gmail API · Google Sheets API · JavaScript

**Who buys this:** Sales agencies, SaaS companies, freelancers doing B2B outreach

---

### 2. Hiring Signal Lead Engine

📁 [`Hiring-Signal-Lead-Engine/`](./Hiring-Signal-Lead-Engine)

**The problem:** Companies that are actively hiring signal a budget and a business need. Sales teams that can identify those signals before competitors do win the deal. But manually scanning job boards every day doesn't scale.

**What it does:** Every morning, scrapes fresh job postings via Apify, normalizes every record into a consistent schema, deduplicates against a full history of previously seen listings, sends surviving records to an LLM for structured scoring against a configurable buying-signal rubric (0–5 score + one-sentence reasoning), separates qualified leads from noise, and emails a ranked HTML digest with direct links — all without a human touching it.

```
Daily Schedule Trigger (Scrape Flow)
        ↓
Apify — scrape job postings
        ↓
Standardize fields → filter out recruiters
        ↓
Zero results? → Alert email → stop
        ↓
Read existing leads (Sheets) → deduplicate
        ↓
Append new raw leads to Sheets
        ↓
AI Score each lead (0–5 + reasoning)
        ↓
Score ≥ 3? → Append to Qualified Leads sheet

Daily Schedule Trigger (Digest Flow — independent)
        ↓
Read today's qualified leads
        ↓
Build HTML digest table
        ↓
Send to sales inbox via Gmail
```

**Key engineering decisions:**
- Two independent schedules — the digest never depends on the scrape finishing successfully; decoupling makes the system resilient to slow scrapes
- Deduplication against full history prevents the same company being scored (and billed) twice
- Zero-results alerting — instead of going silently stale when a source changes structure, an alert fires immediately
- Transparent scoring — every lead has a visible reasoning string so a human can sanity-check the AI's judgment

**Tech stack:** n8n · Apify · OpenAI (gpt-4o-mini) · Google Sheets · Gmail

**Who buys this:** B2B sales teams, recruitment agencies, market intelligence teams

---

### 3. CV Screening Engine

📁 [`Cv_screening_engine/`](./Cv_screening_engine)

**The problem:** HR teams receive hundreds of applications per role. Reading every CV manually to shortlist 10 candidates is a full day of work — often done inconsistently depending on who's reviewing.

**What it does:** Watches a Gmail inbox for application emails, extracts the CV PDF, uses GPT-4o-mini to pull structured fields (name, email, skills, years of experience, GitHub/LinkedIn), fetches the candidate's GitHub profile to compute a 0–5 signal score based on repo count, recent activity, languages used, followers, and documentation quality, then sends everything to GPT-4o-mini for a final 0–10 fit score against a configurable role rubric. A separate daily flow reads the full candidate sheet, ranks by score, and emails HR a top-20 shortlist digest.

```
Gmail Trigger (new application email)
        ↓
Has CV attachment? → No → drop
        ↓ Yes
Extract CV text from PDF
        ↓
GPT-4o-mini → structured fields
(name, email, skills, experience, GitHub URL)
        ↓
Has GitHub URL?
   ↓ Yes                    ↓ No
Fetch GitHub profile    GitHub score = 0
Compute signal score
(repos, activity, languages, followers, docs)
        ↓
GPT-4o-mini final score (0–10)
Skills match (0–4) + Experience (0–3) + GitHub (0–3)
        ↓
Append full record to Google Sheets

Daily Schedule Trigger (HR Digest)
        ↓
Read All Candidates sheet
        ↓
Rank by score → top 20
        ↓
Append to Shortlist sheet
        ↓
Build HTML digest → email HR
```

> ⚠️ Screening aid only — all scores include human-readable reasoning and are meant to help a reviewer prioritize, not replace their judgment.

**Tech stack:** n8n · OpenAI GPT-4o-mini · GitHub API · Gmail · Google Sheets

**Who buys this:** HR departments, recruitment agencies, fast-growing startups with high application volume

---

### 4. WhatsApp AI Booking Bot

📁 [`WhatsApp AI Agent/`](./WhatsApp%20AI%20Agent)

**The problem:** Local businesses — clinics, salons, tutors, real estate agents — receive dozens of "are you available Friday at 3pm?" messages daily on WhatsApp. Answering each one manually takes 2–3 hours that nobody has.

**What it does:** Connects to WhatsApp Business via Meta Cloud API. When a customer sends any message, the bot detects whether it's a booking request or a general question. If booking: Groq AI extracts the date and time from natural language, snaps it to the nearest 30-minute business slot, checks Google Calendar for availability, creates the event if free, and sends a confirmation — all in under 5 seconds. If the slot is taken, it apologizes and asks for another time. If the message is vague, it sends the full list of available slots. If it's a general question, Groq answers conversationally.

```
WhatsApp message → Meta Cloud API webhook
        ↓
Extract sender, message text, phone number
        ↓
Skip verification pings + status updates
        ↓
Booking intent? (regex keyword detection)
   ↓ Yes                         ↓ No
Groq — extract date/time     Groq — chat reply
Snap to 30-min slot               ↓
        ↓                   Send reply → done
Valid datetime?
   ↓ Yes        ↓ No
Google Cal   Ask for
check        clarification
   ↓
Slot free?
   ↓ Yes      ↓ No
Create event  Busy message
Confirmation
        ↓
Meta API → send WhatsApp reply
```

**Business rules enforced:**
- Working days: Monday – Saturday
- Hours: 10:00 AM – 7:00 PM
- Slot duration: 30 minutes
- Auto-rounds "2:10pm" to 14:00, "2:20pm" to 14:30
- Sunday requests rejected gracefully with alternative suggestion

**Tech stack:** n8n · Meta Cloud API · Groq (LLaMA 3.3 70B) · Google Calendar API · Cloudflare Tunnel

**Who buys this:** Every local business that books appointments via WhatsApp — clinics, salons, tutors, fitness trainers, real estate agents

---

### 5. AI Invoice Processor

📁 [`AI-Invoice-Processor/`](./AI-Invoice-Processor)

**The problem:** Accountants and finance teams at SMBs receive 50–200 invoices per month by email. Manually copying vendor name, amounts, dates, and line items from PDFs into spreadsheets takes 3–5 minutes per invoice — up to 16 hours of work per month.

**What it does:** Watches a Gmail inbox, detects emails with PDF attachments, converts each PDF to plain text, sends the text to Groq which extracts 16 structured fields (vendor, dates, amounts, tax, line items, payment terms, currency), validates that all critical fields were found, and routes each invoice to either the Invoices sheet with an auto-confirmation reply to the sender — or the Errors sheet with an alert to your inbox listing exactly what was missing.

```
Gmail polls inbox (every 5 min)
        ↓
Has PDF attachment? → No → stop
        ↓ Yes
Extract PDF → plain text
        ↓
Groq (LLaMA 3.3) — extract 16 invoice fields
        ↓
Parse + validate (vendor + total + date present?)
        ↓
   Valid?
   ↓ Yes                    ↓ No
Log to Invoices sheet    Log to Errors sheet
Send confirmation        Send alert email
to vendor                (what's missing)
```

**Fields extracted:** Invoice number, invoice date, due date, vendor name, vendor email, vendor address, bill-to, subtotal, tax amount, tax rate, total amount, currency, payment terms, line items, notes, AI confidence score

**Tech stack:** n8n · Groq (LLaMA 3.3 70B) · Gmail · Google Sheets · n8n Extract From File node

**Who buys this:** Accountants, finance managers at SMBs, bookkeeping firms, e-commerce businesses

---

### 6. Lead Capture & CRM Pipeline

📁 [`AI-Powered Lead Capture & CRM Automation Pipeline/`](./AI-Powered%20Lead%20Capture%20%26%20CRM%20Automation%20Pipeline)

**The problem:** Inbound leads die in email inboxes. Someone submits a contact form, and by the time a human reads it, categorizes it, adds it to the CRM, sends an acknowledgment, and notifies the sales team — an hour has passed. Response time is one of the biggest predictors of conversion.

**What it does:** A form submission hits a webhook, fields are normalized, Groq AI qualifies the lead (Hot/Warm/Cold, priority 1–10, reason, suggested follow-up), and the enriched lead fans out in parallel to HubSpot (new contact), Gmail (personalized welcome email to the lead), Slack (sales team alert with AI score and suggested opening line), and Google Sheets (running log) — all in under 10 seconds.

```
Form submitted → Webhook
        ↓
Normalize fields (name, email, phone, company, message)
        ↓
Groq — AI qualification
(Hot/Warm/Cold · priority 1–10 · reason · follow-up suggestion)
        ↓
Parse AI score + merge with lead data
        ↓
Fan out in parallel:
├── HubSpot → Create contact (with score)
├── Gmail → Personalized welcome email
├── Slack → Sales alert (#new-leads)
└── Google Sheets → Log all fields + score
```

**Tech stack:** n8n · Groq (LLaMA 3.3 70B) · HubSpot API · Gmail · Slack · Google Sheets

**Who buys this:** Sales teams, marketing agencies, SaaS companies with inbound lead flow, coaches and consultants

---

### 7. Daily AI Social Media Pipeline

📁 [`AI-SocialMedia-Pipeline/`](./AI-SocialMedia-Pipeline)

**The problem:** Staying consistent on LinkedIn and a blog requires 3–5 hours of content work per week — research, writing, formatting, publishing. Most creators either burn out or go silent.

**What it does:** Every morning at 9AM, Groq picks a fresh Personal Finance topic with a unique angle (ensuring no repeats), writes a full LinkedIn post with hook + hashtags and a 400–600 word blog article with SEO title and meta description, publishes both via the LinkedIn UGC API and WordPress REST API, logs everything to Google Sheets as a content library, and emails a formatted HTML summary of what went live.

```
Schedule Trigger (9AM Mon-Sat)
        ↓
Groq — pick today's unique topic
(angle, content type, target emotion)
        ↓
Groq — write all content
(LinkedIn post + blog article + hashtags + SEO)
        ↓
Parse + clean all content
        ↓
Fan out in parallel:
├── LinkedIn UGC API → publish post
├── WordPress REST API → publish blog article
└── Google Sheets → log to content library
        ↓
Gmail → HTML daily summary email
```

**Niche:** Personal Finance & Investing (configurable to any niche)
**Output per run:** 1 LinkedIn post (150–250 words) + 1 blog article (400–600 words) + 10 hashtags + SEO meta

**Tech stack:** n8n · Groq (LLaMA 3.3 70B) · LinkedIn API · WordPress REST API · Google Sheets · Gmail

**Who buys this:** Content creators, personal finance educators, marketing agencies managing multiple LinkedIn accounts

---

### 8. Basic RAG Chatbot

📁 [`basic_RAG_chatbot/`](./basic_RAG_chatbot)

> *First RAG implementation — built to learn the full retrieval-augmented generation stack from scratch.*

**The problem:** Generic AI chatbots hallucinate answers about your specific business. A customer asking about your refund policy or pricing should get answers from your actual documents, not from the AI's training data.

**What it does:** A Python backend that ingests a folder of company documents (about, FAQ, pricing, services, careers, contact, terms, privacy), chunks and embeds them using `all-MiniLM-L6-v2` into a persistent ChromaDB vector database, and at query time retrieves the top-3 most relevant chunks, builds a context-grounded prompt, and sends it to Google Gemini which answers using only the provided context. A FastAPI endpoint exposes the chat interface, and a simple HTML frontend provides the UI.

```
Documents (markdown files)
        ↓
LangChain TextLoader → chunk (500 chars, 50 overlap)
        ↓
SentenceTransformer embed (all-MiniLM-L6-v2)
        ↓
Store in ChromaDB (persistent)

User query → POST /chat
        ↓
Embed query → vector search ChromaDB (top-3 chunks)
        ↓
Build context-grounded prompt
        ↓
Google Gemini → answer (context only, no hallucination)
        ↓
Return JSON response → HTML frontend
```

**Architecture:**
```
basic_RAG_chatbot/
├── backend/
│   ├── app.py          FastAPI server + /chat endpoint
│   ├── ingest.py       Document loader + embedder + Chroma writer
│   ├── rag.py          Query embedding + retrieval + Gemini call
│   └── config.py       API keys + paths via dotenv
├── docs_project/       Company knowledge base (10 markdown files)
└── frontend/
    └── chat_ui.html    Simple browser chat interface
```

**Tech stack:** Python · FastAPI · ChromaDB · SentenceTransformers · LangChain · Google Gemini · HTML/CSS

**What I learned:** Full RAG pipeline from scratch — document chunking strategy, embedding models, vector similarity search, context window management, and grounding LLM responses to a knowledge base.

---

### 9. Elsa Energy RAG Chatbot

📁 [`elsa-RAG-chatbot/`](./elsa-RAG-chatbot)

> *Production RAG chatbot delivered as an internship project for a real client in the smart home and energy management industry.*

**The problem:** Generic AI chatbots can't answer questions about a company's specific products, pricing, or policies — they hallucinate. Elsa Energy needed a chatbot that could answer customer queries strictly from their own knowledge base, and drop into their existing Laravel web app with minimal integration effort.

**What it does:** A Python FastAPI microservice ingests the client's knowledge documents, chunks and embeds them using the Gemini Embedding API, and stores them in a lightweight SQLite vector store (no C++ dependencies, no Docker). At query time, the user's message is embedded, cosine similarity is computed in pure Python against all stored chunks, and the top-3 most relevant chunks are injected into a dynamic system prompt sent to Gemini 2.5 Flash — which answers only from that context. A plug-and-play frontend widget (Glassmorphism design, single `<script>` tag to embed) connects to the API and maintains full conversation history per session.

```
User message
      │
      ▼
[Embed query] ──→ Gemini Embedding API (gemini-embedding-001)
      │
      ▼
[Cosine similarity search] ──→ SQLite vector_store.db
      │
      ▼
[Top-3 chunks retrieved]
      │
      ▼
[Dynamic system prompt] ──→ Gemini 2.5 Flash
      │
      ▼
[Grounded answer returned to frontend widget]
```

**Architecture:**
```
elsa-RAG-chatbot/
├── backend/
│   ├── main.py            FastAPI server — /chat & /ingest routes
│   ├── ingest.py          Document chunking + Gemini embedding pipeline
│   ├── requirements.txt
│   └── knowledge_base/    Client knowledge documents (.txt / .md)
└── frontend/
    ├── widget.html        Standalone sandbox for testing
    ├── chatbot.css        Glassmorphism styling (Teal & Indigo tokens)
    └── chatbot.js         Chat logic, session history, Markdown renderer
```

**Key engineering decisions:**
- SQLite + pure-Python cosine similarity — zero native dependencies, runs anywhere without a Docker container
- Zero-hallucination enforcement — the LLM system prompt strictly constrains answers to retrieved context only
- `/ingest` API route — allows re-ingestion of the knowledge base at runtime without restarting the server
- Laravel-ready proxy pattern documented — one route + two asset copies and the widget is live

**Tech stack:** Python · FastAPI · Google Gemini 2.5 Flash · Gemini Embedding API · SQLite · Vanilla JS · HTML5/CSS3

**Who buys this:** SMBs with product/support knowledge bases, SaaS companies, client-facing businesses that need a branded AI assistant without hallucinations

---

### 10. AI Code Summarizer

📁 [`code_summarizer/`](./code_summarizer)

> *A beginner automation built while learning n8n — showcasing multi-branch AI orchestration and Gmail integration.*

**The problem:** Developers submitting code snippets for review or documentation need both inline comments and a plain-English summary — two different outputs that would normally require two separate manual steps.

**What it does:** Watches a Gmail inbox for incoming emails containing source code. When one arrives, two parallel AI chains run simultaneously — one generates inline comments for the code, the other writes a plain-English summary. Both outputs are merged, aggregated into a single clean response, and emailed back to the sender automatically.

```
Gmail Trigger (new email with code)
        │
        ▼
Fan out in parallel:
├── AI Chain 1 → Generate inline code comments
└── AI Chain 2 → Write plain-English summary
        │
        ▼
Merge Node → combine both outputs
        │
        ▼
Aggregate Node → format final response
        │
        ▼
Gmail → send result back to sender
```

**Tech stack:** n8n · OpenAI · Gmail Trigger · AI Chain Nodes · Merge Node · Aggregate Node · Gmail

**What I learned:** Multi-branch n8n workflows, parallel AI chain execution, merging divergent workflow paths, and formatting AI-generated output for delivery.

---

### 11. Feedback Discount Decision

📁 [`Feedback-Discount-Decision/`](./Feedback-Discount-Decision)

> *My first automation — built while learning n8n fundamentals. Kept here to show where this journey started.*

**What it does:** A customer submits a feedback form. The workflow evaluates the submission using an IF node. If conditions are met, a discount is assigned. The result is appended to Google Sheets.

Simple as it is, this project taught me the fundamentals that every project above is built on: triggers, conditional branching, data mapping, and external integrations.

**Tech stack:** n8n · Form Trigger · IF Node · Set Node · Google Sheets

---

## Skills Demonstrated Across This Portfolio

| Skill | Projects |
|---|---|
| LLM integration (Groq, OpenAI, Gemini) | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 |
| n8n workflow orchestration | 1, 2, 3, 4, 5, 6, 7, 10, 11 |
| Multi-branch conditional logic | 1, 3, 4, 5, 6 |
| Error handling + alerting | 1, 2, 5 |
| Webhook design + API integration | 1, 4, 6, 7 |
| PDF parsing + document extraction | 5, 8 |
| Vector databases + RAG | 8, 9 |
| Python + FastAPI backend | 8, 9 |
| Web scraping (Apify) | 2 |
| GitHub API + signal scoring | 3 |
| Rate-limit-safe processing | 1 |
| Deduplication + state management | 2 |
| Google Workspace APIs | 1, 2, 3, 5, 6, 7 |
| WhatsApp / Meta Cloud API | 4 |
| LinkedIn API | 7 |
| HubSpot CRM integration | 6 |
| Scheduling + cron-based triggers | 2, 3, 7 |

---

## How to Use These Projects

### n8n workflows (projects 1–7, 10, 11)
1. Open your n8n instance
2. Go to the project folder and download the `.json` file
3. In n8n: menu → Import from file → upload the JSON
4. Follow the setup guide in that project's README
5. Connect your credentials and update placeholder values
6. Click Publish to activate

### Python RAG chatbot (project 8)
```bash
git clone https://github.com/m-hannanfaisal/AI-Automation-Projects
cd AI-Automation-Projects/basic_RAG_chatbot

pip install fastapi uvicorn chromadb sentence-transformers \
    langchain langchain-community google-generativeai python-dotenv

# Set up .env
echo "GOOGLE_API_KEY=your_gemini_key_here" > .env

# Update config.py with your actual DOCS_PATH and DB_PATH

# Ingest your documents
python backend/ingest.py

# Start the API
uvicorn backend.app:app --reload

# Open frontend/chat_ui.html in your browser
```

### Elsa Energy RAG Chatbot (project 9)
```bash
git clone https://github.com/m-hannanfaisal/AI-Automation-Projects
cd AI-Automation-Projects/elsa-RAG-chatbot/backend

pip install -r requirements.txt

# Set up .env
cp .env.example .env
# Add your GEMINI_API_KEY to .env

# Ingest the knowledge base
python ingest.py

# Start the API
uvicorn main:app --reload

# Open frontend/widget.html in your browser to test
# Or follow the Laravel integration guide in the README
```

---

## Adding a New Project

This repo is structured for easy extension. When you add a new project:

1. Create a new folder: `Your-Project-Name/`
2. Add: workflow JSON (or code files) + `README.md` + screenshot
3. Add a row to the [Project Index](#project-index) table at the top
4. Add a new section following the template:

```markdown
### N. Project Name

📁 [`folder-name/`](./folder-name)

**The problem:** [one paragraph — what pain does this solve?]

**What it does:** [what happens, end to end]

[architecture diagram in ASCII or code block]

**Tech stack:** [tools used]

**Who buys this:** [target client]
```

---

## Contact

**Hannan Faisal** — AI Automation Specialist 
Reach me at hannanfaisal0507@gmail.com

Available for freelance projects.

Specializing in: n8n workflow automation · LLM integrations · WhatsApp bots · Lead generation systems · AI-powered document processing · RAG chatbots

---

## License

MIT License — free to use, adapt, and deploy for client projects.
