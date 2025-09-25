import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#To activate virtual environnement on bash source .venv/Scripts/activate

@st.cache_data
def load_data(fileName) :
    return pd.read_parquet(fileName)

def spotify_outlier_genres_pie(df, year, top_n_genres=10):
    sub = df[(df["year"] == year) & (~df["on_billboard_year"])].copy()
    outliers = sub.sort_values("track_popularity", ascending=False)

    # turning the list string into a list so that we can explode it later
    # else the parts of the pie chart will be based on combined genres
    outliers["artist_genres"] = outliers["artist_genres"].astype(str).str.strip("[]").str.replace("'", "").str.split(",")

    # explode into individual genres
    exploded = outliers.explode("artist_genres")
    exploded["artist_genres"] = exploded["artist_genres"].str.strip()  # trim spaces

    genre_counts = exploded["artist_genres"].value_counts().head(top_n_genres)

    new_df = genre_counts.reset_index()
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(aspect="equal"))
    ax.pie(new_df["count"], None, labels=new_df["artist_genres"], autopct="%1.0f%%")
    
    st.pyplot(fig)
    st.caption(f"Spotify-only Outliers in {year} (by Genre Share)")

def spotify_hit_genres_pie(df, year, top_n_genres=10):
    sub = df[(df["year"] == year) & (df["on_billboard_year"])].copy()
    outliers = sub.sort_values("track_popularity", ascending=False)

    # turning the list string into a list so that we can explode it later
    # else the parts of the pie chart will be based on combined genres
    outliers["artist_genres"] = outliers["artist_genres"].astype(str).str.strip("[]").str.replace("'", "").str.split(",")

    # explode into individual genres
    exploded = outliers.explode("artist_genres")
    exploded["artist_genres"] = exploded["artist_genres"].str.strip()  # trim spaces

    genre_counts = exploded["artist_genres"].value_counts().head(top_n_genres)

    new_df = genre_counts.reset_index()
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(aspect="equal"))
    ax.pie(new_df["count"], None, labels=new_df["artist_genres"], autopct="%1.0f%%")
    
    st.pyplot(fig)
    st.caption(f"Spotify songs that are on the billboard in {year} (by Genre Share)")

st.set_page_config(layout="wide")

billboard_yearly_df = load_data('dataset_cleaned/billboard_yearly.parquet')
spotify_df = load_data('dataset_cleaned/spotify.parquet')
join_df = load_data('dataset_cleaned/spotify_billboard_joined.parquet')

st.title("The analyse of songs popularity in the USA and Worldwide")
col1, col2, col3, col4 = st.columns(4)
with col4:
    st.markdown("from **New Groove**")

st.markdown('#')

st.title("The longevity of hits in the USA")
st.markdown('#####')
col1, col2 = st.columns(2)

with col1 :
    top20_df = billboard_yearly_df[billboard_yearly_df["best_rank_year"] <= 20]
    median_weeks_agg_cols = {
        "weeks_in_hot100_year": "median",
        "weeks_to_peak_year": "median",
    }
    median_weeks_top20 = top20_df.groupby("year").agg(median_weeks_agg_cols)
    median_weeks_top20.rename(columns={"weeks_in_hot100_year": "median_weeks_on_chart", "weeks_to_peak_year": "median_weeks_to_peak"}, inplace=True)
    median_weeks_top20.reset_index("year", inplace=True)
    # do the same but for top 100
    top100_df = billboard_yearly_df[billboard_yearly_df["best_rank_year"] <= 100]
    median_weeks_top100 = top100_df.groupby("year").agg(median_weeks_agg_cols)
    median_weeks_top100.rename(columns={"weeks_in_hot100_year": "median_weeks_on_chart", "weeks_to_peak_year": "median_weeks_to_peak"}, inplace=True)
    median_weeks_top100.reset_index("year", inplace=True)

    df_20 = median_weeks_top20.rename(columns={
        "median_weeks_on_chart": "Weeks on Chart (Top 20)",
        "median_weeks_to_peak": "Weeks to Peak (Top 20)"
    })

    df_100 = median_weeks_top100.rename(columns={
    "median_weeks_on_chart": "Weeks on Chart (Top 100)",
    "median_weeks_to_peak": "Weeks to Peak (Top 100)"
    })

    df = pd.merge(df_20[["year", "Weeks on Chart (Top 20)", "Weeks to Peak (Top 20)"]],
                df_100[["year", "Weeks on Chart (Top 100)", "Weeks to Peak (Top 100)"]],
                on="year")

    # Set year as index (nicer for plotting)
    df = df.set_index("year")

    st.line_chart(df)
    st.caption("Median Weeks in Billboard (2010-2021)")

with col2 :
    trendBurning_fig = plt.figure(figsize=(7,6))
    plt.scatter(billboard_yearly_df["weeks_to_peak_year"], 
            billboard_yearly_df["weeks_in_hot100_year"], 
            alpha=0.3)

    plt.title("Weeks to Peak vs Weeks on Chart (Billboard 2010–2021)")
    plt.xlabel("Weeks to peak rank (velocity)")
    plt.ylabel("Weeks on chart (longevity)")
    plt.grid(True, linestyle="-.", alpha=0.5)
    st.pyplot(trendBurning_fig)


