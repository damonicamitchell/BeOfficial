"""
BeOfficial Agents – Streamlit App (app.py)

Production-ready Streamlit app for defining BeOfficial's agent team and exporting
config files. No external network calls; this is an authoring and review tool.

How to run locally:
  1) Save this file as app.py
  2) In a terminal:  streamlit run app.py
"""

from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional
import json
import io
import datetime as dt
import streamlit as st

st.set_page_config(page_title="BeOfficial Agents", page_icon="🧠", layout="wide")

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
# Default Agent Definitions
# =========================

def load_default_agents() -> List[Agent]:
    newsletter_agent = Agent(
        name="Weekly Recruiting Newsletter Writer",
        codename="SCRIBE",
        mission=(
            "Create a weekly email newsletter that recruits college to grad students into officiating. "
            "Show the lifestyle, community, training path, and fast ways to earn paid games."
        ),
        target_audience="Young adults from incoming college freshmen to grad students",
        value_proposition=(
            "A friendly newsletter that explains how to start, highlights role models, and shares gigs, "
            "training dates, and income examples that feel real and reachable."
        ),
        core_tasks=[
            "Draft one newsletter each week with a clear call to action",
            "Feature a weekly story or spotlight that feels relatable",
            "Add a simple step by step to get certified or game ready",
            "Include two or three near term opportunities and a short FAQ",
            "Deliver content that a fifth grader could understand without dumbing it down",
        ],
        inputs=[
            "Editorial calendar themes",
            "Upcoming training, camps, and certification dates",
            "Success stories and quotes",
            "Open roles and sign up links",
            "Brand voice guide",
        ],
        outputs=[
            "HTML and plain text newsletter",
            "Subject line and preview text options",
            "One banner line for cross posting on social platforms",
            "UTM tagged links for tracking",
        ],
        data_sources=[
            "Internal events and camp calendars",
            "League assignors and partner orgs",
            "BeOfficial website and landing pages",
        ],
        kpis=[
            "Open rate and click rate",
            "Number of sign ups and completed interest forms",
            "New officials added to pipeline per week",
        ],
        guardrails=[
            "Keep copy positive and clear",
            "No claims about guaranteed earnings",
            "Respect email compliance and unsubscribe rules",
        ],
        example_prompts=[
            "Write a 500 word newsletter that explains the three steps to work paid fall leagues in 30 days. Include one student spotlight and two dates to register.",
            "Draft three subject lines with a playful tone. Keep preview text under 80 characters.",
        ],
    )

    social_agent = Agent(
        name="Social Media Content Producer",
        codename="SPARK",
        mission=(
            "Plan and create platform ready posts for LinkedIn, Instagram, Facebook, TikTok, and YouTube Shorts "
            "that recruit young adults and show the real day in the life of an official."
        ),
        target_audience="College age and grad students on the above platforms",
        value_proposition=(
            "Consistent short form content that makes officiating look modern, social, and rewarding, with a clear way to start."
        ),
        core_tasks=[
            "Create a weekly content calendar",
            "Write captions, hooks, and on screen scripts",
            "Suggest b roll and shot lists for quick filming",
            "Resize and format assets per platform",
            "Publish or hand off to a scheduler",
        ],
        inputs=[
            "Brand voice, logo, color palette",
            "Footage and photos from games, camps, clinics",
            "Recruiting offers and landing pages",
            "Key dates from the editorial calendar",
        ],
        outputs=[
            "7 to 10 short posts per week with captions",
            "Two 30 to 45 second TikTok or Reels scripts per week",
            "One 60 to 90 second YouTube Short per week",
            "Hashtag clusters by platform",
        ],
        data_sources=[
            "Internal footage library",
            "User generated content with permission",
            "Trending audio guidelines by platform",
        ],
        kpis=[
            "Follows, saves, and shares",
            "Click throughs to sign up pages",
            "Number of interest forms from social",
        ],
        guardrails=[
            "No game footage without league permission",
            "Protect minors and follow platform safety rules",
            "Do not disparage other officials or teams",
        ],
        example_prompts=[
            "Write a 20 second TikTok hook that shows how to earn weekend cash reffing youth tournaments. End with a single call to action.",
            "Draft LinkedIn copy that focuses on leadership and conflict resolution skills you build as an official.",
        ],
    )

    news_monitor_agent = Agent(
        name="Referee News Monitor",
        codename="EARLYBIRD",
        mission=(
            "Gather and summarize daily referee industry news and deliver a 5:30 am digest email with links."
        ),
        target_audience="Vernon and BeOfficial leadership",
        value_proposition=(
            "One concise morning brief that saves time and keeps strategy current on rules, safety, tech, and training."
        ),
        core_tasks=[
            "Scan key sources and saved searches",
            "Extract three to five high value items",
            "Summarize in plain language with one line why it matters",
            "Package for delivery at 5:30 am Central",
        ],
        inputs=[
            "Source list and keywords",
            "Relevance criteria and topics to track",
            "Contact list for delivery",
        ],
        outputs=[
            "Daily email brief",
            "Weekly roll up with trends",
            "CSV archive of links and tags",
        ],
        data_sources=[
            "referee.com",
            "naso.org",
            "nfhs.org",
            "Saved Google News queries",
        ],
        kpis=[
            "Brief sent on time",
            "Number of relevant items per week",
            "Click throughs on links in brief",
        ],
        guardrails=[
            "Respect robots.txt and site terms in the future build",
            "Quote snippets only and link out",
            "Avoid paywalled content unless licensed",
        ],
        notes=(
            "Future build can use a news API or polite scraping with caching. Scheduling handled by cron or automation platform."
        ),
        example_prompts=[
            "Summarize the new NFHS guidance on concussion protocols in two sentences and explain how it impacts youth basketball assignors.",
        ],
    )

    leadgen_agent = Agent(
        name="Email List Builder and Lead Generator",
        codename="MAGNET",
        mission=(
            "Grow a qualified email list of college to grad students interested in officiating and nurture them to sign up."
        ),
        target_audience="Students ages 18 to 28 in target schools and cities",
        value_proposition=(
            "Lead magnets and landing pages that convert with simple steps to get on the floor fast."
        ),
        core_tasks=[
            "Design landing pages with a two step form",
            "Create two lead magnets such as Starter Guide and Game Day Checklist",
            "Set up tagging and segments by city and sport",
            "Run small budget test campaigns and report",
        ],
        inputs=[
            "Email platform access",
            "Brand assets",
            "Offer details and training dates",
        ],
        outputs=[
            "List growth report by week",
            "Segmented CSV exports",
            "Two downloadable PDFs as magnets",
        ],
        data_sources=[
            "Form submissions",
            "Ad platform metrics",
            "Campus partner lists where allowed",
        ],
        kpis=[
            "Subscribers per week",
            "Cost per lead where ads run",
            "Conversion to interest call or training sign up",
        ],
        guardrails=[
            "Follow email and privacy laws",
            "Use opt in and provide unsubscribe",
            "No purchasing third party student lists",
        ],
        example_prompts=[
            "Write a landing page hero that promises a first paid game in 30 days with honest language and no hype.",
            "Draft a 2 page Starter Guide outline for new officials with the first three steps to take this week.",
        ],
    )

    coordinator_agent = Agent(
        name="Tournament Scouting and Day Of Coordinator",
        codename="RALLY",
        mission=(
            "Scout tournament sites, collect operations details, and prepare run of show plans. On event days provide checklists and live rosters so crews are on time and covered."
        ),
        target_audience="Tournament directors, assignors, crew chiefs, and officials",
        value_proposition=(
            "A single source of truth for who, where, and when with backups and escalation paths."
        ),
        core_tasks=[
            "Review tournament websites and gather dates, locations, contact info",
            "Build crew rosters and court assignments",
            "Create a run of show timeline and communication tree",
            "Publish a day of dashboard with live status and replacements",
        ],
        inputs=[
            "Tournament URLs and PDFs",
            "Referee availability and cert levels",
            "Venue maps and parking notes",
        ],
        outputs=[
            "Scouting brief per tournament",
            "Staffing plan and court grid",
            "Day of checklist and escalation plan",
        ],
        data_sources=[
            "Public tournament sites",
            "Internal roster database",
            "Maps and traffic tools",
        ],
        kpis=[
            "On time start percentage",
            "Coverage rate with no court left unstaffed",
            "Swap resolution time",
        ],
        guardrails=[
            "Respect tournament brand and requests",
            "Do not publish personal data outside the team",
            "Confirm last minute changes with site leads",
        ],
        example_prompts=[
            "Extract dates, venue, and contact info from this tournament site and build a one page scouting brief.",
            "Generate a court by court schedule from 8 am to 8 pm with three officials per game and 10 minute changeover windows.",
        ],
    )

    return [newsletter_agent, social_agent, news_monitor_agent, leadgen_agent, coordinator_agent]


