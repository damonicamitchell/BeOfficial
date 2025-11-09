"""
BeOfficial Agents – Streamlit App (app.py)
Command-center style Streamlit app for BeOfficial's agent team.
Includes a dashboard, agent profiles, EARLYBIRD email preview, and Send Test Email.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional
import json
import datetime as dt
import streamlit as st
import os
import smtplib
import ssl
from email.message import EmailMessage

st.set_page_config(page_title="BeOfficial Command Center", page_icon="🏀", layout="wide")

# =========================
# Data Models
# =========================
@dataclass
class Agent:
    name: str
    codename: str
    mission: str
    target_audience: str
    value_proposition: str
    core_tasks: List[str]
    inputs: List[str]
    outputs: List[str]
    data_sources: List[str]
    kpis: List[str]
    guardrails: List[str]
    notes: Optional[str] = None
    example_prompts: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return asdict(self)


# =========================
# Utility Functions
# =========================
def email_preview(subject: str, intro: str, bullets: List[str], footer: str) -> str:
    """Create a formatted plain text email preview."""
    body = [
        f"Subject: {subject}",
        "",
        intro,
        "",
        *[f"• {b}" for b in bullets if b.strip()],
        "",
        footer,
    ]
    return "\n".join(body)  # ✅ fixed string literal


def send_email(to_email: str, subject: str, body: str) -> str:
    """Send email via SMTP using environment variables."""
    required = ["SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS", "SMTP_FROM"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        return f"Missing environment variables: {', '.join(missing)}"

    host = os.environ["SMTP_HOST"]
    port = int(os.environ["SMTP_PORT"])
    user = os.environ["SMTP_USER"]
    pwd = os.environ["SMTP_PASS"]
    from_email = os.environ["SMTP_FROM"]

    msg = EmailMessage()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(host, port) as server:
            server.starttls(context=context)
            server.login(user, pwd)
            server.send_message(msg)
        return "OK"
    except Exception as e:
        return f"Error: {e}"


def export_agents_json(agents: List[Agent]):
    payload = {
        "exported_at": dt.datetime.now().isoformat(),
        "project": "BeOfficial",
        "agents": [a.to_dict() for a in agents],
    }
    st.download_button(
        label="⬇️ Download beofficial_agents.json",
        data=json.dumps(payload, indent=2),
        file_name="beofficial_agents.json",
        mime="application/json",
        use_container_width=True,
    )


def kpi_badge(text: str):
    st.markdown(
        f"""
        <div style='display:inline-block;padding:6px 10px;border-radius:999px;background:#F1F5F9;font-weight:600;'>
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================
# Agent Definitions
# =========================
def load_default_agents() -> List[Agent]:
    return [
        Agent(
            name="Weekly Recruiting Newsletter Writer",
            codename="SCRIBE",
            mission="Create weekly newsletters to recruit college and grad students into officiating.",
            target_audience="College and grad students",
            value_proposition="Friendly, clear newsletters that highlight success stories and opportunities.",
            core_tasks=[
                "Draft newsletter weekly",
                "Add spotlight stories",
                "Include signup and CTA links",
            ],
            inputs=["Training schedules", "Event list", "Quotes"],
            outputs=["Newsletter email", "Subject lines", "Banner line"],
            data_sources=["Internal events", "BeOfficial site"],
            kpis=["Open rate", "Clicks"],
            guardrails=["Positive tone", "No false claims"],
        ),
        Agent(
            name="Social Media Content Producer",
            codename="SPARK",
            mission="Create social content to attract young officials.",
            target_audience="18–28 on social platforms",
            value_proposition="Short-form videos that make officiating look modern and rewarding.",
            core_tasks=[
                "Plan content calendar",
                "Write captions",
                "Produce Reels and Shorts",
            ],
            inputs=["Footage", "Brand voice", "Dates"],
            outputs=["10 posts weekly", "Scripts", "Captions"],
            data_sources=["UGC library"],
            kpis=["Followers", "Leads"],
            guardrails=["Protect minors", "No unauthorized footage"],
        ),
        Agent(
            name="Referee News Monitor",
            codename="EARLYBIRD",
            mission="Deliver 5:30am daily briefs on referee industry updates.",
            target_audience="Vernon and BeOfficial leadership",
            value_proposition="One concise morning brief that saves time and keeps you informed.",
            core_tasks=["Scan key sources", "Summarize top news", "Send digest"],
            inputs=["News feeds", "Referee sites"],
            outputs=["Daily email brief"],
            data_sources=["referee.com", "naso.org", "nfhs.org"],
            kpis=["On-time send rate"],
            guardrails=["Cite all sources", "No paywalled text"],
        ),
        Agent(
            name="Email List Builder and Lead Generator",
            codename="MAGNET",
            mission="Build email lists of college students and convert them into new referees.",
            target_audience="Students 18–28",
            value_proposition="Lead magnets and landing pages that convert with ease.",
            core_tasks=["Create landing pages", "Design lead magnets"],
            inputs=["Offers", "Design assets"],
            outputs=["Leads list", "Conversion report"],
            data_sources=["Form submissions"],
            kpis=["Subscribers", "Conversion rate"],
            guardrails=["Privacy compliance"],
        ),
        Agent(
            name="Tournament Scouting and Day Of Coordinator",
            codename="RALLY",
            mission="Coordinate referees for tournaments and ensure coverage.",
            target_audience="Tournament directors, officials",
            value_proposition="Reliable operations plan that keeps events on time.",
            core_tasks=["Build rosters", "Confirm venues", "Monitor check-ins"],
            inputs=["Tournament URLs", "Staff availability"],
            outputs=["Coverage plan", "Run of show"],
            data_sources=["Public sites"],
            kpis=["Coverage %"],
            guardrails=["Confirm final schedule with leads"],
        ),
    ]