st.markdown("##")

st.title("Billboard (USA) vs Spotify (global)")
st.markdown('#####')
col1, col2 = st.columns(2)

with col1:
    coverage = join_df.groupby("year")["on_billboard_year"].mean().reset_index(name="coverage_rate")
    coverage["coverage_rate"] = (coverage["coverage_rate"]*100).round(1)

    fig = plt.figure(figsize=(10,6))
    plt.bar(coverage["year"], coverage["coverage_rate"], color="skyblue", edgecolor="black")
    plt.title("Spotify Top 100 ↔ Billboard Hot 100 Alignment (2010-2021)")
    plt.xlabel("Year")
    plt.ylabel("Coverage Rate (%)")
    plt.xticks(rotation=45)
    plt.ylim(0, 100)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    fig = plt.figure(figsize=(10,6))

    # joined tracks
    mask = join_df["on_billboard_year"]

    plt.scatter(
        join_df.loc[mask, "track_popularity"],
        join_df.loc[mask, "best_rank_year"],
        c="tab:blue", alpha=0.6, label="On Billboard"
    )

    # not on Billboard
    plt.scatter(
        join_df.loc[~mask, "track_popularity"],
        [105] * sum(~mask),
        c="tab:red", alpha=0.6, marker="x", label="Spotify only"
    )

    plt.title("Spotify Popularity vs Billboard Best Rank (2010–2021)")
    plt.xlabel("Spotify Track Popularity")
    plt.ylabel("Billboard Best Rank")
    plt.gca().invert_yaxis()
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig)


st.markdown('##')

option = st.selectbox("", join_df.groupby("year")["year"])

st.markdown('#####')

col1, col2 = st.columns(2)

with col1:
    spotify_outlier_genres_pie(join_df, option)

with col2:
    spotify_hit_genres_pie(join_df, option)

st.markdown("##")

st.title("Trait needed to be a slow-burning hit")
st.markdown('#####')

hits = join_df[join_df["on_billboard_year"]].copy()
spotify_only = join_df[~join_df["on_billboard_year"]].copy()

def vs_scatter_plot(first_trait, second_trait):
    fig = plt.figure(figsize=(8,6))
    sc = plt.scatter(hits[first_trait], hits[second_trait], c=hits["weeks_in_hot100_year"], cmap="viridis", alpha=0.7)
    plt.colorbar(sc, label="Weeks on Billboard Hot 100")
    plt.xlabel(first_trait)
    plt.ylabel(second_trait)
    plt.grid(True, linestyle="-.", alpha=0.5)
    st.pyplot(fig)
    st.caption(f"{first_trait} vs {second_trait} (colored by longevity)")

metrics_cols = ["danceability","energy","loudness","acousticness","instrumentalness","liveness","valence"]

col1, col2= st.columns(2)
with col1:
    col1Bis, col2Bis = st.columns(2)
    with col1Bis:
        first_trait = st.selectbox("First trait", metrics_cols)
    with col2Bis:
        second_trait = st.selectbox("Second trait", metrics_cols, index=1)
    vs_scatter_plot(first_trait, second_trait)

with col2:
    trait = st.selectbox("Trait", metrics_cols)
    fig = plt.figure(figsize=(8,6))
    plt.hist(hits[trait].dropna(), bins=30, alpha=0.6, label="Billboard Joiners", color="skyblue")
    plt.hist(spotify_only[trait].dropna(), bins=30, alpha=0.6, label="Spotify-only", color="salmon")
    plt.xlabel(trait)
    plt.ylabel("Count")
    plt.legend()
    st.pyplot(fig)
    st.caption(f"Distribution of {trait}")

st.markdown('##')

col1, col2, col3 = st.columns(3)

with col2:
    metrics_subset = join_df[metrics_cols]
    metrics_subset_top20 = join_df[join_df["best_rank_year"] <= 20][metrics_cols]

    means_metrics = metrics_subset.mean()
    normalized_metrics = (means_metrics - metrics_subset.min()) / (metrics_subset.max() - metrics_subset.min())

    means_metrics_top20 = metrics_subset_top20.mean()
    normalized_metrics_top20 = (means_metrics_top20 - metrics_subset_top20.min()) / (metrics_subset_top20.max() - metrics_subset_top20.min())

    labels = normalized_metrics.index
    values = normalized_metrics.values

    # trying to do a spider/ radar plot here...
    # https://stackoverflow.com/questions/52910187/how-to-make-a-polygon-radar-spider-chart-in-python
    # https://matplotlib.org/stable/gallery/specialty_plots/radar_chart.html
    values = np.concatenate((values, [values[0]])) # close the loop or else the plot won't be complete...
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))

    top20_values = np.concatenate((normalized_metrics_top20.values, [normalized_metrics_top20.values[0]]))

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, 'o-', linewidth=2)
    # ax.plot(angles, top20_values, 'o-', linewidth=2, color='orange') # not as useful as I thought
    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_ylim(0,1)

    st.pyplot(fig)
    st.caption("What trait to target for a song to be a hit ?")