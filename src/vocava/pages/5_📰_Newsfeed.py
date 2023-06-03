import streamlit as st

from vocava import entity, storage
from vocava.news import get_news
from vocava.service import Service

NEWSDATA_API_KEY = st.secrets["newsdata_api_key"]
ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]
COHERE_API_KEY = st.secrets["cohere_api_key"]


def fetch_news(keyword: str, language: str):
    news = get_news(
        api_key=NEWSDATA_API_KEY,
        query=keyword,
        language=language,
    )
    return news["results"]


def main():
    st.title('Newsfeed')

    tutor = entity.get_tutor("Claude", key=ANTHROPIC_API_KEY)

    languages = list(entity.LANGUAGES)
    default_native_lang = st.session_state.get("user.native_lang", languages[0])
    default_target_lang = st.session_state.get("user.target_lang", languages[4])
    default_fluency = st.session_state.get("user.fluency", 3)
    native_language = st.sidebar.selectbox(
        "Native Language", options=entity.LANGUAGES,
        index=languages.index(default_native_lang),
    )
    target_language = st.sidebar.selectbox(
        "Choose Language", options=entity.LANGUAGES,
        index=languages.index(default_target_lang),
    )
    fluency = st.sidebar.slider(
        "Fluency", min_value=1, max_value=10, step=1,
        value=default_fluency,
    )
    store = storage.VectorStore(COHERE_API_KEY)
    store.connect()
    user = entity.User(
        native_language=native_language,
        target_language=target_language,
        fluency=fluency,
        db=store,
    )
    st.session_state["user.native_lang"] = native_language
    st.session_state["user.target_lang"] = target_language
    st.session_state["user.fluency"] = fluency

    keyword = st.text_input("Keyword", "technology")
    if st.button("Fetch News"):
        with st.spinner():
            articles = fetch_news(keyword, user.target_language_code())
        st.session_state["news.history"] = articles

    articles = st.session_state.get("news.history", [])
    for article in articles:
        with st.expander(article["title"]):
            st.write(article["description"])
            if article["image_url"]:
                st.image(article["image_url"])
            st.write(article["content"])
            st.markdown(f"[Read more]({article['link']})")
    st.divider()

    if articles:
        selected_article_title = st.selectbox(
            "Choose an article to translate",
            options=[article["title"] for article in articles]
        )
        selected_article = next(article for article in articles if
                                article['title'] == selected_article_title)

        length = len(selected_article["title"])
        length += len(selected_article["description"])
        length += len(selected_article["content"])
        length += 100
        if st.button("Translate Selected News"):
            news_service = Service(
                name="news-translate",
                user=user,
                tutor=tutor,
                max_tokens=length,
            )
            if "translated-title" not in selected_article:
                with st.spinner():
                    data = news_service.run(
                        title=selected_article["title"],
                        description=selected_article["description"],
                        text=selected_article["content"],
                    )
                selected_article["translated-title"] = data["title"]
                selected_article["translated-description"] = data["description"]
                selected_article["translated-content"] = data["content"]
            with st.expander(selected_article["translated-title"]):
                st.write(selected_article["translated-description"])
                if selected_article["image_url"]:
                    st.image(selected_article["image_url"])
                st.write(selected_article["translated-content"])
                st.write("[Read more]({})".format(selected_article["link"]))


if __name__ == "__main__":
    main()
