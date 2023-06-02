import streamlit as st

from vocava import entity
from vocava.news import get_news
from vocava.service import Service

NEWSDATA_API_KEY = st.secrets["newsdata_api_key"]
ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]


def fetch_news(keyword: str, language: str):
    news = get_news(
        api_key=NEWSDATA_API_KEY,
        query=keyword,
        language=language,
    )
    return news["results"]


def main():
    st.title('Newsfeed')

    debug_mode = st.sidebar.checkbox("DEBUG Mode", value=True)
    model = "Claude" if not debug_mode else "mock"
    tutor = entity.get_tutor(model, key=ANTHROPIC_API_KEY)

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
    user = entity.User(
        native_language=native_language,
        target_language=target_language,
        fluency=fluency,
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
        with st.expander(article['title']):
            st.write(article['description'])
            st.write(article['content'])
            st.markdown(f"[Read more]({article['link']})")
    st.divider()

    if articles:
        selected_article_title = st.selectbox(
            "Choose an article to translate",
            options=[article['title'] for article in articles]
        )
        selected_article = next(article for article in articles if
                                article['title'] == selected_article_title)

        if st.button("Translate Selected News"):
            news_service = Service(
                name="news-translate",
                user=user,
                tutor=tutor,
                max_tokens=500,
            )
            if "translation" not in selected_article:
                with st.spinner():
                    data = news_service.run(
                        text=selected_article["content"],
                        fluency=user.fluency(),
                    )
                selected_article["translation"] = data["translation"]
            with st.expander(selected_article['title']):
                st.write(selected_article['translation'])
                st.write("[Read more]({})".format(selected_article['url']))


if __name__ == "__main__":
    main()
