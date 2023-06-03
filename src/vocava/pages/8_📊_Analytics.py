import streamlit as st
import plotly.graph_objects as go

from vocava import entity, storage

COHERE_API_KEY = st.secrets["cohere_api_key"]


def analytics(user: entity.User):
    with st.spinner():
        known_phrases = user.known_phrases()
        known_vocabulary = user.known_vocabulary()
        known_mistakes = user.known_mistakes()

    cols = st.columns(3)
    with cols[0]:
        st.metric(label="Translation Count", value=len(known_phrases))
    with cols[1]:
        st.metric(label="Vocabulary Count", value=len(known_vocabulary))
    with cols[2]:
        st.metric(label="Grammar Count", value=len(known_mistakes))

    # Get the progress data
    progress_data = user.get_progress()

    # Create data lists for the plot
    dates, counts = [], []
    for date, count in progress_data:
        dates.append(date)
        counts.append(count)

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

    with st.expander("Language Preferences ⚙️"):
        languages = list(entity.LANGUAGES)
        default_native_lang = st.session_state.get("user.native_lang", languages[0])
        default_target_lang = st.session_state.get("user.target_lang", languages[4])
        default_fluency = st.session_state.get("user.fluency", 3)
        native_language = st.sidebar.selectbox(
            "Native Language", options=entity.LANGUAGES,
            index=languages.index(default_native_lang),
        )
        target_language = st.sidebar.selectbox(
            "Target Language", options=entity.LANGUAGES,
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
    analytics(user)


if __name__ == '__main__':
    main()
