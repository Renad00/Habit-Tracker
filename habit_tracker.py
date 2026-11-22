import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Habit Tracker",
    page_icon="",
    layout="wide",
)



st.markdown("""
<style>

/* ===== Main Background ===== */
.stApp {
    background-color: #F8F3EC;
    color: #493629;
}

/* ===== Sidebar ===== */
[data-testid="stSidebar"] {
    background-color: #E9DDCE;
}

/* ===== Headings ===== */
h1, h2, h3 {
    color: #604735;
}

/* ===== Bold Text ===== */
strong, b {
    color: #604735;
}

/* ===== Regular Text ===== */
.stApp p,
.stApp label {
    color: #574435;
}

/* ===== Buttons ===== */
.stButton > button {
    background-color: #B99A7B;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 7px 18px;
    transition: 0.2s;
}

.stButton > button:hover {
    background-color: #A68768;
    color: white;
    border: none;
}

/* ===== Metric Cards ===== */
[data-testid="stMetric"] {
    background-color: #EFE4D6;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #DFCEBB;
    box-shadow: 0 2px 6px rgba(96, 71, 53, 0.08);
}

/* Metric Labels */
[data-testid="stMetricLabel"] {
    color: #79583F;
}

/* Metric Values */
[data-testid="stMetricValue"] {
    color: #604735;
}

/* ===== Input Fields ===== */
.stTextInput input,
.stNumberInput input,
.stDateInput input {
    background-color: #FFFCF8;
    border-radius: 8px;
    border: 1px solid #D5C1AC;
}

/* ===== Select Boxes ===== */
.stSelectbox div[data-baseweb="select"] {
    background-color: #FFFCF8;
    border-radius: 8px;
}

/* ===== Progress Bar ===== */
.stProgress > div > div > div {
    background-color: #79583F;
}

/* ===== Dataframes ===== */
[data-testid="stDataFrame"] {
    border: 1px solid #DFCEBB;
    border-radius: 10px;
}

/* ===== Success Messages ===== */
[data-testid="stAlert"][kind="success"] {
    background-color: #E8EDE2;
    border: 1px solid #C8D2BE;
    border-radius: 10px;
}

/* ===== Info Messages ===== */
[data-testid="stAlert"][kind="info"] {
    background-color: #F1E9DE;
    border: 1px solid #DFCEBB;
    border-radius: 10px;
}

/* ===== Warning Messages ===== */
[data-testid="stAlert"][kind="warning"] {
    background-color: #F5EBDD;
    border: 1px solid #E5D0AD;
    border-radius: 10px;
}

/* ===== Error Messages ===== */
[data-testid="stAlert"][kind="error"] {
    background-color: #F4E5E1;
    border: 1px solid #DFC2B9;
    border-radius: 10px;
}

/* ===== Dividers ===== */
hr {
    border-color: #DFCEBB;
}
/* Better Metric Cards */
[data-testid="stMetric"] {
    background-color: #EFE4D6 !important;
    border: 1px solid #DFCEBB !important;
    border-radius: 14px !important;
    padding: 22px !important;
    box-shadow: 0px 3px 8px rgba(96, 71, 53, 0.10) !important;
    min-height: 110px;
}

/* Metric Labels */
[data-testid="stMetricLabel"] {
    color: #79583F !important;
}

/* Metric Values */
[data-testid="stMetricValue"] {
    color: #604735 !important;
    font-weight: 700 !important;
}

</style>
""", unsafe_allow_html=True)

if "habits" not in st.session_state:
    st.session_state.habits = pd.read_csv("habits_tracker.csv")


add_habit = st.Page("add_habit.py", title="Add Habits", icon="",)
log_habit = st.Page("log_habit.py", title="Log Habit", icon="")
my_progress = st.Page("my_progress.py", title="My Progress", icon="")
manage_habits = st.Page("manage_habits.py", title="Manage Habits", icon="")
rewards = st.Page("rewards.py", title="My Rewards", icon="🏆")

pg = st.navigation([add_habit, log_habit, my_progress, manage_habits, rewards])
pg.run()