# =========================
# Utilities
# =========================

def _download_bytes(name: str, data: bytes):
    st.download_button(
        label=f"⬇️ Download {name}",
        data=data,
        file_name=name,
        mime="application/json" if name.endswith(".json") else "text/plain",
        use_container_width=True,
    )


def export_agents_json(agents: List[Agent]):
    payload = {
        "exported_at": dt.datetime.now().isoformat(),
        "project": "BeOfficial",
        "agents": [a.to_dict() for a in agents],
    }
    buf = json.dumps(payload, indent=2).encode("utf-8")
    _download_bytes("beofficial_agents.json", buf)


def email_preview(subject: str, intro: str, bullets: List[str], footer: str) -> str:
    body = [
        f"Subject: {subject}",
        "",
        intro,
        "",
        *[f"• {b}" for b in bullets],
        "",
        footer,
    ]
    return "
".join(body)


# =========================
# App UI
# =========================

if "agents" not in st.session_state:
    st.session_state.agents: List[Agent] = load_default_agents()

AGENTS = st.session_state.agents

st.title("BeOfficial Agent Team")

st.caption(
    "Define, edit, and export agent profiles for recruiting, social content, industry news, lead gen, and tournament coordination."
)

# ---- Sidebar ----
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Overview",
        "Agents",
        "EARLYBIRD – Email Digest Preview",
        "SPARK – Content Calendar",
        "Export",
    ],
)

