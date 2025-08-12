"""
Minimal Streamlit app to display task creation leaderboard.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json
from datetime import datetime

# Configuration
STATS_URL = "https://raw.githubusercontent.com/sama-at/public-data/main/task_stats.json"  # UPDATE THIS

st.set_page_config(
    page_title="Task Leaderboard",
    page_icon="🏆",
    layout="centered"
)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_stats():
    """Load statistics from the public repository."""
    try:
        response = requests.get(STATS_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None

def main():
    st.title("🏆 Task Creation Leaderboard")
    
    # Load data
    stats = load_stats()
    
    if not stats:
        st.warning("No data available. Please check back later.")
        return
    
    # Display last updated time
    st.caption(f"Last updated: {stats.get('updated_date', 'Unknown')}")
    
    # Display summary metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Tasks", stats.get('total_tasks', 0))
    with col2:
        st.metric("Total Creators", stats.get('total_creators', 0))
    
    # Prepare data for the chart
    task_counts = stats.get('task_counts', {})
    if task_counts:
        df = pd.DataFrame(
            list(task_counts.items()),
            columns=['Creator', 'Tasks']
        )
        
        # Create bar chart with Plotly
        fig = px.bar(
            df,
            x='Creator',
            y='Tasks',
            title='Tasks Created by Each Person',
            labels={'Tasks': 'Number of Tasks', 'Creator': 'Creator'},
            color='Tasks',
            color_continuous_scale='Viridis',
            text='Tasks'
        )
        
        # Update layout for better appearance
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(
            showlegend=False,
            xaxis_tickangle=-45,
            height=500,
            yaxis=dict(title='Number of Tasks'),
            xaxis=dict(title='Creator'),
            margin=dict(t=60, b=100)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display data table
        with st.expander("View Data Table"):
            st.dataframe(
                df.sort_values('Tasks', ascending=False),
                use_container_width=True,
                hide_index=True
            )
    else:
        st.info("No task data available yet.")
    
    # Auto-refresh button
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

if __name__ == "__main__":
    main()
