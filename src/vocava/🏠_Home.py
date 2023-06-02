import streamlit

with open("home-page.md") as file:
    content = file.read()


streamlit.markdown(content)
