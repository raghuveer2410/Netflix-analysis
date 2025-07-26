import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_page_config(page_title="Netflix Data Analysis", layout="wide")
st.title("📺 Netflix Data Analysis Dashboard")

@st.cache_data
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")

    # Check if expected columns are present
    expected_cols = ['director', 'cast', 'country']
    missing_cols = [col for col in expected_cols if col not in df.columns]
    if missing_cols:
        st.error(f"Missing columns in dataset: {missing_cols}")
        st.stop()

    df.dropna(subset=expected_cols, inplace=True)
    return df

# Load data
data = load_data()

# Sidebar Filters
type_filter = st.sidebar.multiselect("Select Content Type", options=data['type'].unique(), default=data['type'].unique())
country_filter = st.sidebar.multiselect("Select Country", options=data['country'].value_counts().index[:10], default=data['country'].value_counts().index[:5])
year_range = st.sidebar.slider("Select Year Range", int(data['year_added'].min()), int(data['year_added'].max()), (2015, 2021))

# Filter data
filtered = data[(data['type'].isin(type_filter)) &
                (data['country'].isin(country_filter)) &
                (data['year_added'] >= year_range[0]) &
                (data['year_added'] <= year_range[1])]

# KPI Section
col1, col2, col3 = st.columns(3)
col1.metric("Total Titles", len(filtered))
col2.metric("Movies", (filtered['type'] == 'Movie').sum())
col3.metric("TV Shows", (filtered['type'] == 'TV Show').sum())

# Charts Section
st.subheader("📊 Distribution by Type")
fig1, ax1 = plt.subplots()
sns.countplot(x='type', data=filtered, palette='Set2', ax=ax1)
st.pyplot(fig1)

st.subheader("🌎 Top Countries")
top_countries = filtered['country'].value_counts().head(10)
fig2, ax2 = plt.subplots()
sns.barplot(y=top_countries.index, x=top_countries.values, palette='Oranges', ax=ax2)
ax2.set_xlabel("Number of Titles")
st.pyplot(fig2)

st.subheader("📅 Yearly Content Added")
yearly_counts = filtered['year_added'].value_counts().sort_index()
fig3, ax3 = plt.subplots()
sns.lineplot(x=yearly_counts.index, y=yearly_counts.values, marker="o", ax=ax3)
ax3.set_xlabel("Year")
ax3.set_ylabel("Titles Added")
st.pyplot(fig3)

st.subheader("🎭 Most Common Genres")
all_genres = sum(filtered['genres'], [])
genre_counts = pd.Series(all_genres).value_counts().head(10)
fig4, ax4 = plt.subplots()
sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='Set3', ax=ax4)
ax4.set_xlabel("Count")
ax4.set_ylabel("Genre")
st.pyplot(fig4)

st.subheader("🔤 Word Cloud of Titles")
titles = filtered['title'].dropna()
wordcloud = WordCloud(width=800, height=400, background_color='black').generate(' '.join(titles))
fig5, ax5 = plt.subplots()
ax5.imshow(wordcloud, interpolation='bilinear')
ax5.axis('off')
st.pyplot(fig5)
