
import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.title("My Progress")

today = date.today()

habits = st.session_state.habits

try:
    completions = pd.read_csv("habit_completions.csv")
except FileNotFoundError:
    completions = pd.DataFrame(
        columns=["habit_name", "date", "completed"]
    )

completions["date"] = pd.to_datetime(completions["date"]).dt.date


# calculate the user's daily progress.
total_habits = len(habits)

active_habit_names = habits["habit_name"].tolist()

completed_today = completions[
    (completions["date"] == today) &
    (completions["completed"] == True) &
    (completions["habit_name"].isin(active_habit_names))
]

completed_count = completed_today["habit_name"].nunique()

# Calculate daily progress percentage
if total_habits > 0:
    progress = completed_count / total_habits
else:
    progress = 0

col1, col2, col3 = st.columns(3)

col1.metric("Total Habits", total_habits)
col2.metric("Completed Today", completed_count)
col3.metric("Progress", f"{progress:.0%}")

st.progress(progress)


# Habit Performance

st.subheader("Habit Performance")

performance = []

for index, row in habits.iterrows():

    habit = row["habit_name"]
    frequency = row["frequency"]
    target = int(row["target_goal"])
    start_date = pd.to_datetime(row["start_date"]).date()

    habit_completions = completions[
        (completions["habit_name"] == habit) &
        (completions["completed"] == True)
    ]

    completed_dates = habit_completions["date"].tolist()

    streak = 0
    
    # Calculate streak and completion rate for daily habits
    if frequency == "Daily":

        check_date = today
        
        # If not completed today, start checking from yesterday
        if check_date not in completed_dates:
            check_date = today - timedelta(days=1)
            
        # Count consecutive completed days
        while check_date in completed_dates and check_date >= start_date:
            streak += 1
            check_date = check_date - timedelta(days=1)

        total_days = (today - start_date).days + 1

        completed_count = 0

        for completed_date in completed_dates:
            if start_date <= completed_date <= today:
                completed_count += 1

        if total_days > 0:
            completion_rate = completed_count / total_days
        else:
            completion_rate = 0

        streak_text = f"{streak} days"
        
    # Calculate streak and completion rate for weekly habits
    else:

        week_start = start_date - timedelta(days=start_date.weekday())
        current_week = today - timedelta(days=today.weekday())

        completed_weeks = []

        while week_start <= current_week:

            next_week = week_start + timedelta(days=7)
            
            # Count completed days in the current week
            days_completed = 0

            for completed_date in completed_dates:
                if week_start <= completed_date < next_week:
                    days_completed += 1

            if days_completed >= target:
                completed_weeks.append(week_start)

            week_start = next_week

        check_week = current_week

        if check_week not in completed_weeks:
            check_week = current_week - timedelta(days=7)

        while check_week in completed_weeks:
            streak += 1
            check_week = check_week - timedelta(days=7)

        total_weeks = ((current_week - (start_date - timedelta(days=start_date.weekday()))).days // 7) + 1

        if total_weeks > 0:
            completion_rate = len(completed_weeks) / total_weeks
        else:
            completion_rate = 0

        streak_text = f"{streak} weeks"
        
    # Check if the daily habit earned the 7-day reward
    if frequency == "Daily" and streak >= 7:
        st.success(f"🏆 {habit}: 7-Day Reward Unlocked!")
    performance.append({
        "Habit": habit,
        "Current Streak": streak_text,
        "Completion Rate": f"{completion_rate:.0%}"
    })

performance_df = pd.DataFrame(performance)

st.dataframe(performance_df, hide_index=True)



# Completion History

st.subheader("Completion History")

if len(completions) > 0:

    history = completions[
        completions["completed"] == True
    ]

    history = history.groupby("date").size()

    # Display dates without time
    history.index = [
        completion_date.strftime("%Y-%m-%d")
        for completion_date in history.index
    ]

    st.bar_chart(history)

else:
    st.info("No completion history yet.")

