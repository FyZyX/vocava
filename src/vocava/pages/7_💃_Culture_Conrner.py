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

    culture_service = Service("culture", user=user, tutor=tutor)
    trip_service = Service("trip", user=user, tutor=tutor)
    faux_pas_service = Service("faux_pas", user=user, tutor=tutor)

    culture_info = culture_service.run()
    trip_info = trip_service.run()
    faux_pas_info = faux_pas_service.run()

    st.markdown("## Places to visit")
    st.markdown(", ".join(culture_info.get('places_to_visit', [])))

    st.markdown("## Cuisine")
    st.markdown(", ".join(culture_info.get('cuisine', [])))

    st.markdown("## Local Politics")
    st.markdown("\n".join(culture_info.get('local_politics', [])))

    st.markdown("## Slang and Idioms")
    st.markdown(", ".join(culture_info.get('slang_idioms', [])))

    st.markdown("## Plan a Trip")
    st.markdown("\n".join(trip_info))

    st.markdown("## Cultural Faux Pas")
    st.markdown("\n".join(faux_pas_info))


if __name__ == "__main__":
    main()
