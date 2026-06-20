#!/usr/bin/env python3
"""
Streamlit Web UI for the Persona-Adaptive Support Agent.

    streamlit run app_streamlit.py
"""

import uuid
import json
from datetime import datetime

import streamlit as st

from src.agent import SupportAgent, AgentResponse

# ── Page Config ──────────────────────────────────────────

st.set_page_config(
    page_title="CloudFlow Support Agent",
    page_icon=" ",
    layout="wide",
)

# ── Custom CSS ───────────────────────────────────────────

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=DM+Sans:wght@400;500;700&display=swap');

    .stApp { font-family: 'DM Sans', sans-serif; }

    .persona-badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .persona-technical {
        background: rgba(0, 200, 255, 0.15);
        color: #00c8ff;
        border: 1px solid rgba(0, 200, 255, 0.3);
    }
    .persona-frustrated {
        background: rgba(255, 180, 0, 0.15);
        color: #ffb400;
        border: 1px solid rgba(255, 180, 0, 0.3);
    }
    .persona-business {
        background: rgba(180, 100, 255, 0.15);
        color: #b464ff;
        border: 1px solid rgba(180, 100, 255, 0.3);
    }

    .escalation-banner {
        background: linear-gradient(135deg, #ff4444, #cc0000);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: 700;
        margin: 10px 0;
        text-align: center;
        letter-spacing: 1px;
    }

    .source-chip {
        display: inline-block;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        margin: 2px;
        color: #aaa;
        font-family: 'JetBrains Mono', monospace;
    }

    .metric-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)


# ── Initialize Agent (cached) ────────────────────────────

@st.cache_resource
def load_agent():
    """Initialize the support agent once and cache it."""
    agent = SupportAgent()
    agent.initialize_knowledge_base()
    return agent


# ── Session State ────────────────────────────────────────

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]

if "messages" not in st.session_state:
    st.session_state.messages = []

if "stats" not in st.session_state:
    st.session_state.stats = {
        "total_queries": 0,
        "escalations": 0,
        "personas": {
            "Technical Expert": 0,
            "Frustrated User": 0,
            "Business Executive": 0,
        },
    }


# ── Sidebar ──────────────────────────────────────────────

with st.sidebar:
    st.markdown("## CloudFlow Support")
    st.markdown("---")
    st.markdown(f"**Session:** `{st.session_state.session_id}`")

    if st.button("New Session", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())[:8]
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("### Session Stats")
    stats = st.session_state.stats
    col1, col2 = st.columns(2)
    col1.metric("Queries", stats["total_queries"])
    col2.metric("Escalations", stats["escalations"])

    st.markdown("---")
    st.markdown("### Personas Detected")
    for persona, count in stats["personas"].items():
        st.markdown(f"- **{persona}:** {count}")

    st.markdown("---")
    st.markdown("### About")
    st.markdown(
        "This agent adapts its support style based on "
        "your communication pattern. It detects three personas: "
        "**Technical Expert**, **Frustrated User**, "
        "and **Business Executive**."
    )


# ── Helper Functions ─────────────────────────────────────

def get_persona_css_class(persona_label: str) -> str:
    """Map persona label to CSS class."""
    mapping = {
        "Technical Expert": "technical",
        "Frustrated User": "frustrated",
        "Business Executive": "business",
    }
    return mapping.get(persona_label, "technical")


def display_persona_badge(persona_label: str):
    """Display a colored persona badge."""
    css_class = get_persona_css_class(persona_label)
    st.markdown(
        f'<span class="persona-badge persona-{css_class}">'
        f"{persona_label}</span>",
        unsafe_allow_html=True,
    )


def display_metrics(confidence: float, retrieval_score: float, is_escalated: bool):
    """Display metrics in three columns."""
    cols = st.columns(3)
    cols[0].markdown(
        f'<div class="metric-card">'
        f'<div class="metric-value">{confidence:.0%}</div>'
        f'<div class="metric-label">Persona Confidence</div>'
        f"</div>",
        unsafe_allow_html=True,
    )
    cols[1].markdown(
        f'<div class="metric-card">'
        f'<div class="metric-value">{retrieval_score:.3f}</div>'
        f'<div class="metric-label">Retrieval Score</div>'
        f"</div>",
        unsafe_allow_html=True,
    )
    cols[2].markdown(
        f'<div class="metric-card">'
        f'<div class="metric-value">{"Yes" if is_escalated else "No"}</div>'
        f'<div class="metric-label">Escalated</div>'
        f"</div>",
        unsafe_allow_html=True,
    )


def display_sources(sources: list):
    """Display source chips."""
    if sources:
        st.markdown("**Sources:**")
        chips = " ".join(
            f'<span class="source-chip">{s["source"]}</span>'
            for s in sources[:4]
        )
        st.markdown(chips, unsafe_allow_html=True)


# ── Main Chat Interface ──────────────────────────────────

st.title("CloudFlow Support Agent")
st.markdown(
    "*Persona-adaptive AI support with knowledge-grounded responses*"
)

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            display_persona_badge(msg.get("persona", ""))

            if msg.get("is_escalated"):
                st.markdown(
                    '<div class="escalation-banner">'
                    "ESCALATED TO HUMAN AGENT</div>",
                    unsafe_allow_html=True,
                )

            st.markdown(msg["content"])
            display_sources(msg.get("sources"))
            display_metrics(
                msg.get("confidence", 0),
                msg.get("retrieval_score", 0),
                msg.get("is_escalated", False),
            )

            if msg.get("escalation_summary"):
                with st.expander("View Handoff Summary (JSON)"):
                    st.json(msg["escalation_summary"])

# Chat input
if prompt := st.chat_input("Type your support question here..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Process
    agent = load_agent()
    with st.spinner("Analyzing your message..."):
        resp: AgentResponse = agent.chat(
            prompt, session_id=st.session_state.session_id
        )

    # Update stats
    st.session_state.stats["total_queries"] += 1
    st.session_state.stats["personas"][resp.persona_label] = (
        st.session_state.stats["personas"].get(resp.persona_label, 0) + 1
    )
    if resp.is_escalated:
        st.session_state.stats["escalations"] += 1

    # Store assistant message
    assistant_msg = {
        "role": "assistant",
        "content": resp.message,
        "persona": resp.persona_label,
        "confidence": resp.persona_confidence,
        "sources": resp.sources,
        "retrieval_score": resp.retrieval_score,
        "is_escalated": resp.is_escalated,
        "escalation_summary": resp.escalation_summary,
    }
    st.session_state.messages.append(assistant_msg)

    # Display assistant response
    with st.chat_message("assistant"):
        display_persona_badge(resp.persona_label)

        if resp.is_escalated:
            st.markdown(
                '<div class="escalation-banner">'
                "ESCALATED TO HUMAN AGENT</div>",
                unsafe_allow_html=True,
            )

        st.markdown(resp.message)
        display_sources(resp.sources)
        display_metrics(
            resp.persona_confidence,
            resp.retrieval_score,
            resp.is_escalated,
        )

        if resp.escalation_summary:
            with st.expander("View Handoff Summary (JSON)"):
                st.json(resp.escalation_summary)

    st.rerun()