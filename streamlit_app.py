import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load and cache data
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    
    # Check if expected columns exist
    required_columns = ['director', 'cast', 'country']
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        st.error(f"Missing columns in dataset: {missing}")
        st.stop()

    df.dropna(subset=required_columns, inplace=True)
    return df

# Main app
def main():
    st.title("📺 Netflix Data Analysis Dashboard")
    df = load_data()

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Country Distribution
    st.subheader("Top 10 Countries with Most Content")
    top_countries = df['country'].value_counts().nlargest(10)
    st.bar_chart(top_countries)

    # Wordcloud for Titles
    st.subheader("Word Cloud of Movie Titles")
    title_text = " ".join(df['title'].astype(str))
    wc = WordCloud(width=800, height=400, background_color='black').generate(title_text)
    st.image(wc.to_array(), use_column_width=True)

    # Type Distribution
    st.subheader("Content Type Distribution")
    st.write(df['type'].value_counts())
    fig, ax = plt.subplots()
    sns.countplot(data=df, x='type', ax=ax)
    st.pyplot(fig)

if __name__ == '__main__':
    main()
