
import streamlit as st
import pandas as pd
from datetime import timedelta, date


st.title("My Rewards 🏆")

# Read completion records
try:
    completions = pd.read_csv("habit_completions.csv")

except FileNotFoundError:
    completions = pd.DataFrame(
        columns=["habit_name", "date", "completed"]
    )


# Keep only completed records
completed_habits = completions[
    completions["completed"].astype(str).str.lower() == "true"
].copy()


# Keep only active habits
active_habit_names = st.session_state.habits["habit_name"].tolist()

completed_habits = completed_habits[
    completed_habits["habit_name"].isin(active_habit_names)
].copy()


# Remove duplicate records
completed_habits["date"] = pd.to_datetime(
    completed_habits["date"]
).dt.date

completed_habits = completed_habits.drop_duplicates(
    subset=["habit_name", "date"]
)


# Calculate completion points
completion_points = len(completed_habits) * 10


# Calculate streak bonus points
bonus_points = 0

habit_streaks = {}

today = date.today()

for habit in completed_habits["habit_name"].unique():

    habit_records = completed_habits[
        completed_habits["habit_name"] == habit
    ]

    completed_dates = sorted(
        habit_records["date"].unique()
    )

    streak = 0
    previous_date = None

    longest_streak = 0

    for completed_date in completed_dates:

        if previous_date is None:
            streak = 1

        elif completed_date == previous_date + timedelta(days=1):
            streak += 1

        else:
            streak = 1

        if streak > longest_streak:
            longest_streak = streak

        previous_date = completed_date

    # Calculate current streak
    if completed_dates[-1] == today:
        current_streak = streak

    elif completed_dates[-1] == today - timedelta(days=1):
        current_streak = streak

    else:
        current_streak = 0

    habit_streaks[habit] = current_streak

    # Calculate bonus points
    if longest_streak >= 30:
        bonus_points += 130

    elif longest_streak >= 7:
        bonus_points += 30


# Display points
total_points = completion_points + bonus_points

st.subheader("Your Points")

col1, col2 = st.columns(2)

col1.metric("Total Points", total_points)
col2.metric("Bonus Points", bonus_points)


# Streak Progress
st.divider()

st.subheader("🔥 Your Streak Progress")

if len(habit_streaks) > 0:

    for habit, streak in habit_streaks.items():

        st.write(f"**{habit}**")

        if streak >= 30:
            st.success(
                "🏆 Congratulations! You earned the "
                "30-day streak reward: 100 bonus points!"
            )

        elif streak >= 7:
            st.success(
                "🔥 Congratulations! You earned the "
                "7-day streak reward: 30 bonus points!"
            )

        else:
            days_left = 7 - streak

            st.progress(streak / 7)

            st.caption(
                f"{streak}/7 days completed - "
                f"{days_left} more days to earn 30 bonus points!"
            )

else:
    st.info("Complete your habits to start earning points!")


# How to Earn Rewards
st.divider()

st.subheader("🎁 How to Earn Rewards")

st.write("Complete your daily habits and earn points!")

st.markdown("""
- ✅ **Daily Completion:** Earn **10 points** for every habit you complete each day.

### 🏆 Bonus Rewards

- 🔥 **7-Day Streak:** Complete the same habit for 7 consecutive days and earn **30 bonus points**.

- 🏆 **30-Day Streak:** Complete the same habit for 30 consecutive days and earn **100 bonus points**.

💡 **Remember:** Missing a day resets your streak. Stay consistent and keep earning rewards!
""")
