import streamlit as st
import plotly.graph_objects as go

from vocava import entity, storage

COHERE_API_KEY = st.secrets["cohere_api_key"]


def analytics(user: entity.User):
    st.title("Your Learning Progress")

    st.metric(label="Translation Count", value=len(user.known_phrases()))
    st.metric(label="Vocabulary Count", value=len(user.known_vocabulary()))
    st.metric(label="Grammar Count", value=len(user.known_mistakes()))

    # Get the progress data
    progress_data = user.get_progress()

    # Create data lists for the plot
    dates = [item[0] for item in progress_data]
    counts = [item[1] for item in progress_data]

    # Create a Plotly line graph
    fig = go.Figure(data=go.Scatter(x=dates, y=counts))

    # Add layout
    fig.update_layout(
        title="Your Learning Progress Over Time",
        xaxis_title="Date",
        yaxis_title="Total Count of Saved Items",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )

    # Display the plot
    st.plotly_chart(fig)


def main():
    st.title("Analytics")

    st.header("Language Preferences ⚙️")
    languages = list(entity.LANGUAGES)
    default_native_lang = st.session_state.get("user.native_lang", languages[0])
    default_target_lang = st.session_state.get("user.target_lang", languages[4])
    default_fluency = st.session_state.get("user.fluency", 3)
    cols = st.columns(2)
    with cols[0]:
        native_language = st.selectbox(
            "Native Language", options=entity.LANGUAGES,
            index=languages.index(default_native_lang),
        )
    with cols[1]:
        target_language = st.selectbox(
            "Target Language", options=entity.LANGUAGES,
            index=languages.index(default_target_lang),
        )
    fluency = st.slider(
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
    analytics(user)


if __name__ == '__main__':
    main()