# =========================
# App State
# =========================
if "agents" not in st.session_state:
    st.session_state.agents = load_default_agents()

AGENTS = st.session_state.agents

# =========================
# Navigation
# =========================
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Agents", "EARLYBIRD – Email Digest Preview", "Send Test Email", "Export"],
)

# =========================
# Dashboard
# =========================
if page == "Dashboard":
    st.title("🏀 BeOfficial Command Center")
    st.caption("View what each agent is doing and track progress.")
    for agent in AGENTS:
        with st.expander(f"{agent.name} ({agent.codename})"):
            st.write(agent.mission)
            st.write("**Outputs:**", ", ".join(agent.outputs))
            st.write("**KPIs:**", ", ".join(agent.kpis))
            st.write("**Next Action:** TBD")

# =========================
# EARLYBIRD Preview
# =========================
elif page == "EARLYBIRD – Email Digest Preview":
    st.subheader("5:30am Daily Brief – Preview")
    subject = st.text_input("Subject", "Referee Daily Brief – Monday")
    intro = st.text_area("Intro", "Good morning! Here are the top items for officials today.")
    items = st.text_area("Items (one per line)", "NFHS rule changes\nNew training camps\nFeature: Official of the Week")
    footer = st.text_input("Footer", "Reply with topics you want tracked. BeOfficial · EarlyBird")
    preview = email_preview(subject, intro, items.splitlines(), footer)
    st.code(preview, language="text")

# =========================
# Send Test Email
# =========================
elif page == "Send Test Email":
    st.subheader("Send Test Email")
    st.caption("Send a one-time test of the EARLYBIRD brief via SMTP.")
    default_subject = "Referee Daily Brief – Test"
    default_body = email_preview(
        subject=default_subject,
        intro="Good morning! Sample items below.",
        bullets=[
            "NFHS clarifies basketball emphasis.",
            "Referee.com article on leadership.",
            "Local clinic updates posted.",
        ],
        footer="Reply with topics you want tracked. BeOfficial · EarlyBird",
    )

    with st.form("send_form"):
        to_email = st.text_input("To", value="vernon.crumpjr@be0fficial.com")
        subject = st.text_input("Subject", value=default_subject)
        body = st.text_area("Body", value=default_body, height=240)
        submitted = st.form_submit_button("Send Email Now")

    if submitted:
        status = send_email(to_email, subject, body)
        if status == "OK":
            st.success(f"Email sent successfully to {to_email}")
        else:
            st.error(status)

    st.markdown("**SMTP Environment Variables Example (for Gmail)**")
    st.code(
        """export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your_gmail_username
export SMTP_PASS=your_app_password
export SMTP_FROM="BeOfficial EarlyBird <your_gmail_username@gmail.com>"
""",
        language="bash",
    )

# =========================
# Agents Page
# =========================
elif page == "Agents":
    st.subheader("Agent Profiles")
    for a in AGENTS:
        with st.expander(f"{a.name} ({a.codename})"):
            st.write(a.to_dict())

# =========================
# Export
# =========================
elif page == "Export":
    st.subheader("Export Project Files")
    export_agents_json(AGENTS)
