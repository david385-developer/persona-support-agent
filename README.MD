# CloudFlow — Persona-Adaptive Customer Support Agent

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![LLM: Groq](https://img.shields.io/badge/LLM-Groq%20Llama%203.3%2070B-orange)](https://groq.com/)
[![Vector DB: FAISS](https://img.shields.io/badge/Vector%20DB-FAISS-green)](https://github.com/facebookresearch/faiss)

## Overview

**CloudFlow** is an AI-powered customer support chatbot that automatically detects customer types, retrieves relevant answers from a knowledge base, and adapts its response tone to match the customer's communication style. It intelligently escalates complex issues to human agents when needed, using a hybrid LLM + heuristic approach for persona classification and a RAG pipeline for grounded, knowledge-aware responses.

---

## Table of Contents

- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [System Components](#system-components)
  - [Persona Detection](#persona-detection-hybrid-approach)
  - [RAG Pipeline](#rag-pipeline-design)
  - [Response Generation](#response-generation)
  - [Escalation Logic](#escalation-logic)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Example Queries](#example-queries)
- [Knowledge Base](#knowledge-base)
- [Known Limitations](#known-limitations)
- [Future Improvements](#future-improvements)

---

## Tech Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Python** | Python | 3.11+ | Primary language |
| **LLM** | Groq API | v1.0 | Free-tier inference for persona detection & response generation |
| **Groq SDK** | groq | 0.37.1 | Groq API client library |
| **Agent Framework** | LangChain | 1.3.10 | Orchestration, document loading, chunking |
| **LangChain Groq** | langchain-groq | 1.1.3 | Groq integration for LangChain |
| **LangChain Core** | langchain-core | 1.4.8 | Core abstractions for chains & components |
| **LangChain Community** | langchain-community | 0.4.2 | Community integrations (FAISS, loaders) |
| **LangChain Text Splitters** | langchain-text-splitters | 1.1.2 | RecursiveCharacterTextSplitter |
| **Embeddings** | sentence-transformers | 5.6.0 | all-MiniLM-L6-v2 (384-dim local embeddings) |
| **Vector Database** | faiss-cpu | 1.14.3 | IndexFlatIP for cosine similarity search |
| **PDF Loading** | pypdf | 6.13.3 | PyPDFLoader for document ingestion |
| **PDF Generation** | fpdf | 1.7.2 | Programmatic PDF creation for knowledge base |
| **Document Processing** | unstructured | 0.23.1 | Multi-format document loading |
| **UI (Web)** | Streamlit | 1.58.0 | Interactive chat interface with sidebar |
| **UI (CLI)** | Python stdlib | Built-in | Terminal chatbot via `input()`/`print()` |
| **Config Management** | python-dotenv | 1.2.2 | .env file parsing for API keys |
| **Data Processing** | pandas | 3.0.3 | DataFrames for structured retrieval results |
| **NLP Utilities** | spaCy | 3.8.14 | Text preprocessing (optional, included) |
| **HTTP Requests** | requests | 2.34.2 | HTTP client for external APIs |

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    USER MESSAGE INGESTION                        │
│                      (CLI or Streamlit)                          │
└────────────────────────┬─────────────────────────────────────────┘
                         │
        ┌────────────────▼────────────────┐
        │  PERSONA DETECTION              │
        │  ┌──────────────────────────┐   │
        │  │ 1. LLM Classification    │   │
        │  │    (Groq: Llama 3.3)     │   │
        │  └──────────────────────────┘   │
        │  ┌──────────────────────────┐   │
        │  │ 2. Heuristic Keywords    │   │
        │  │    (Keyword Matching)    │   │
        │  └──────────────────────────┘   │
        │  ┌──────────────────────────┐   │
        │  │ 3. Hybrid Combination    │   │
        │  │    (Weighted Blend)      │   │
        │  └──────────────────────────┘   │
        └────────────────┬─────────────────┘
                         │
        ┌────────────────▼─────────────────┐
        │  RETRIEVAL (RAG PIPELINE)        │
        │  ┌──────────────────────────┐    │
        │  │ 1. Query Embedding       │    │
        │  │    (MiniLM-L6-v2)        │    │
        │  └──────────────────────────┘    │
        │  ┌──────────────────────────┐    │
        │  │ 2. FAISS Similarity      │    │
        │  │    Search (Top-K=4)      │    │
        │  └──────────────────────────┘    │
        │  ┌──────────────────────────┐    │
        │  │ 3. Confidence Check      │    │
        │  │    (>= 0.35 threshold)   │    │
        │  └──────────────────────────┘    │
        └────────────────┬─────────────────┘
                         │
        ┌────────────────▼─────────────────┐
        │  ESCALATION DECISION             │
        │  ├─ Sensitive Keywords?          │
        │  ├─ Low Retrieval Confidence?    │
        │  ├─ User Frustration?            │
        │  ├─ Prolonged Conversation?      │
        │  └─ Explicit Human Request?      │
        └────────────────┬─────────────────┘
                         │
        ┌────────────────▼─────────────────┐
        │ Response Generation              │
        │ (Persona-Specific Prompt +       │
        │  Retrieved Context +             │
        │  Conversation History)           │
        │ → Groq LLM → Adaptive Response   │
        └────────────────┬─────────────────┘
                         │
        ┌────────────────▼─────────────────┐
        │  OUTPUT & STATE UPDATE           │
        │  (Response + Metadata +          │
        │   Updated Conversation History)  │
        └─────────────────────────────────┘
```

---

## System Components

### Persona Detection (Hybrid Approach)

The system classifies users into **3 personas** using parallel LLM and heuristic methods:

#### **The 3 Personas**

| Persona | Characteristics | Response Style |
|---------|-----------------|-----------------|
| **Technical Expert** | Jargon-heavy, requests error codes, API details, technical depth | Direct, code-focused, include commands & workarounds, skip pleasantries |
| **Frustrated User** | Emotional language, repeated complaints, urgency signals | Empathetic, simple numbered steps, reassuring tone, checkin questions |
| **Business Executive** | Outcome-focused, asks about ROI, SLA, timelines, operations impact | Bottom-line first, bullet points, business impact framing, include ETAs |

#### **Detection Method**

1. **LLM Classification** (Primary)
   - Sends user message to Groq (Llama 3.3 70B) with structured system prompt
   - Returns JSON: `{persona, confidence (0-1), reasoning}`
   - Fast inference using Groq's free tier

2. **Heuristic Keywords** (Backup/Blend)
   - Counts keyword matches per persona:
     - Technical: `"api"`, `"error"`, `"code"`, `"debug"`, `"json"`, `"endpoint"`, etc.
     - Frustrated: `"nothing works"`, `"ridiculous"`, `"broken"`, `"unacceptable"`, `"terrible"`, `"fix"`, etc.
     - Business: `"roi"`, `"sla"`, `"operations"`, `"cost"`, `"timeline"`, `"impact"`, etc.
   - Exclamation mark density signals frustration

3. **Combination Logic**
   - If LLM confidence ≥ 0.8 → **trust LLM result**
   - If LLM confidence < 0.8 → **blend**: 60% LLM + 40% heuristic (weighted score)
   - If disagreement → pick **higher-confidence** result
   - If LLM fails → **fall back to heuristics entirely**

**Output**: `(persona_name, confidence_score, detection_method)`

---

### RAG Pipeline Design

The knowledge base is retrieved using a 5-step RAG pipeline:

#### **1. Document Loading**
- **Format Support**: `.md`, `.txt`, `.pdf`
- **Tool**: LangChain `DirectoryLoader` + `PyPDFLoader`
- **Metadata Preservation**: Page numbers and source filenames stored with each chunk

#### **2. Chunking Strategy**
- **Splitter**: `RecursiveCharacterTextSplitter`
- **Config**:
  - Chunk size: **500 characters**
  - Overlap: **80 characters** (prevents context loss at boundaries)
  - Separators (in order): Markdown headings → double newlines → single newlines → sentences → spaces
- **Chunk Metadata**: source file, first heading in chunk, page number (PDFs), unique chunk_id

#### **3. Embedding**
- **Model**: `sentence-transformers/all-MiniLM-L6-v2` (384 dims)
- **Normalization**: Embeddings normalized to unit vectors (`normalize_embeddings=True`)
- **Execution**: Runs locally on CPU (no API calls, full privacy)

#### **4. Vector Storage**
- **Database**: FAISS `IndexFlatIP`
- **Similarity Metric**: Inner product on normalized vectors = **cosine similarity**
- **Persistence**: Index + chunk list saved to `.vector_store/` directory (loaded on startup)

#### **5. Retrieval & Ranking**
- **Query Process**:
  1. User query → normalized embedding (same MiniLM model)
  2. FAISS searches top-K nearest neighbors (default K=4)
  3. Returns: `(chunk_content, metadata, cosine_similarity_score)`
- **Confidence Check**: Average similarity score must be ≥ 0.35; otherwise triggers escalation

---

### Response Generation

Each persona receives a tailored system prompt that guides the LLM's response style:

```
PERSONA PROMPTS (pseudo-code):

Technical Expert:
  "You are a technical support specialist. Be direct. Include error codes, 
   API endpoints, and commands. Offer workarounds. Skip pleasantries."

Frustrated User:
  "Lead with empathy and reassurance. Use simple, numbered steps.
   Use a calm, supportive tone. End with a check-in question."

Business Executive:
  "Be concise. Lead with business impact and timelines. Use bullet points.
   Reference SLAs and uptime guarantees. Frame outcomes around ROI."
```

**Prompt Construction**:
```
System Prompt (persona-specific rules)
+ Retrieved Context (top-4 chunks from knowledge base)
+ Conversation History (last 3-5 exchanges)
+ User Message
+ Instruction: "Answer ONLY from the above context. Do not hallucinate."
```

**Output**: LLM streams response tailored to detected persona, grounded in retrieved knowledge.

---

### Escalation Logic

Automatic escalation is triggered by **6 configurable rules**:

| Trigger | Condition | Detection Method | Priority |
|---------|-----------|------------------|----------|
| **Sensitive Keywords** | Mentions: billing, legal, refund, data breach, lawsuit, "cancel account" | Keyword matching against sensitive list | P1 (1 hr SLA) |
| **Explicit Human Request** | User says: "speak to human", "talk to manager", "escalate", "support team" | Keyword matching | P3 (24 hr) |
| **Retry Threshold Exceeded** | User signals dissatisfaction 3+ times: "doesn't help", "already tried", "not working" | Retry counter | P3 (24 hr) |
| **No Relevant Docs** | FAISS retrieval returns 0 results or all chunks below 0.1 similarity | Retrieval check | P4 (48 hr) |
| **Low Confidence** | Average cosine similarity of top-4 chunks < 0.35 | Similarity score calculation | P4 (48 hr) |
| **Prolonged Conversation** | Conversation history ≥ 4 user turns without resolution | Message count tracking | P2 (4 hr) |

**Bonus Trigger**: If no rule fires but conversation ≥ 4 messages, an LLM-based evaluation determines if escalation is warranted.

#### **Escalation Handoff**
When escalation triggers, a structured JSON summary is generated:

```json
{
  "persona": "Frustrated User",
  "priority": "P2",
  "issue_summary": "User unable to reset password after multiple attempts",
  "documents_used": ["04_password_reset.md", "11_security_policy.md"],
  "attempted_steps": [
    "Checked email for reset link",
    "Verified account exists",
    "Confirmed browser cookies enabled"
  ],
  "conversation_summary": "User has retried 4 times over 2 turns...",
  "recommended_next_steps": [
    "Check account lockout status",
    "Verify email deliverability",
    "Offer manual account recovery"
  ]
}
```

User sees: *"You're being connected to a human specialist who specializes in account recovery. They have context from our conversation above."*

---

## Project Structure

```
persona-support-agent/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── .env.example                   # Example environment file
├── .gitignore                     # Git exclusions
│
├── config.py                      # Global constants: API keys, paths, thresholds
├── test_groq.py                   # Quick Groq API connectivity test
│
├── cli.py                         # Terminal-based chatbot interface
├── app_streamlit.py               # Web UI (Streamlit)
│
├── data/                          # Knowledge base (16 documents)
│   ├── 01_password_reset.md
│   ├── 02_api_troubleshooting.md
│   ├── ... (13 more .md files)
│   └── 16_escalation_procedures.pdf
│
├── .vector_store/                 # FAISS index + cached embeddings (auto-generated)
│   ├── index.faiss
│   └── chunks.pkl
│
└── src/                           # Core Python modules
    ├── __init__.py
    ├── knowledge_base.py          # KnowledgeBase class: load, chunk, embed, retrieve
    ├── persona_detector.py        # PersonaDetector class: LLM + heuristic classification
    ├── response_generator.py      # ResponseGenerator class: persona-specific prompts → LLM
    ├── escalation.py              # EscalationManager class: triggers, priority, handoff
    ├── agent.py                   # SupportAgent class: main orchestrator
    ├── llm.py                     # LLM client wrapper (Groq)
    ├── config.py                  # Config loading & constants
    ├── conversation_memory.py     # Conversation state management
    └── handoff.py                 # Handoff summary generation
```

---

## Installation & Setup

### Prerequisites
- Python 3.11+
- Groq API key (free tier: [console.groq.com/keys](https://console.groq.com/keys))

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/persona-support-agent.git
cd persona-support-agent
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### Step 5: Verify Groq Connectivity
```bash
python test_groq.py
```

Expected output:
```
✓ Groq API key is valid
✓ Model 'llama-3.3-70b-versatile' is available
✓ Test inference: "Hello" → "Hello! How can I assist you today?"
```

### Step 6: Generate Knowledge Base (Optional)
If data/ directory is empty, run:
```bash
python create_documents.py
```

This generates 15 markdown files + 1 PDF into `data/` directory.

### Step 7: Build Vector Index
```bash
python ingest.py
```

Expected output:
```
Loading documents from data/...
  ✓ Loaded 16 documents (45 KB total)
Chunking...
  ✓ Created 234 chunks (avg 195 chars)
Embedding (this may take 30-60 seconds)...
  ✓ Embedded 234 chunks
Building FAISS index...
  ✓ Index saved to .vector_store/index.faiss
  ✓ Chunks saved to .vector_store/chunks.pkl
Ready for inference!
```

### Step 8: Run the Chatbot

**CLI Interface** (interactive terminal):
```bash
python cli.py
```

**Streamlit Web UI**:
```bash
streamlit run app_streamlit.py
```

Both interfaces support:
- Type your support request → persona auto-detection
- View detected persona + confidence + retrieval sources
- Automatic escalation when appropriate
- `reset` command (CLI) or "New Conversation" button (Streamlit) to start fresh

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | ✓ Yes | — | Free API key from [console.groq.com/keys](https://console.groq.com/keys) |
| `GROQ_MODEL` | No | `llama-3.3-70b-versatile` | Groq model ID (other options: `mixtral-8x7b-32768`, `gemma-7b-it`) |
| `CHUNK_SIZE` | No | 500 | Characters per document chunk |
| `CHUNK_OVERLAP` | No | 80 | Character overlap between chunks |
| `TOP_K` | No | 4 | Number of documents to retrieve per query |
| `SIMILARITY_THRESHOLD` | No | 0.35 | Minimum cosine similarity for retrieval confidence |
| `PERSONA_LLM_THRESHOLD` | No | 0.8 | LLM confidence threshold for persona detection |
| `MAX_CONVERSATION_TURNS` | No | 4 | Turn count before escalation |

---

## Usage

### CLI Interface

```bash
$ python cli.py

Welcome to CloudFlow Support. Type 'quit' to exit, 'reset' for new conversation.

You: I'm getting 401 errors when calling the API. Can you help?

[PERSONA DETECTION]
Persona: Technical Expert | Confidence: 0.87 (LLM) | Method: LLM Classification

[RESPONSE]
You're encountering a 401 Unauthorized error. Here's what to check:

1. Verify your API key is correct in the Authorization header:
   Authorization: Bearer YOUR_API_KEY

2. Ensure your key hasn't expired. Check your account settings...
   
[SOURCES]
- 02_api_troubleshooting.md (Section: "401 Unauthorized") [Score: 0.78]
- 11_security_policy.md (Section: "API Authentication") [Score: 0.65]
```

### Streamlit Web UI

```bash
$ streamlit run app_streamlit.py
```

Features:
- **Chat Interface**: Message history with timestamps
- **Sidebar Display**:
  - Persona badge (color-coded: 🔵 Technical, 🔴 Frustrated, 🟡 Business)
  - Message count & dissatisfaction counter
  - Escalation status & handoff JSON
- **Expandable Sources**: View retrieval details for each response
- **New Conversation**: Reset button to clear state

---

## Example Queries

### **Persona 1: Technical Expert**
```
User: "The webhook delivery is failing with a 503. I've verified the endpoint 
       is reachable with curl. What error codes should I check in the logs?"

Expected Response:
- Direct, technical language
- Include error code meanings
- Offer debugging commands
- Reference API documentation sections
```

### **Persona 2: Frustrated User**
```
User: "I've been trying to reset my password for an hour and it's not working! 
       This is ridiculous. Why can't I just get in???"

Expected Response:
- Lead with empathy: "I understand how frustrating this must be..."
- Simple, numbered steps
- Reassuring tone
- Offer escalation: "If this doesn't work, I can connect you with our account team"
```

### **Persona 3: Business Executive**
```
User: "What's the SLA uptime commitment? We need 99.9% for our compliance audit."

Expected Response:
- Bottom-line first
- Include SLA percentages and incident response times
- Frame around business impact
- Link to compliance documentation
```

### **Escalation Scenario 1: Sensitive Keywords**
```
User: "I need to cancel my account and get a refund for this month."

Expected Response:
- Automatic escalation triggered (keywords: "cancel", "refund")
- P2 priority (4-hour SLA)
- Handoff summary generated
- User message: "You're being connected to our billing specialist..."
```

### **Escalation Scenario 2: Repeated Dissatisfaction**
```
User Turn 1: "This doesn't work."
User Turn 2: "I already tried that."
User Turn 3: "Nothing you suggest actually helps!"

Expected Response:
- Escalation triggered (retry count = 3)
- P3 priority (24-hour SLA)
- Summary: Attempted steps documented, persona tracked
- Escalation banner shown
```

---

## Knowledge Base

CloudFlow's knowledge base covers **16 documents** on a fictional SaaS workflow automation platform:

| # | Document | Content Coverage |
|---|----------|------------------|
| 1 | Product Overview | Plans, features, pricing, core workflows |
| 2 | Password Reset Guide | Self-service reset flow, email delivery, security |
| 3 | Billing & Subscription FAQ | Billing cycles, payment methods, upgrades/downgrades |
| 4 | Account Management | Team management, SSO setup, account deletion |
| 5 | API Error Troubleshooting | 401, 403, 404, 429, 500, 503 errors + solutions |
| 6 | Connectivity Troubleshooting | Dashboard, API, webhook connectivity issues |
| 7 | Email Delivery Troubleshooting | Bounce rates, deliverability, SPF/DKIM setup |
| 8 | Performance Troubleshooting | Slow workflows, query optimization, bottlenecks |
| 9 | Payment Troubleshooting | Failed transactions, declined cards, reconciliation |
| 10 | Security Policy | Encryption, compliance (SOC 2, GDPR), incident response |
| 11 | SLA Agreement | Uptime commitments, response times, incident credits |
| 12 | Refund Policy | 30-day guarantee, partial refunds, dispute process |
| 13 | Data Privacy Policy | Data residency, GDPR rights, data export/deletion |
| 14 | Onboarding Guide | First-time setup, quickstart, team invitations |
| 15 | Mobile App Troubleshooting | iOS/Android issues, offline mode, sync problems |
| 16 | Escalation Procedures Manual (PDF) | Tier definitions, handoff protocol, SLA by priority |

**Total Knowledge Base Size**: ~45 KB, 234 chunks, 384-dim embeddings

---

## Known Limitations

1. **Groq API Dependency**: All persona detection and response generation require live Groq API access. Offline mode is not supported.

2. **Fixed Persona Count**: System is hard-coded for 3 personas. Adding a 4th requires modifying keyword lists, system prompts, and detection logic in `persona_detector.py`.

3. **Context Length**: LLM receives max ~4 chunks (2000 chars) of context. Very large documents may lose detail if chunks don't rank in top-4.

4. **Knowledge Base Staleness**: Vector embeddings are static. If documents are updated, `ingest.py` must be re-run to rebuild the index (currently a manual process).

5. **Multi-language Support**: All content, prompts, and keyword lists are English-only. Non-English queries may be misclassified or retrieve irrelevant results.

6. **No Learning/Feedback Loop**: Escalation data and resolved tickets are not fed back into the system. Historical performance metrics are not tracked.

---

## Future Improvements

- [ ] **Add Feedback Loop**: Collect resolved/unresolved feedback and retrain heuristic keyword weights
- [ ] **Dynamic Persona Configuration**: UI to add/edit personas, keywords, and system prompts without code changes
- [ ] **Multi-language Support**: Extend to Spanish, French, German with language detection
- [ ] **Conversation Analytics Dashboard**: Track metrics: persona distribution, escalation rate, resolution rate, avg response time
- [ ] **Context Window Optimization**: Implement hierarchical chunking (summary + detail) to fit more context
- [ ] **Real-time Escalation Handoff**: Integration with ticketing systems (Zendesk, Jira) for auto-creation
- [ ] **Fine-tuned Persona Model**: Train a smaller LLM on CloudFlow support patterns for faster persona detection
- [ ] **Offline Mode**: Fallback to local heuristics when Groq API is unavailable
- [ ] **Document Hot-reload**: Auto-detect new files in `data/` and update index without manual re-ingest
- [ ] **Conversation Export**: Download chat history as PDF with metadata

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Add tests for new functionality
4. Ensure all tests pass
5. Commit with clear messages (`git commit -m "Add persona sentiment analysis"`)
6. Push and open a Pull Request

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

---

## Support

- **Issues**: Open an issue on GitHub for bugs or feature requests
- **Documentation**: See inline code comments for detailed implementation notes
- **Groq API Docs**: [docs.groq.com](https://docs.groq.com/)
- **LangChain Docs**: [docs.langchain.com](https://docs.langchain.com/)

---

**Built with ❤️ using LangChain, FAISS, and Groq**
