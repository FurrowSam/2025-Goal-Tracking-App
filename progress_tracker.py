import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date

# Set page configuration
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
    # 2025 is used as an example year
    date_range = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
    # Create DataFrame
    progress_table = pd.DataFrame(index=date_range, columns=activities)
    progress_table[:] = "Not Completed"  # Default status
    return progress_table

# Load data or read from CSV
# If the CSV file does not exist, create a new DataFrame
try:
    progress_table = pd.read_csv("progress_tracker.csv", index_col=0)
    progress_table.index = pd.to_datetime(progress_table.index)  # Ensure proper datetime index
except FileNotFoundError:
    progress_table = load_data()

# Title
# Set the title of the app
st.title("🌟 2025 Daily Progress Tracker")

# Sidebar for navigation
st.sidebar.header("Navigation")
view = st.sidebar.radio("Go to:", ["Today's Activities", "Full Progress Table", "Visualizations"])

# Select today's date
today = st.sidebar.date_input("Select the date", date.today())

if view == "Today's Activities":
    # Display activities for today
    st.header(f"✅ Activities for {today}")
    st.markdown("Check off activities as you complete them:")

    if str(today) in progress_table.index:
        cols = st.columns(len(progress_table.columns) // 3 + 1)  # Split activities into columns
        for i, activity in enumerate(progress_table.columns):
            with cols[i % len(cols)]:
                # Add a checkbox for each activity
                if st.checkbox(activity, key=f"{today}_{activity}", value=(progress_table.loc[str(today), activity] == "Completed")):
                    progress_table.loc[str(today), activity] = "Completed"
                else:
                    progress_table.loc[str(today), activity] = "Not Completed"

                # Save progress to CSV in real-time
                progress_table.to_csv("progress_tracker.csv")

elif view == "Full Progress Table":
    st.header("📋 Full Progress Table")
    st.markdown("Review your progress throughout the year.")
    
    # Highlight completed rows in green
    def color_completed(val):
        return "background-color: #d4edda; color: black;" if val == "Completed" else ""

    styled_table = progress_table.style.applymap(color_completed)
    st.dataframe(styled_table, use_container_width=True)

elif view == "Visualizations":
    # Seaborn Visualizations
    st.header("📊 Progress Visualizations")
    st.markdown("Visualize your progress over time.")

    if st.button("Generate Visualization"):
        # Create a summary of completed tasks
        completed_counts = (progress_table == "Completed").sum(axis=1).reset_index()
        completed_counts.columns = ["Date", "Completed Activities"]

        # Lineplot of progress over time
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=completed_counts, x="Date", y="Completed Activities", marker="o")
        plt.title("📈 Number of Completed Activities Over Time", fontsize=16)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Completed Activities", fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Display the plot in Streamlit
        st.pyplot(plt)
