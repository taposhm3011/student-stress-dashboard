
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("Mock_Student_Survey_With_OpenEnded.csv")

st.set_page_config(page_title="Student Stress & Achievement Dashboard", layout="wide")

st.title("🎓 Student Stress & Achievement Dashboard")
st.markdown("Analyze student well-being and performance metrics from survey results.")

# Sidebar filters
with st.sidebar:
    selected_category = st.selectbox("Filter by Group Category", options=["All"] + sorted(df["Category"].unique().tolist()))
    selected_student = st.selectbox("Drill Down to Student", options=["All"] + sorted(df["Student Name"].unique().tolist()))

# Apply filters
filtered_df = df.copy()
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]
if selected_student != "All":
    filtered_df = filtered_df[filtered_df["Student Name"] == selected_student]

# Radar chart for individual student
if selected_student != "All":
    st.subheader(f"📊 Competency Profile: {selected_student}")
    student_row = filtered_df.iloc[0]
    radar_data = pd.DataFrame({
        "Competency": ["Stress Triggers", "Emotional Regulation", "Coping Strategies", "Goal Setting", "Drive and Persistence", "Personal Growth"],
        "Score": [student_row["Stress Triggers"], student_row["Emotional Regulation"], student_row["Coping Strategies"],
                  student_row["Goal Setting"], student_row["Drive and Persistence"], student_row["Personal Growth"]]
    })
    fig_radar = px.line_polar(radar_data, r='Score', theta='Competency', line_close=True,
                              title="Radar Chart of Competency Scores", range_r=[0,5])
    st.plotly_chart(fig_radar, use_container_width=True)

# Heatmap
st.subheader("🔥 Heatmap of Competency Scores (All Students)")
score_columns = ["Stress Triggers", "Emotional Regulation", "Coping Strategies", "Goal Setting", "Drive and Persistence", "Personal Growth"]
heatmap_data = filtered_df.set_index("Student Name")[score_columns]
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap="YlOrRd", annot=True, linewidths=0.5, ax=ax)
st.pyplot(fig)

# Open-ended responses
if selected_student != "All":
    st.subheader("🗣 Open-Ended Responses")
    st.markdown(f"**Biggest Source of Stress**: {student_row['Biggest Source of Stress']}")
    st.markdown(f"**Support or Resources Needed**: {student_row['Support or Resources Needed']}")
    st.markdown(f"**5-Year Career Milestone**: {student_row['5-Year Career Milestone']}")
    st.markdown(f"**Challenging Academic Project**: {student_row['Challenging Academic Project']}")
    st.markdown(f"**Biggest Professional Fear**: {student_row['Biggest Professional Fear']}")
