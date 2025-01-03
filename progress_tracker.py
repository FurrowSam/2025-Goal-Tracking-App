import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date

# Initialize the DataFrame or load from a CSV file
@st.cache_data
def load_data():
    # Define activities
    activities = [
        "Morning Workout",
        "Breakfast",
        "Job Search / Project Review",
        "Work Hours",
        "Afternoon Walk",
        "Snack/Refresh",
        "AI/ML Projects / Job Search",
        "Afternoon Workout",
        "Dinner / Chores",
        "Free Time",
        "Plan for Tomorrow"
    ]
    # Create a date range for the year
    date_range = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
    # Create DataFrame
    progress_table = pd.DataFrame(index=date_range, columns=activities)
    progress_table[:] = "Not Completed"  # Default status
    return progress_table

# Load data
progress_table = load_data()

# Title
st.title("2025 Daily Progress Tracker")

# Select today's date
today = st.date_input("Select the date", date.today())

# Display activities for today
st.header(f"Activities for {today}")
if str(today) in progress_table.index:
    for activity in progress_table.columns:
        # Add a checkbox for each activity
        if st.checkbox(activity, key=f"{today}_{activity}"):
            progress_table.loc[str(today), activity] = "Completed"
        else:
            progress_table.loc[str(today), activity] = "Not Completed"

# Save progress
if st.button("Save Progress"):
    st.write(progress_table.head())

    progress_table.to_csv("progress_tracker.csv")
    st.success("Progress saved!")

# Display the full table (optional)
if st.checkbox("Show Full Progress Table"):
    st.dataframe(progress_table)

# Seaborn Visualizations
st.header("Progress Visualizations")

# Create a summary of completed tasks
if st.button("Generate Visualization"):
    completed_counts = (progress_table == "Completed").sum(axis=1).reset_index()
    completed_counts.columns = ["Date", "Completed Activities"]

    # Lineplot of progress over time
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=completed_counts, x="Date", y="Completed Activities")
    plt.title("Number of Completed Activities Over Time")
    plt.xlabel("Date")
    plt.ylabel("Completed Activities")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(plt)



