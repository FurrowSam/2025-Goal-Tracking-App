from dash import Dash, dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

# Initialize the app
app = Dash(__name__)

# Define activities and initialize data
def load_data():
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
    date_range = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
    progress_table = pd.DataFrame(index=date_range, columns=activities)
    progress_table[:] = "Not Completed"
    return progress_table

# Load the initial data
progress_table = load_data()

# Layout of the app
app.layout = html.Div([
    html.H1("2025 Daily Progress Tracker"),
    
    # Date Picker
    dcc.DatePickerSingle(
        id='date-picker',
        date=date.today(),
        display_format="YYYY-MM-DD"
    ),
    html.H3(id='date-header'),

    # Activity Checkboxes
    html.Div(id='activity-checklist'),

    # Save Button
    html.Button("Save Progress", id='save-button', n_clicks=0),
    html.Div(id='save-message'),

    # Full Table Display
    html.Button("Show Full Progress Table", id='show-table-button', n_clicks=0),
    html.Div(id='full-table-container'),

    # Visualization
    html.Button("Generate Visualization", id='generate-viz-button', n_clicks=0),
    dcc.Graph(id='progress-viz')
])

# Callbacks for dynamic content
@app.callback(
    [Output('date-header', 'children'),
     Output('activity-checklist', 'children')],
    [Input('date-picker', 'date')]
)
def update_activities(selected_date):
    if not selected_date:
        selected_date = str(date.today())

    checklist = []
    for activity in progress_table.columns:
        checklist.append(
            html.Div([
                dcc.Checklist(
                    options=[{'label': activity, 'value': 'Completed'}],
                    id=f"checklist-{activity}",
                    value=['Completed'] if progress_table.loc[selected_date, activity] == "Completed" else []
                )
            ])
        )
    return f"Activities for {selected_date}", checklist


@app.callback(
    Output('save-message', 'children'),
    [Input('save-button', 'n_clicks')],
    [State('date-picker', 'date')] + [
        State(f"checklist-{activity}", 'value') for activity in load_data().columns
    ]
)
def save_progress(n_clicks, selected_date, *activity_states):
    if n_clicks > 0:
        for activity, state in zip(progress_table.columns, activity_states):
            progress_table.loc[selected_date, activity] = "Completed" if 'Completed' in state else "Not Completed"
        
        progress_table.to_csv("progress_tracker.csv")
        return "Progress saved successfully!"


@app.callback(
    Output('full-table-container', 'children'),
    [Input('show-table-button', 'n_clicks')]
)
def show_full_table(n_clicks):
    if n_clicks > 0:
        return html.Div([
            html.H4("Full Progress Table"),
            dcc.Graph(
                figure=go.Figure(data=[
                    go.Table(
                        header=dict(values=["Date"] + list(progress_table.columns)),
                        cells=dict(values=[progress_table.index] + [progress_table[col].values for col in progress_table.columns])
                    )
                ])
            )
        ])
    return ""


@app.callback(
    Output('progress-viz', 'figure'),
    [Input('generate-viz-button', 'n_clicks')]
)
def generate_visualization(n_clicks):
    if n_clicks > 0:
        completed_counts = (progress_table == "Completed").sum(axis=1).reset_index()
        completed_counts.columns = ["Date", "Completed Activities"]
        
        fig = px.line(completed_counts, x="Date", y="Completed Activities",
                      title="Number of Completed Activities Over Time")
        return fig
    return go.Figure()

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
