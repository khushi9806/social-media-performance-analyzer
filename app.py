import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Social Media Performance Analyzer",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------

st.sidebar.header("📂 Data Source")

data_source = st.sidebar.radio(
    "Choose Data Source",
    ["Use Sample Data", "Upload Your Own Data"]
)

if data_source == "Use Sample Data":

    df = pd.read_csv("Social_Media_Analyzed_Data.csv")

else:

    uploaded_file = st.sidebar.file_uploader(
        "Upload your Instagram data",
        type=["csv", "xlsx"]
    )

    if uploaded_file is not None:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)

        # -----------------------------
        # Data Validation
        # -----------------------------

        required_columns = [
            "Post ID",
            "Post Date",
            "Content Type",
            "Category",
            "Posting Time",
            "Views",
            "Likes",
            "Comments"
        ]

        optional_columns = [
            "Shares",
            "Saves",
            "Followers Gained",
            "Engagement Rate"
        ]

        # Check required columns
        missing_required = [
            column
            for column in required_columns
            if column not in df.columns
        ]

        if missing_required:
            st.error(
                "❌ Your file is missing required columns: "
                + ", ".join(missing_required)
            )
            st.stop()

        # Check optional columns
        missing_optional = [
            column
            for column in optional_columns
            if column not in df.columns
        ]

        if missing_optional:
            st.warning(
                "⚠️ Optional columns not found: "
                + ", ".join(missing_optional)
                + ". Some analysis may not be available."
            )
        else:
            st.success(
                "✅ All optional metrics are available!"
            )

        st.success(
            "✅ Your Instagram data has been uploaded successfully!"
        )

        # Uploaded Data Summary
        st.write("### 📊 Uploaded Data Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Records", len(df))

        with col2:
            st.metric("Total Columns", len(df.columns))

        with col3:
            st.metric("Data Validation", "Passed ✅")

    else:
        st.info(
            "👆 Please upload a CSV or Excel file to continue."
        )
        st.stop()
# -----------------------------
# Performance Score & Classification
# -----------------------------

performance_metrics = [
    "Views",
    "Likes",
    "Comments",
    "Shares",
    "Saves",
    "Followers Gained"
]

# Create normalized scores
for metric in performance_metrics:
    min_value = df[metric].min()
    max_value = df[metric].max()

    if max_value != min_value:
        df[metric + " Score"] = (
            (df[metric] - min_value)
            / (max_value - min_value)
        ) * 100
    else:
        df[metric + " Score"] = 0

# Calculate overall performance score
df["Performance Score"] = (
    df["Views Score"] * 0.30 +
    df["Likes Score"] * 0.20 +
    df["Comments Score"] * 0.10 +
    df["Shares Score"] * 0.10 +
    df["Saves Score"] * 0.10 +
    df["Followers Gained Score"] * 0.20
)

# Classify posts
score_rank = df["Performance Score"].rank(method="first")

df["Performance Level"] = pd.qcut(
    score_rank,
    q=[0, 0.30, 0.80, 1.00],
    labels=[
        "Low Performance",
        "Medium Performance",
        "High Performance"
    ]
)

# -----------------------------
# Title
# -----------------------------
st.title("📊 Social Media Performance Analyzer")
st.write(
    "Analyze social media post performance using data analysis."
)
# -----------------------------
# Performance Score Explanation
# -----------------------------

with st.expander("ℹ️ How is Performance Score calculated?"):

    st.write(
        "The Performance Score is calculated using the following weighted metrics:"
    )

    st.markdown("""
    - 👀 **Views:** 30%
    - ❤️ **Likes:** 20%
    - 💬 **Comments:** 10%
    - 🔄 **Shares:** 10%
    - 🔖 **Saves:** 10%
    - 👥 **Followers Gained:** 20%
    """)

    st.info(
        "Each metric is normalized to a score between 0 and 100, "
        "and the weighted scores are combined to calculate the overall "
        "Performance Score."
    )
# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

