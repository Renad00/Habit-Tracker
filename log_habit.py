
import streamlit as st
import pandas as pd
from datetime import date

st.title("Log Your Daily Habits")

today = date.today()

habits = st.session_state.habits

try:
    completions = pd.read_csv("habit_completions.csv")
except FileNotFoundError:
    completions = pd.DataFrame(
        columns=["habit_name", "date", "completed"]
    )

completions["date"] = completions["date"].astype(str)

# Display active habits
active_habits = habits[
    pd.to_datetime(habits["start_date"]).dt.date <= today
]

st.write(today.strftime("%A, %B %d, %Y"))

if len(active_habits) > 0:

    selected_habits = []

    for index, row in active_habits.iterrows():

        habit = row["habit_name"]
        
        #Check whether the habit was already completed today
        existing = completions[
            (completions["habit_name"] == habit) &
            (completions["date"] == str(today))
        ]

        completed = not existing.empty

        checked = st.checkbox(
            habit,
            value=completed,
            key=f"habit_{index}"
        )

        if checked:
            selected_habits.append(habit)

    if st.button("Complete"):

        for index, row in active_habits.iterrows():

            habit = row["habit_name"]
            
            existing = completions[
                (completions["habit_name"] == habit) &
                (completions["date"] == str(today))
            ]

            if habit in selected_habits:

                if existing.empty:

                    new_record = {
                        "habit_name": habit,
                        "date": today,
                        "completed": True
                    }

                    completions.loc[len(completions)] = new_record

            else:
            
                #If the user unchecked the habit
                completions = completions[
                    ~(
                        (completions["habit_name"] == habit) &
                        (completions["date"] == str(today))
                    )
                ]

        completions.to_csv(
            "habit_completions.csv",
            index=False
        )

        st.success("Your progress has been saved!")

else:
    st.info("You don't have any active habits yet.")
