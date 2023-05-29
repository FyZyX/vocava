import streamlit as st

from vocava.news import get_news

NEWSDATA_API_KEY = st.secrets["newsdata_api_key"]


def fetch_news(keyword: str, language: str):
    news = get_news(
        api_key=NEWSDATA_API_KEY,
        query=keyword,
        language=language,
    )
    return news["results"]


def main():
    st.title('Newsfeed')

    cols = st.columns([3, 1])
    with cols[0]:
        keyword = st.text_input("Keyword", "technology")
    with cols[1]:
        target_lang = st.text_input("Language", "en")

    if st.button("Fetch News"):
        articles = fetch_news(keyword, target_lang)
        for article in articles:
            st.subheader(article['title'])
            st.write(article['description'])
            st.write(article['content'])
            st.write("[Read more]({})".format(article['url']))
            st.write("-----")


if __name__ == "__main__":
    main()