# Category filter
categories = ["All"] + sorted(df["Category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox(
    "Select Category",
    categories
)

# Content Type filter
content_types = ["All"] + sorted(df["Content Type"].dropna().unique().tolist())
selected_content = st.sidebar.selectbox(
    "Select Content Type",
    content_types
)

# Posting Time filter
posting_times = ["All"] + sorted(df["Posting Time"].dropna().unique().tolist())
selected_time = st.sidebar.selectbox(
    "Select Posting Time",
    posting_times
)
# Performance Level filter
performance_levels = ["All"] + sorted(
    df["Performance Level"].dropna().unique().tolist()
)

selected_performance = st.sidebar.selectbox(
    "Select Performance Level",
    performance_levels
)

# -----------------------------
# Apply Filters
# -----------------------------
filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

if selected_content != "All":
    filtered_df = filtered_df[
        filtered_df["Content Type"] == selected_content
    ]

if selected_time != "All":
    filtered_df = filtered_df[
        filtered_df["Posting Time"] == selected_time
    ]
if selected_performance != "All":
    filtered_df = filtered_df[
        filtered_df["Performance Level"] == selected_performance
    ]
    # Check if selected filters return any data
if filtered_df.empty:
    st.warning(
        "⚠️ No data is available for the selected filter combination. "
        "Please try different filters."
    )
    st.stop()
# -----------------------------
# KPI Section
# -----------------------------
st.subheader("📈 Performance Overview")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(
        "Total Posts",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Total Views",
        f"{filtered_df['Views'].sum():,}"
    )

with col3:
    st.metric(
        "Total Likes",
        f"{filtered_df['Likes'].sum():,}"
    )

with col4:
    st.metric(
        "Total Comments",
        f"{filtered_df['Comments'].sum():,}"
    )

with col5:
    st.metric(
        "Followers Gained",
        f"{filtered_df['Followers Gained'].sum():,}"
    )

# -----------------------------
# Engagement Rate
# -----------------------------
with col6:
    if len(filtered_df) > 0:
        avg_engagement = filtered_df["Engagement Rate"].mean()
    else:
        avg_engagement = 0

    st.metric(
        "Avg Engagement",
        f"{avg_engagement:.2f}%"
    )
# -----------------------------
# Complete Data
# -----------------------------
st.write("### 📋 Dataset")

display_columns = [
    "Post ID",
    "Post Date",
    "Content Type",
    "Category",
    "Posting Time",
    "Views",
    "Likes",
    "Comments",
    "Engagement Rate",
    "Performance Level"
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True
)
# -----------------------------
# Performance Classification
# -----------------------------
st.write("### 🎯 Performance Classification")

performance_count = filtered_df["Performance Level"].value_counts()

fig = px.bar(
    performance_count,
    x=performance_count.index,
    y=performance_count.values,
    title="Performance Classification"
)

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Performance Level",
    yaxis_title="Number of Posts",
    height=500,
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117"
)

st.plotly_chart(fig, use_container_width=True)
# -----------------------------
# Top 10 Posts by Engagement
# -----------------------------
st.write("### 🏆 Top 10 Posts by Engagement")

top_10 = (
    filtered_df
    .sort_values("Engagement Rate", ascending=False)
    .head(10)
)

st.dataframe(
    top_10[
        [
            "Post ID",
            "Content Type",
            "Category",
            "Views",
            "Likes",
            "Comments",
            "Shares",
            "Saves",
            "Followers Gained",
            "Engagement Rate"
        ]
    ],
    use_container_width=True,
    hide_index=True
)
# Top 10 Engagement Chart
fig = px.bar(
    top_10,
    x="Post ID",
    y="Engagement Rate",
    title="Top 10 Posts by Engagement Rate",
    text="Engagement Rate"
)

fig.update_traces(
    marker_color="#00BFFF",
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Post ID",
    yaxis_title="Engagement Rate (%)",
    height=500,
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117"
)

st.plotly_chart(fig, use_container_width=True)
# -----------------------------
# Best Posting Time
# -----------------------------
st.write("### 🕐 Average Views by Posting Time")

time_analysis = (
    filtered_df
    .groupby("Posting Time")["Views"]
    .mean()
    .sort_values(ascending=False)
)

if len(time_analysis) > 0:

    time_chart = time_analysis.reset_index()
    time_chart.columns = ["Posting Time", "Views"]

    fig = px.bar(
        time_chart,
        x="Posting Time",
        y="Views",
        title="Average Views by Posting Time"
    )

    # Highlight the best posting time
    bar_colors = [
        "#00C2FF" if i == 0 else "#6366F1"
        for i in range(len(time_chart))
    ]

    fig.update_traces(marker_color=bar_colors)

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Posting Time",
        yaxis_title="Average Views",
        height=500,
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("No data available for the selected filters.")

if len(time_analysis) > 0:
    best_time = time_analysis.index[0]
    best_time_views = time_analysis.iloc[0]

    st.info(
        f"📌 Best Posting Time: {best_time} "
        f"(Average Views: {best_time_views:,.0f})"
    )
    # -----------------------------
# Best Content Type
# -----------------------------
st.write("### 🎬 Average Views by Content Type")

content_analysis = (
    filtered_df
    .groupby("Content Type")["Views"]
    .mean()
    .sort_values(ascending=False)
)

if len(content_analysis) > 0:

    content_chart = content_analysis.reset_index()
    content_chart.columns = ["Content Type", "Views"]

    fig = px.bar(
        content_chart,
        x="Content Type",
        y="Views",
        title="Average Views by Content Type"
    )

    # Highlight the best content type
    bar_colors = [
        "#00C2FF" if i == 0 else "#6366F1"
        for i in range(len(content_chart))
    ]

    fig.update_traces(marker_color=bar_colors)

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Content Type",
        yaxis_title="Average Views",
        height=500,
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("No data available for the selected filters.")

