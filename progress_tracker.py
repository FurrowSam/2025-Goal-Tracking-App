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
        "Job Search",
        "Minimum of 4 GitHub Commits",
        "Afternoon Workout",
        "Dinner / Chores",
        "Free Time",
        "Planning for Tomorrow"
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
    st.header("📊 Progress Dashboard")
    st.markdown("A snapshot of your progress and task completion overview.")

    # Total number of tasks completed across all activities
    total_completed = (progress_table == "Completed").sum().sum()
    total_tasks = progress_table.size
    completion_rate = total_completed / total_tasks * 100

    # Task completion counts
    task_completion_counts = (progress_table == "Completed").sum(axis=0).sort_values(ascending=False)

    # Display KPIs
    st.markdown("### 📈 Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Completed Tasks", total_completed)
    col2.metric("Total Tasks", total_tasks)
    col3.metric("Completion Rate", f"{completion_rate:.2f}%")

    # Task completion comparison bar chart
    st.markdown("### 🔄 Task Completion Comparison")
    import plotly.express as px
    task_completion_df = task_completion_counts.reset_index()
    task_completion_df.columns = ["Activity", "Total Completed"]

    fig_bar = px.bar(
        task_completion_df,
        x="Total Completed",
        y="Activity",
        orientation="h",
        title="Total Completed Tasks Per Activity",
        color="Total Completed",
        color_continuous_scale="Viridis",
    )
    fig_bar.update_layout(
        xaxis_title="Total Completed",
        yaxis_title="Activity",
        title_font_size=18,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Weekly progress heatmap (optional additional visualization)
    st.markdown("### 📅 Weekly Progress Heatmap")
    daily_completed = (progress_table == "Completed").sum(axis=1)
    daily_completed_df = daily_completed.reset_index()
    daily_completed_df.columns = ["Date", "Completed Count"]
    daily_completed_df["Week"] = daily_completed_df["Date"].dt.isocalendar().week
    daily_completed_df["Day"] = daily_completed_df["Date"].dt.day_name()

    fig_heatmap = px.density_heatmap(
        daily_completed_df,
        x="Day",
        y="Week",
        z="Completed Count",
        title="Weekly Task Completion Heatmap",
        color_continuous_scale="Blues",
    )
    fig_heatmap.update_layout(
        xaxis_title="Day of the Week",
        yaxis_title="Week Number",
        title_font_size=18,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
