import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.express as px
import webbrowser

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Smart Job System", layout="wide")

# -------------------------------
# CUSTOM CSS (DARK UI)
# -------------------------------
st.markdown("""
<style>
body {background-color: #0e1117; color: white;}
[data-testid="stSidebar"] {background-color: #111;}
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    margin: 10px 0;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.6);
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# LOGIN SYSTEM (UI)
# -------------------------------
if "login" not in st.session_state:
    st.session_state.login = False

def login():
    st.markdown("<h2 style='text-align:center;'>🔐 Login</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username == "admin" and password == "1234":
                st.session_state.login = True
            else:
                st.error("Invalid credentials")

# -------------------------------
# SCRAPER
# -------------------------------
def scrape_jobs():
    url = "https://realpython.github.io/fake-jobs/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for card in soup.find_all('div', class_='card-content'):
        title = card.find('h2').text.strip()
        company = card.find('h3').text.strip()
        location = card.find('p').text.strip()

        jobs.append({
            "title": title,
            "company": company,
            "location": location
        })

    return pd.DataFrame(jobs)

# -------------------------------
# MAIN APP
# -------------------------------
if not st.session_state.login:
    login()

else:
    df = scrape_jobs()

    # -------------------------------
    # SIDEBAR NAVIGATION
    # -------------------------------
    st.sidebar.title("💼 Navigation")

    page = st.sidebar.radio("Go to", [
        "Dashboard",
        "Jobs",
        "Analysis",
        "Skills",
        "Quick Links"
    ])

    # -------------------------------
    # DASHBOARD
    # -------------------------------
    if page == "Dashboard":
        st.title("🚀 Smart Job Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.markdown(f"<div class='card'>📊 Total Jobs<br><h2>{len(df)}</h2></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='card'>🏢 Companies<br><h2>{df['company'].nunique()}</h2></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='card'>📍 Locations<br><h2>{df['location'].nunique()}</h2></div>", unsafe_allow_html=True)

        st.subheader("📍 Top Locations")
        fig = px.bar(df['location'].value_counts().head(10),
                     title="Top Job Locations",
                     color=df['location'].value_counts().head(10).values,
                     color_continuous_scale="Blues")
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # JOB PAGE
    # -------------------------------
    elif page == "Jobs":
        st.title("📋 Job Listings")

        keyword = st.text_input("🔍 Search job")

        if keyword:
            filtered = df[df['title'].str.contains(keyword, case=False)]
            st.success(f"{len(filtered)} jobs found")
            st.dataframe(filtered)
        else:
            st.dataframe(df)

    # -------------------------------
    # ANALYSIS PAGE
    # -------------------------------
    elif page == "Analysis":
        st.title("📊 Analysis")

        loc_data = df['location'].value_counts().head(10)

        fig = px.bar(loc_data,
                     title="Location Analysis",
                     color=loc_data.values,
                     color_continuous_scale="Teal")

        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # SKILLS PAGE
    # -------------------------------
    elif page == "Skills":
        st.title("🧠 Skill Demand")

        skills = ["Python", "Java", "SQL", "Data", "AI"]
        skill_count = {skill: df['title'].str.contains(skill, case=False).sum() for skill in skills}

        fig = px.bar(
            x=list(skill_count.keys()),
            y=list(skill_count.values()),
            title="Skill Demand",
            color=list(skill_count.values()),
            color_continuous_scale="Viridis"
        )

        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # LINKS PAGE
    # -------------------------------
    elif page == "Quick Links":
        st.title("🌐 Job & Career Links")

        if st.button("Open Indeed"):
            webbrowser.open("https://in.indeed.com")

        if st.button("Open Naukri"):
            webbrowser.open("https://www.naukri.com")

        if st.button("Open Coursera"):
            webbrowser.open("https://www.coursera.org")

        if st.button("Resume Builder"):
            webbrowser.open("https://www.canva.com/resumes/")