if len(content_analysis) > 0:
    best_content = content_analysis.index[0]
    best_content_views = content_analysis.iloc[0]

    st.info(
        f"📌 Best Content Type: {best_content} "
        f"(Average Views: {best_content_views:,.0f})"
    )


# -----------------------------
# Best Category
# -----------------------------
st.write("### 🏷️ Average Engagement by Category")

category_analysis = (
    filtered_df
    .groupby("Category")["Engagement Rate"]
    .mean()
    .sort_values(ascending=False)
)

if len(category_analysis) > 0:

    category_chart = category_analysis.reset_index()
    category_chart.columns = ["Category", "Engagement Rate"]

    fig = px.bar(
        category_chart,
        x="Category",
        y="Engagement Rate",
        title="Average Engagement by Category"
    )

    # Highlight the best category
    bar_colors = [
        "#00C2FF" if i == 0 else "#6366F1"
        for i in range(len(category_chart))
    ]

    fig.update_traces(marker_color=bar_colors)

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Category",
        yaxis_title="Average Engagement Rate",
        height=500,
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("No data available for the selected filters.")
if len(category_analysis) > 0:
    best_category = category_analysis.index[0]
    best_category_engagement = category_analysis.iloc[0]

    st.info(
        f"📌 Best Category: {best_category} "
        f"(Average Engagement: {best_category_engagement:.2f}%)"
    )

    # ---------------------------
# Key Insights
# ---------------------------
st.write("### 💡 Key Insights")

st.info(
    f"🎬 **Best Content Type:** {best_content} "
    f"with {best_content_views:,.0f} average views."
)

st.info(
    f"🕒 **Best Posting Time:** {best_time} "
    f"with {best_time_views:,.0f} average views."
)

st.info(
    f"🏷️ **Best Category:** {best_category} "
    f"with {best_category_engagement:.2f}% average engagement."
)
# -------------------------
# Recommendations
# -------------------------

st.write("### 💡 Recommendations")

st.info(
    f"🎬 **Content Recommendation:** "
    f"Focus on {best_content} content because it has the highest "
    f"average views ({best_content_views:,.0f})."
)

st.info(
    f"⏰ **Posting Recommendation:** "
    f"Consider posting around {best_time} because it has the highest "
    f"average views ({best_time_views:,.0f})."
)

st.info(
    f"🏷️ **Category Recommendation:** "
    f"Focus on {best_category} because it has the highest "
    f"average engagement ({best_category_engagement:.2f}%)."
)
st.success(
    f"🎯 **Overall Recommendation:** "
    f"Focus on {best_content} content around {best_time}, "
    f"especially in the {best_category} category."
)
# -------------------------
# Best Performing Combination
# -------------------------

combination_analysis = (
    filtered_df
    .groupby(["Content Type", "Posting Time", "Category"])
    .agg(
        Average_Views=("Views", "mean"),
        Average_Engagement=("Engagement Rate", "mean"),
        Number_of_Posts=("Post ID", "count")
    )
)

# Only consider combinations with at least 2 posts
combination_analysis = combination_analysis[
    combination_analysis["Number_of_Posts"] >= 2
]

# Normalize views and engagement
views_min = combination_analysis["Average_Views"].min()
views_max = combination_analysis["Average_Views"].max()

engagement_min = combination_analysis["Average_Engagement"].min()
engagement_max = combination_analysis["Average_Engagement"].max()

if views_max != views_min:
    combination_analysis["Views_Score"] = (
        (combination_analysis["Average_Views"] - views_min)
        / (views_max - views_min)
    ) * 100
else:
    combination_analysis["Views_Score"] = 0

if engagement_max != engagement_min:
    combination_analysis["Engagement_Score"] = (
        (combination_analysis["Average_Engagement"] - engagement_min)
        / (engagement_max - engagement_min)
    ) * 100
else:
    combination_analysis["Engagement_Score"] = 0

# Final recommendation score
combination_analysis["Recommendation_Score"] = (
    combination_analysis["Views_Score"] * 0.60
    + combination_analysis["Engagement_Score"] * 0.40
)

combination_analysis = combination_analysis.sort_values(
    "Recommendation_Score",
    ascending=False
)

if len(combination_analysis) > 0:

    best_combination = combination_analysis.iloc[0]

    best_content_combo = combination_analysis.index[0][0]
    best_time_combo = combination_analysis.index[0][1]
    best_category_combo = combination_analysis.index[0][2]

    st.success(
    f"🔥 **Best Performing Combination:** "
    f"{best_content_combo} + {best_time_combo} + {best_category_combo}\n\n"
    f"📊 **Average Views:** {best_combination['Average_Views']:,.0f} | "
    f"💬 **Average Engagement:** {best_combination['Average_Engagement']:.2f}% | "
    f"🎯 **Recommendation Score:** "
    f"{best_combination['Recommendation_Score']:.2f}/100"
    f" | 📌 **Posts:** {int(best_combination['Number_of_Posts'])}"
)