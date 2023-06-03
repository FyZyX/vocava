from datetime import datetime, timedelta

import plotly.graph_objects as go
import streamlit as st

from vocava import entity, storage

COHERE_API_KEY = st.secrets["cohere_api_key"]


def get_progress_graph(phrases, vocabulary, mistakes) -> go.Figure:
    traces = []
    colors = ['orange', 'deepskyblue', 'mediumseagreen']
    names = ['Known Phrases', 'Known Vocabulary', 'Known Mistakes']
    for idx, values in enumerate([phrases, vocabulary, mistakes]):
        total = 0
        dates, counts = [], []
        for value in values:
            dates.append(value["timestamp"])
            total += 1
            counts.append(total)
        trace = go.Scatter(x=dates, y=counts, mode='lines+markers', name=names[idx],
                           line=dict(color=colors[idx]))
        traces.append(trace)

    fig = go.Figure(data=traces)
    fig.update_layout(
        title="Your Learning Progress Over Time",
        xaxis_title="Date",
        yaxis_title="Total Count of Saved Items",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        ),
        xaxis=dict(
            showgrid=True,
        ),
        yaxis=dict(
            showgrid=True,
        ),
        legend=dict(
            y=0.5,
            font=dict(
                size=16
            )
        )
    )

    return fig


def count_recent_items(items, minutes=5):
    now = datetime.now()
    threshold = now - timedelta(minutes=minutes)
    return len([item for item in items if item['timestamp'] > threshold])


def analytics(user: entity.User):
    with st.spinner():
        known_phrases = user.known_phrases()
        known_vocabulary = user.known_vocabulary()
        known_mistakes = user.known_mistakes()

    cols = st.columns(3)
    with cols[0]:
        recent_phrases = count_recent_items(known_phrases)
        st.metric(label="Translation Count", value=len(known_phrases),
                  delta=recent_phrases)
    with cols[1]:
        recent_vocabulary = count_recent_items(known_vocabulary)
        st.metric(label="Vocabulary Count", value=len(known_vocabulary),
                  delta=recent_vocabulary)
    with cols[2]:
        recent_mistakes = count_recent_items(known_mistakes)
        st.metric(label="Grammar Count", value=len(known_mistakes),
                  delta=recent_mistakes)

    fig = get_progress_graph(known_phrases, known_vocabulary, known_mistakes)
    st.plotly_chart(fig)


def main():
    st.title("Analytics")

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
