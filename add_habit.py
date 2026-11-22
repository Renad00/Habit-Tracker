
import streamlit as st
import pandas as pd
from datetime import date

st.title("Add New Habit")
st.write("Create a new habit")

frequency = st.selectbox(
    "Frequency",
    ["Daily", "Weekly"]
)

with st.form("habit_form"):

    habit_name = st.text_input("Habit Name")

    if frequency == "Daily":

        col1, col2 = st.columns(2)

        target_goal = col1.number_input(
            "Target Goal",
            min_value=1,
            value=30
        )

        target_unit = col2.selectbox(
            "Unit",
            ["Minutes", "Hours", "Pages", "Times"]
        )

    else:

        target_goal = st.radio(
            "Target (Days per Week)",
            [1, 2, 3, 4, 5, 6, 7],
            horizontal=True
        )

        target_unit = "Days"

    category = st.selectbox(
        "Category",
        ["Health", "Fitness", "Learning", "Personal", "Other"]
    )

    start_date = st.date_input(
        "Start Date",
        value=date.today()
    )

    submit = st.form_submit_button("Add Habit")


if submit:

    if habit_name.strip() == "":
        st.warning("Please enter a habit name.")

    else:

        # Check for duplicate habit names
        existing_names = st.session_state.habits[
            "habit_name"
        ].str.strip().str.lower()

        new_name = habit_name.strip().lower()

        if new_name in existing_names.values:

            st.warning("This habit already exists!")

        else:

            new_habit = {
                "habit_name": habit_name.strip(),
                "frequency": frequency,
                "target_goal": target_goal,
                "target_unit": target_unit,
                "category": category,
                "start_date": start_date
            }

            st.session_state.habits.loc[
                len(st.session_state.habits)
            ] = new_habit

            st.session_state.habits.to_csv(
                "habits_tracker.csv",
                index=False
            )

            st.success("Habit added successfully!")