st.sidebar.divider()
st.sidebar.subheader("Quick Settings")
st.sidebar.text_input("Brand Voice Notes", value="Friendly, clear, energetic, zero fluff")
st.sidebar.text_input("Primary CTA URL", value="https://beofficial.example.com/start")

# ---- Overview ----
if page == "Overview":
    st.subheader("Quick Overview")
    st.table(
        {
            "Agent": [a.name for a in AGENTS],
            "Codename": [a.codename for a in AGENTS],
            "Primary KPI": [a.kpis[0] for a in AGENTS],
            "Primary Output": [a.outputs[0] for a in AGENTS],
        }
    )

    st.info(
        "Tip: Start with two KPIs per agent for Month 1. Example: SCRIBE focuses on Open Rate and Sign Ups."
    )

# ---- Agents ----
elif page == "Agents":
    st.subheader("Agent Profiles")

    tabs = st.tabs([a.codename for a in AGENTS])
    for tab, agent in zip(tabs, AGENTS):
        with tab:
            with st.container(border=True):
                left, right = st.columns([1.2, 1])
                with left:
                    st.markdown(f"### {agent.name}
**Codename:** `{agent.codename}`")
                    agent.mission = st.text_area(
                        "Mission", value=agent.mission, height=100, key=f"ms_{agent.codename}"
                    )
                    agent.target_audience = st.text_input(
                        "Target audience", value=agent.target_audience, key=f"ta_{agent.codename}"
                    )
                    agent.value_proposition = st.text_area(
                        "Value proposition", value=agent.value_proposition, height=90, key=f"vp_{agent.codename}"
                    )
                with right:
                    st.markdown("**KPIs**")
                    kpi_edit = st.experimental_data_editor(
                        {"KPIs": agent.kpis}, num_rows="dynamic", key=f"kpi_{agent.codename}"
                    )
                    agent.kpis = [k for k in kpi_edit["KPIs"] if k]

                cols = st.columns(2)
                with cols[0]:
                    st.markdown("**Core tasks**")
                    core_edit = st.experimental_data_editor(
                        {"Tasks": agent.core_tasks}, num_rows="dynamic", key=f"core_{agent.codename}"
                    )
                    agent.core_tasks = [t for t in core_edit["Tasks"] if t]

                    st.markdown("**Inputs**")
                    inp_edit = st.experimental_data_editor(
                        {"Inputs": agent.inputs}, num_rows="dynamic", key=f"inp_{agent.codename}"
                    )
                    agent.inputs = [i for i in inp_edit["Inputs"] if i]

                    st.markdown("**Outputs**")
                    out_edit = st.experimental_data_editor(
                        {"Outputs": agent.outputs}, num_rows="dynamic", key=f"out_{agent.codename}"
                    )
                    agent.outputs = [o for o in out_edit["Outputs"] if o]

                with cols[1]:
                    st.markdown("**Data sources**")
                    src_edit = st.experimental_data_editor(
                        {"Sources": agent.data_sources}, num_rows="dynamic", key=f"src_{agent.codename}"
                    )
                    agent.data_sources = [s for s in src_edit["Sources"] if s]

                    st.markdown("**Guardrails**")
                    grd_edit = st.experimental_data_editor(
                        {"Rules": agent.guardrails}, num_rows="dynamic", key=f"grd_{agent.codename}"
                    )
                    agent.guardrails = [g for g in grd_edit["Rules"] if g]

                if agent.example_prompts:
                    st.markdown("**Example prompts**")
                    for p in agent.example_prompts:
                        st.code(p, language="text")

                agent.notes = st.text_area(
                    "Implementation notes (optional)", value=agent.notes or "", key=f"nt_{agent.codename}"
                )

                st.success("Changes are saved in-session. Use Export to download JSON.")

# ---- EARLYBIRD – Email Digest Preview ----
elif page == "EARLYBIRD – Email Digest Preview":
    st.subheader("5:30 am Daily Brief – Preview")
    col1, col2 = st.columns([1, 1])

    with col1:
        subject = st.text_input("Subject", value="Referee Daily Brief – Mon")
        intro = st.text_area(
            "Intro", value=(
                "Good morning! Here are the top items for officials and assignors. Each has a one line take on why it matters."
            ), height=90
        )
        bullets = st.experimental_data_editor(
            {"Items": [
                "NFHS updates guidance on concussion protocols; assignors should review pregame checklist.",
                "Referee.com feature on conflict de escalation – great for preseason training decks.",
                "NISOA adds spring clinic dates; consider cross posting for college refs.",
            ]}, num_rows="dynamic"
        )
        footer = st.text_input(
            "Footer", value="Reply with topics you want tracked. BeOfficial · EarlyBird"
        )

    with col2:
        preview = email_preview(
            subject=subject,
            intro=intro,
            bullets=[x for x in bullets["Items"] if x],
            footer=footer,
        )
        st.markdown("**Preview (plain text)**")
        st.code(preview, language="text")

    st.info("This is a composition view only. Actual fetching and delivery will be added later.")

# ---- SPARK – Content Calendar ----
elif page == "SPARK – Content Calendar":
    st.subheader("One Week Content Calendar")

    default_calendar = [
        {"Day": "Mon", "Platform": "TikTok", "Concept": "Weekend cash: 3 step start", "CTA": "Join interest list"},
        {"Day": "Tue", "Platform": "Instagram", "Concept": "UGC: first uniform try on", "CTA": "Free Starter Guide"},
        {"Day": "Wed", "Platform": "YouTube Short", "Concept": "Signals 101 in 45s", "CTA": "Clinic signup"},
        {"Day": "Thu", "Platform": "LinkedIn", "Concept": "Leadership you gain officiating", "CTA": "Info call"},
        {"Day": "Fri", "Platform": "Facebook", "Concept": "Myth busting: you need D1 skills?", "CTA": "Start local"},
        {"Day": "Sat", "Platform": "TikTok", "Concept": "Game day bag checklist", "CTA": "Download PDF"},
        {"Day": "Sun", "Platform": "Instagram", "Concept": "Spotlight: student official", "CTA": "Apply for fall league"},
    ]

    cal = st.experimental_data_editor(
        {
            "Day": [r["Day"] for r in default_calendar],
            "Platform": [r["Platform"] for r in default_calendar],
            "Concept": [r["Concept"] for r in default_calendar],
            "CTA": [r["CTA"] for r in default_calendar],
        }, num_rows="dynamic"
    )

    output_rows = []
    for i in range(len(cal["Day"])):
        row = {
            "Day": cal["Day"][i],
            "Platform": cal["Platform"][i],
            "Concept": cal["Concept"][i],
            "CTA": cal["CTA"][i],
        }
        if any(row.values()):
            output_rows.append(row)

    if output_rows:
        buf = json.dumps({"calendar": output_rows}, indent=2).encode("utf-8")
        _download_bytes("spark_content_calendar.json", buf)
        st.success("Calendar ready. Download JSON above.")

# ---- Export ----
elif page == "Export":
    st.subheader("Export Project Files")

    colA, colB = st.columns([1, 1])
    with colA:
        st.markdown("**Agents JSON**")
        export_agents_json(AGENTS)

    with colB:
        st.markdown("**README notes**")
        readme = (
            "BeOfficial Agents configuration exported from Streamlit.

"
            "Files: beofficial_agents.json (agents), spark_content_calendar.json (optional).
"
            "Next: connect automations for news fetching, email delivery, social scheduling, and day-of dashboards."
        )
        _download_bytes("README_beofficial.txt", readme.encode("utf-8"))

    st.info("Keep this JSON under version control so changes to agents are tracked over time.")
