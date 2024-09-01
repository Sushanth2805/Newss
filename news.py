import streamlit as st
import requests

# Set your NewsAPI key securely
NEWS_API_KEY = st.secrets["NEWS_API"]

# Define the base URL for NewsAPI
BASE_URL = "https://newsapi.org/v2/top-headlines?"

# Set up the Streamlit app
st.title("Taaza News")

# Let the user select a country
country = st.selectbox("Select Country", ["us", "in", "gb", "ca", "au"])

# Let the user select a category
category = st.selectbox(
    "Select News Category",
    ["business", "entertainment", "general", "health", "science", "sports", "technology"],
)

# Let the user enter a keyword for search
keyword = st.text_input("Enter a keyword to search news (optional)")

# Let the user select the number of articles to display
num_articles = st.slider("Number of articles to display", 5, 50, 20)

# Fetch the news from NewsAPI
@st.cache_data
def get_news(country, category, keyword, page_size):
    params = {
        "country": country,
        "category": category,
        "q": keyword,
        "apiKey": NEWS_API_KEY,
        "pageSize": page_size,
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

# Show news when the user clicks the button
if st.button("Get News"):
    with st.spinner("Fetching news..."):
        news_data = get_news(country, category, keyword, num_articles)

    # Check if news data is valid and display it
    if news_data and news_data.get("status") == "ok":
        for article in news_data["articles"]:
            st.subheader(article["title"])
            
            # Check if the description exists before displaying it
            description = article.get("description")
            if description:
                st.write(description)  # Only display if description is present
              # Optional: display a placeholder message

            if article.get('urlToImage'):
                st.image(article['urlToImage'], width=100)  # Displaying an image if available
            st.write(f"[Read more]({article['url']})")
            st.write("—" * 50)
    else:
        st.error("Failed to fetch news. Please check your API key and parameters.")

# Add an info box for users
st.info("This app uses the NewsAPI to fetch and display the latest news based on the selected country, category, and optional keyword.")

# Hide the Streamlit footer
hide_footer_style = """
    <style>
    .footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_footer_style, unsafe_allow_html=True)
