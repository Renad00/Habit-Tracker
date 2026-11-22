
import streamlit as st
import pandas as pd

st.title("Manage Habits")


habits = st.session_state.habits

if len(habits) > 0:

    st.subheader("Your Habits")

    st.dataframe(habits, hide_index=True)

    habit_names = habits["habit_name"].tolist()

    selected_habit = st.selectbox(
        "Select a habit",
        habit_names
    )

    habit_index = habits[habits["habit_name"] == selected_habit].index[0]

    st.subheader("Edit Habit")

    habit_name = st.text_input(
        "Habit Name",
        value=habits.loc[habit_index, "habit_name"]
    )

    frequency = st.selectbox(
        "Frequency",
        ["Daily", "Weekly"],
        index=["Daily", "Weekly"].index(
            habits.loc[habit_index, "frequency"]
        )
    )

    target_goal = st.number_input(
        "Target Goal",
        min_value=1,
        value=int(habits.loc[habit_index, "target_goal"])
    )

    target_unit = st.selectbox(
        "Unit",
        ["Minutes", "Hours", "Pages", "Times", "Days"],
        index=["Minutes", "Hours", "Pages", "Times", "Days"].index(
            habits.loc[habit_index, "target_unit"]
        )
    )

    category = st.selectbox(
        "Category",
        ["Health", "Fitness", "Learning", "Personal", "Other"],
        index=["Health", "Fitness", "Learning", "Personal", "Other"].index(
            habits.loc[habit_index, "category"]
        )
    )

    start_date = st.date_input(
        "Start Date",
        value=pd.to_datetime(
            habits.loc[habit_index, "start_date"]
        ).date()
    )

    if st.button("Save Changes"):

        if habit_name.strip() == "":
            st.warning("Please enter a habit name.")

        else:
            old_habit_name = habits.loc[habit_index, "habit_name"]

            st.session_state.habits.loc[habit_index] = {
                "habit_name": habit_name,
                "frequency": frequency,
                "target_goal": target_goal,
                "target_unit": target_unit,
                "category": category,
                "start_date": str(start_date)
            }

            st.session_state.habits.to_csv(
                "habits_tracker.csv",
                index=False
            )
            # Update completion records if the name changed
            try:
                completions = pd.read_csv("habit_completions.csv")
    
                completions.loc[
                    completions["habit_name"] == old_habit_name,
                    "habit_name"
                ] = habit_name.strip()
    
                completions.to_csv(
                    "habit_completions.csv",
                    index=False
                )
    
            except FileNotFoundError:
                pass


            st.success("Habit updated successfully!")

    
    if st.button("Delete Habit"):

        # Delete from habits_tracker.csv
        st.session_state.habits = st.session_state.habits[
            st.session_state.habits["habit_name"] != selected_habit
        ]
    
        st.session_state.habits = st.session_state.habits.reset_index(drop=True)
    
        st.session_state.habits.to_csv(
            "habits_tracker.csv",
            index=False
        )
    
        # Delete from habit_completions.csv
        try:
            completions = pd.read_csv("habit_completions.csv")
    
            completions = completions[
                completions["habit_name"] != selected_habit
            ]
    
            completions.to_csv(
                "habit_completions.csv",
                index=False
            )
    
        except FileNotFoundError:
            pass
    
        st.success("Habit deleted successfully!")
    
        st.rerun()
    
            

else:
    st.info("You haven't added any habits yet.")
