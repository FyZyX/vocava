import datetime

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

    services = [
        "Culture Info",
        "Plan a Trip",
        "Cultural Faux Pas",
    ]

    service_choice = st.selectbox("Choose a Service", options=services)
    st.divider()

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
        cols = st.columns(3)
        with cols[0]:
            country = st.text_input("Country")
        with cols[1]:
            start_date = st.date_input("Start Date", datetime.date.today() +
                                       datetime.timedelta(days=30))
        with cols[2]:
            end_date = st.date_input("End Date", datetime.date.today() +
                                     datetime.timedelta(days=37))
        cols = st.columns(2)
        with cols[0]:
            budget = st.number_input("Budget (U.S. $)", min_value=100)
        with cols[1]:
            companions = st.selectbox("Travel Companions", [
                "Alone", "Partner", "Family",
            ])
        interests = st.multiselect("Interests", [
            "Historical Sites", "Nature", "Food", "Music Festivals",
        ])

        if st.button("Plan a Trip"):
            selected_service = Service(
                "culture-trip",
                user=user,
                tutor=tutor,
                max_tokens=2_000,
                extract_json=False,
            )
            with st.spinner():
                trip_info = selected_service.run(
                    country=country,
                    start_date=start_date,
                    end_date=end_date,
                    budget=budget,
                    interests=", ".join(interests),
                    companions=companions,
                    fluency=user.fluency(),
                )
            st.session_state["culture.trip"] = trip_info

        if "culture.trip" in st.session_state:
            trip_info = st.session_state["culture.trip"]
            st.markdown(trip_info)

    elif service_choice == "Cultural Faux Pas":
        cols = st.columns(2)
        with cols[0]:
            country = st.text_input("Country")
        with cols[1]:
            region = st.text_input("Region or City (Optional)")

        if st.button("Get Cultural Faux Pas"):
            selected_service = Service(
                "culture-faux-pas",
                user=user,
                tutor=tutor,
                max_tokens=2_000,
                extract_json=False,
            )
            with st.spinner():
                faux_pas_info = selected_service.run(
                    country=country,
                    region=region,
                    fluency=user.fluency(),
                )
            st.session_state["culture.faux_pas"] = faux_pas_info

        if "culture.faux_pas" in st.session_state:
            faux_pas_info = st.session_state["culture.faux_pas"]
            st.markdown(faux_pas_info)


if __name__ == "__main__":
    main()
