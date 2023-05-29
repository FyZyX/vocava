import streamlit as st


def main():
    st.title('Culture Corner')

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

    target_lang = st.sidebar.text_input("Target Language", "en")

    if target_lang in culture_info:
        info = culture_info[target_lang]

        st.subheader("Places to visit")
        for place in info['places_to_visit']:
            st.write(place)

        st.subheader("Cuisine")
        for dish in info['cuisine']:
            st.write(dish)

        st.subheader("Local Politics")
        for politics in info['local_politics']:
            st.write(politics)

        st.subheader("Slang and Idioms")
        for slang_idiom in info['slang_idioms']:
            st.write(slang_idiom)
    else:
        st.write("Sorry, we don't have information for this language yet.")


if __name__ == "__main__":
    main()
