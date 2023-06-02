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

    services = {
        "Culture Info": Service("culture-info", user=user, tutor=tutor),
        "Plan a Trip": Service("culture-trip", user=user, tutor=tutor),
        "Cultural Faux Pas": Service("culture-faux-pas", user=user, tutor=tutor)
    }

    service_choice = st.selectbox(
        "Choose a Service", options=list(services.keys())
    )
    selected_service = services[service_choice]

    if service_choice == "Culture Info":
        if st.button("Create Guide"):
            selected_service = Service(
                "culture-info",
                user=user,
                tutor=tutor,
                max_tokens=2_000,
                extract_json=False,
            )
            with st.spinner():
                service_info = selected_service.run(fluency=user.fluency())
            st.session_state["culture.info"] = service_info
        if "culture.info" in st.session_state:
            service_info = st.session_state["culture.info"]
            st.markdown(service_info)

    elif service_choice == "Plan a Trip":
        service_info = selected_service.run()
        st.markdown("\n".join(service_info))

    elif service_choice == "Cultural Faux Pas":
        service_info = selected_service.run()
        st.markdown("\n".join(service_info))


if __name__ == "__main__":
    main()
