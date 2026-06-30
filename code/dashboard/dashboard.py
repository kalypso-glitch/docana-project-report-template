import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import os


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------
@st.cache_data
def load_data():
    base_path = os.path.join(os.path.dirname(__file__), "../../results/")
    #base = Path(__file__).resolve().parent.parent  # goes from /code/dashboard to project root
    sub_path = os.path.join(base_path, "subreddit_stats.csv")
    user_path = os.path.join(base_path, "user_stats.csv")
    sim_path = os.path.join(base_path, "user_sub_similarity.csv")

    return (
        pd.read_csv(sub_path),
        pd.read_csv(user_path),
        pd.read_csv(sim_path)
    )


sub_df, user_df, sim_df = load_data()


# ---------------------------------------------------------
# Dashboard Layout
# ---------------------------------------------------------
st.set_page_config(
    page_title="Reddit Readability Dashboard",
    layout="wide"
)

st.title("📊 Reddit Readability Dashboard")
st.markdown("Interaktive Analyse von Subreddits, Usern und Readability Scores.")


# ---------------------------------------------------------
# Tabs
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📁 Subreddits", "👤 Users", "🔗 User–Sub Similarity"])

def top_20_percent(df, column="count_posts"):
    threshold = df[column].quantile(0.80)  # 80th percentile
    return df[df[column] >= 10]




# ---------------------------------------------------------
# Subreddit Tab
# ---------------------------------------------------------
with tab1:
    st.header("Subreddit Statistics")

    st.subheader("Subreddit auswählen")

    sub_query = st.text_input("Subreddit eingeben (Autocomplete)")

    # Vorschläge generieren
    if sub_query:
        sub_suggestions = [
            s for s in sub_df["subreddit"].unique()
            if sub_query.lower() in s.lower()
        ][:10]  # nur 10 Vorschläge
    else:
        sub_suggestions = []

    # Vorschläge anzeigen
    if sub_suggestions:
        st.write("Vorschläge:")
        for s in sub_suggestions:
            if st.button(s, key=f"sub_{s}"):
                sub_query = s

    # Auswahl übernehmen, wenn exakter Treffer
    selected_sub = sub_query if sub_query in sub_df["subreddit"].unique() else None

    if selected_sub is not None and selected_sub != "":
        filtered = sub_df[sub_df["subreddit"] == selected_sub]
    else:
        filtered = sub_df


    st.subheader("Tabelle")
    top_subs_df = top_20_percent(filtered, "count_posts")
    st.dataframe(top_subs_df, use_container_width=True)

    st.subheader("Durchschnittlicher Readability Score")
    fig = px.bar(
        filtered,
        x="subreddit",
        y="avg",
        title="Average Readability per Subreddit",
        color="avg",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------
# User Tab
# ---------------------------------------------------------
with tab2:
    st.header("User Statistics")

    user_query = st.text_input("User eingeben (Autocomplete)")

    # Vorschläge generieren
    if user_query:
        user_suggestions = [
            u for u in user_df["author"].unique()
            if user_query.lower() in u.lower()
        ][:10]  # nur 10 Vorschläge
    else:
        user_suggestions = []

    # Vorschläge anzeigen
    if user_suggestions:
        st.write("Vorschläge:")
        for s in user_suggestions:
            if st.button(s, key=f"sub_{s}"):
                user_query = s

    # Auswahl übernehmen, wenn exakter Treffer
    selected_user = user_query if user_query in user_df["author"].unique() else None


    if selected_user is not None and selected_user != "":
        filtered = user_df[user_df["author"] == selected_user]
    else:
        filtered = user_df

    st.subheader("Tabelle")
    top_users_df = top_20_percent(filtered, "count_posts")
    st.dataframe(top_users_df, use_container_width=True)

    st.subheader("Durchschnittlicher Readability Score")
    fig = px.bar(
        filtered,
        x="author",
        y="avg",
        title="Average Readability per User",
        color="avg",
        color_continuous_scale="Greens"
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------
# User–Sub Similarity Tab
# ---------------------------------------------------------
with tab3:
    st.header("User–Subreddit Similarity")

    st.markdown("Vergleicht, wie ähnlich der User‑Score dem Subreddit‑Score ist.")

    st.subheader("Heatmap: User vs Subreddit")
    top_users = sim_df["author"].value_counts().head(50).index
    top_subs = sim_df["subreddit"].value_counts().head(50).index

    filtered = sim_df[
        sim_df["author"].isin(top_users) &
        sim_df["subreddit"].isin(top_subs)
    ]

    pivot = filtered.pivot_table(
        index="author",
        columns="subreddit",
        values="diff",
        aggfunc="mean"
    )


    fig = px.imshow(
        pivot,
        color_continuous_scale="RdBu_r",
        aspect="auto",
        title="Score Difference (User vs Subreddit)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Rohdaten")
    #top_sim_df = top_20_percent(sim_df, "count_posts")
    st.dataframe(filtered, use_container_width=True)
    #lazy_table(sim_df, page_size=50, key_prefix="sim")
