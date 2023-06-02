import streamlit as st

from vocava import entity
from vocava.service import Service

ANTHROPIC_API_KEY = st.secrets["anthropic_api_key"]


def main():
    st.title('Culture Corner')

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
    fluency = st.sidebar.slider("Fluency", min_value=1, max_value=10, step=1,
                                value=default_fluency)
    user = entity.User(
        native_language=native_language,
        target_language=target_language,
        fluency=fluency,
    )
    st.session_state["user.native_lang"] = native_language
    st.session_state["user.target_lang"] = target_language
    st.session_state["user.fluency"] = fluency

    culture_info = {
        "en": {
            "places_to_visit": ["New York", "Los Angeles", "Chicago"],
            "cuisine": ["Burger", "Pizza", "Fried Chicken"],
            "local_politics": ["US is a democratic country with a multi-party system.",
                               "The two major parties are the Democrats and Republicans."],
            "slang_idioms": ["Bite the bullet", "Break a leg", "Hit the sack"],
        },
        "fr": {
            "places_to_visit": ["Paris", "Marseille", "Lyon"],
            "cuisine": ["Baguette", "Croissant", "Coq au vin"],
            "local_politics": [
                "France is a democratic country with a semi-presidential system.",
                "The president is the head of the state."],
            "slang_idioms": ["C'est la vie", "Coup de foudre", "Bon appetit"],
        },
        # Add more languages...
    }

    if user.target_language_name() in culture_info:
        info = culture_info[user.target_language_name()]

        st.markdown("## Places to visit")
        st.markdown(", ".join(info['places_to_visit']))

        st.markdown("## Cuisine")
        st.markdown(", ".join(info['cuisine']))

        st.markdown("## Local Politics")
        st.markdown("\n".join(info['local_politics']))

        st.markdown("## Slang and Idioms")
        st.markdown(", ".join(info['slang_idioms']))
    else:
        st.write("Sorry, we don't have information for this language yet.")


if __name__ == "__main__":
    main()
