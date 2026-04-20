import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import webbrowser

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Smart Job System", layout="wide")

# -------------------------------
# LOGIN SYSTEM
# -------------------------------
if "login" not in st.session_state:
    st.session_state["login"] = False

def login():
    st.title("🔐 Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state["login"] = True
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
if not st.session_state["login"]:
    login()

else:
    df = scrape_jobs()

    st.title("💼 Smart Job Management System")

    # -------------------------------
    # SIDEBAR UI
    # -------------------------------
    st.sidebar.title("💼 Menu")

    st.sidebar.markdown("### 🔎 Job Portals")
    st.sidebar.markdown("1. Indeed  \n2. Naukri  \n3. Glassdoor  \n4. Shine")

    st.sidebar.markdown("### 🔍 Job Search")
    st.sidebar.markdown("5. Search Jobs (Google)")

    st.sidebar.markdown("### 📊 Analysis")
    st.sidebar.markdown("6. Show Jobs  \n7. Search Job (Local Data)  \n8. Location Analysis  \n9. Skill Analysis")

    st.sidebar.markdown("### 🎓 Learning Platforms")
    st.sidebar.markdown("10. Coursera  \n11. Udemy  \n12. LinkedIn Learning")

    st.sidebar.markdown("### 📄 Career Tools")
    st.sidebar.markdown("13. Resume Builder  \n14. LinkedIn Profile")

    st.sidebar.markdown("### 🚪 Exit")
    st.sidebar.markdown("15. Exit")

    # -------------------------------
    # INTERACTIVE MENU
    # -------------------------------
    menu = st.sidebar.radio("Select Option", [
        "Indeed",
        "Naukri",
        "Glassdoor",
        "Shine",
        "Search Jobs",
        "Show Jobs",
        "Search (Local)",
        "Location Analysis",
        "Skill Analysis",
        "Coursera",
        "Udemy",
        "LinkedIn Learning",
        "Resume Builder",
        "LinkedIn Profile",
        "Exit"
    ])

    # -------------------------------
    # FUNCTIONALITY
    # -------------------------------
    if menu == "Indeed":
        webbrowser.open("https://in.indeed.com")

    elif menu == "Naukri":
        webbrowser.open("https://www.naukri.com")

    elif menu == "Glassdoor":
        webbrowser.open("https://www.glassdoor.co.in")

    elif menu == "Shine":
        webbrowser.open("https://www.shine.com")

    elif menu == "Search Jobs":
        keyword = st.text_input("Enter job keyword")
        if keyword:
            webbrowser.open(f"https://www.google.com/search?q={keyword}+jobs")

    elif menu == "Show Jobs":
        st.subheader("📋 Job Listings")
        st.dataframe(df)

    elif menu == "Search (Local)":
        keyword = st.text_input("Search jobs")
        if keyword:
            filtered = df[df['title'].str.contains(keyword, case=False)]
            st.dataframe(filtered)

    elif menu == "Location Analysis":
        st.subheader("📍 Location Analysis")
        st.bar_chart(df['location'].value_counts())

    elif menu == "Skill Analysis":
        st.subheader("🧠 Skill Demand")
        skills = ["Python", "Java", "SQL", "Data", "AI"]
        skill_count = {skill: df['title'].str.contains(skill, case=False).sum() for skill in skills}
        st.bar_chart(skill_count)

    elif menu == "Coursera":
        webbrowser.open("https://www.coursera.org")

    elif menu == "Udemy":
        webbrowser.open("https://www.udemy.com")

    elif menu == "LinkedIn Learning":
        webbrowser.open("https://www.linkedin.com/learning")

    elif menu == "Resume Builder":
        webbrowser.open("https://www.canva.com/resumes/")

    elif menu == "LinkedIn Profile":
        webbrowser.open("https://www.linkedin.com")

    elif menu == "Exit":
        st.warning("👋 Exit selected")