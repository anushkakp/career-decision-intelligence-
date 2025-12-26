import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pycountry
import time

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Career Decision Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# GLOBAL CSS – CLASSY ENTERPRISE STYLE + MOTION
# =====================================================
st.markdown("""
<style>
.stApp { background-color:#0B1120; }

h1,h2,h3,h4 { color:#F9FAFB; }
p,label,span { color:#CBD5E1; }

section[data-testid="stSidebar"] { background-color:#020617; }

/* Page transition */
.main > div {
    animation: pageFade 0.6s ease-in-out;
}

@keyframes pageFade {
    from { opacity:0; transform:translateY(8px); }
    to { opacity:1; transform:translateY(0); }
}

/* Hero animation */
.hero {
    animation: heroSlide 0.9s ease-out;
}

@keyframes heroSlide {
    from { opacity:0; transform:translateY(24px); }
    to { opacity:1; transform:translateY(0); }
}

.card {
    background:#020617;
    border-radius:22px;
    padding:24px;
    border:1px solid #1E293B;
    margin-bottom:18px;
    transition: all 0.25s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.35);
}

.kpi {
    background:#020617;
    border-radius:20px;
    padding:20px;
    border:1px solid #1E293B;
    text-align:center;
}

.stButton>button {
    background:linear-gradient(90deg,#2563EB,#4F46E5);
    color:white;
    border-radius:14px;
    font-weight:600;
    border:none;
    padding:12px 20px;
    transition: all 0.2s ease;
}

.stButton>button:hover {
    transform: scale(1.03);
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# DATA
# =====================================================
job_domains = {
    "Technology": ["Software Engineer", "Data Scientist", "ML Engineer"],
    "Finance": ["Financial Analyst", "Accountant"],
    "Healthcare": ["Doctor", "Nurse"],
    "Business": ["Product Manager", "Business Analyst"],
    "Design": ["UI/UX Designer"],
    "Government": ["Civil Servant"]
}

ALL_JOBS = sorted([j for v in job_domains.values() for j in v])
ALL_COUNTRIES = sorted([c.name for c in pycountry.countries])

np.random.seed(7)

# Job-level base metrics (global averages)
job_salary = {j: np.random.randint(8, 20) for j in ALL_JOBS}   # LPA
job_growth = {j: round(np.random.uniform(0.65, 0.9), 2) for j in ALL_JOBS}

# Country-level deterministic factors
country_salary_factor = {}
country_growth_factor = {}

for c in ALL_COUNTRIES:
    base = (abs(hash(c)) % 100) / 100
    country_salary_factor[c] = round(0.75 + base * 0.9, 2)
    country_growth_factor[c] = round(0.85 + base * 0.3, 2)

country_cost = {c: np.random.randint(40, 85) for c in ALL_COUNTRIES}
country_life = {c: round(np.random.uniform(6.0, 8.8), 1) for c in ALL_COUNTRIES}

# =====================================================
# CORE LOGIC (FIXED & LOGICAL)
# =====================================================
def simulate(job, country, risk):

    growth = round(
        job_growth[job] * country_growth_factor[country] * 100, 1
    )

    salary = round(
        job_salary[job] * country_salary_factor[country], 1
    )

    lifestyle = country_life[country]
    cost = country_cost[country]

    stress = round((cost / 100) * (1 - risk), 2)

    score = round(
        (0.4 * growth) +
        (0.3 * lifestyle * 10) -
        (0.3 * stress * 100),
        1
    )

    return growth, salary, lifestyle, stress, score

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================
st.sidebar.title("Career Intelligence")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Simulator", "Insights", "Executive Summary", "About"]
)

# =====================================================
# DASHBOARD (UNCHANGED + MOTION)
# =====================================================
if page == "Dashboard":

    st.markdown("""
    <div class="card hero">
        <h1>Career Decision Intelligence</h1>
        <p>
        A data-driven platform designed to support career and
        relocation decisions using AI-powered evaluation models.
        </p>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(0.2)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='kpi'><h2>Global Coverage</h2><p>All countries supported</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='kpi'><h2>Multi-Domain Careers</h2><p>Across major industries</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='kpi'><h2>Decision Intelligence</h2><p>AI-based scoring</p></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>Careers as Dynamic Systems</h3>
        <p>
        Careers evolve based on market demand, geography,
        lifestyle factors, and individual risk tolerance.
        This platform models these variables holistically.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# SIMULATOR
# =====================================================
elif page == "Simulator":

    st.markdown("<h1>Career & Country Simulator</h1>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        job = st.selectbox("Job Role", ALL_JOBS)
    with c2:
        risk_label = st.select_slider("Risk Tolerance", ["Low", "Medium", "High"])
    with c3:
        countries = st.multiselect(
            "Compare Countries (2–3)",
            ALL_COUNTRIES,
            default=["Canada", "Germany"],
            max_selections=3
        )

    risk_map = {"Low": 0.3, "Medium": 0.6, "High": 0.9}
    risk = risk_map[risk_label]

    if st.button("Run Simulation"):
        st.session_state["job"] = job
        st.session_state["results"] = {
            c: simulate(job, c, risk) for c in countries
        }

    if "results" in st.session_state:
        cols = st.columns(len(st.session_state["results"]))
        for col, (country, r) in zip(cols, st.session_state["results"].items()):
            with col:
                st.markdown(f"""
                <div class="card">
                    <h3>{country}</h3>
                    <p>Career Growth: <b>{r[0]}%</b></p>
                    <p>Average Salary: <b>{r[1]} LPA</b></p>
                    <p>Lifestyle Index: <b>{r[2]}/10</b></p>
                    <p>Stress Risk: <b>{round(r[3]*100,1)}%</b></p>
                    <p><b>Decision Score: {r[4]}/100</b></p>
                </div>
                """, unsafe_allow_html=True)

# =====================================================
# INSIGHTS (UNCHANGED STYLE)
# =====================================================
elif page == "Insights":

    if "results" not in st.session_state:
        st.warning("Run a simulation first.")
    else:
        results = st.session_state["results"]

        fig, ax = plt.subplots(figsize=(9,4), facecolor="#020617")
        ax.set_facecolor("#020617")

        labels = ["Growth", "Salary", "Lifestyle", "Stress"]

        for country, r in results.items():
            ax.plot(
                labels,
                [r[0], r[1], r[2]*10, r[3]*100],
                marker="o",
                linewidth=2.5,
                label=country
            )

        ax.set_title("Career Decision Comparison", color="white")
        ax.tick_params(colors="white")
        for spine in ax.spines.values():
            spine.set_color("#334155")

        ax.legend(facecolor="#020617", edgecolor="#334155", labelcolor="white")
        ax.grid(alpha=0.2)
        st.pyplot(fig)

# =====================================================
# EXECUTIVE SUMMARY (UNCHANGED + CLASSY)
# =====================================================
elif page == "Executive Summary":

    if "results" not in st.session_state:
        st.warning("Run a simulation first.")
    else:
        job = st.session_state["job"]
        results = st.session_state["results"]

        ranked = sorted(results.items(), key=lambda x: x[1][4], reverse=True)
        best = ranked[0]

        st.markdown(f"""
        <div class="card hero">
            <h2>Recommended Option</h2>
            <p>
            For the role of <b>{job}</b>, the most balanced option is:
            </p>
            <h2>{best[0]}</h2>
            <p>Overall Decision Score: <b>{best[1][4]}</b></p>
        </div>
        """, unsafe_allow_html=True)

        for idx, (country, r) in enumerate(ranked, start=1):
            st.markdown(f"""
            <div class="card">
                {idx}. {country} — Score: {r[4]}
            </div>
            """, unsafe_allow_html=True)

# =====================================================
# ABOUT
# =====================================================
elif page == "About":

    st.markdown("""
    <div class="card">
        <h2>About This Platform</h2>
        <p>
        This platform demonstrates how decision intelligence
        can be applied to complex career and relocation choices.
        </p>
        <p>
        Technology Stack: Python, Streamlit, Data Analytics, UX Design
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    "<center style='color:#64748B'>Confidential — Career Decision Intelligence Platform</center>",
    unsafe_allow_html=True
)
