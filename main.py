import streamlit as st
import requests
from config import EDAMAM_APP_ID, EDAMAM_APP_KEY

# Injecting custom styles
st.markdown("""
<style>
    .recipe-image {
        width: 100px;
        height: 100px;
        object-fit: cover;
        border-radius: 8px;
    }

    .recipe-title {
        max-width: 200px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
</style>
""", unsafe_allow_html=True)

st.title("Recipe Finder")

ingredients = st.text_input("Enter ingredients separated by commas:")

vegetarian = st.checkbox("Vegetarian")
vegan = st.checkbox("Vegan")
keto = st.checkbox("Keto")

diet_filter = ""
if vegetarian:
    diet_filter += "&diet=vegetarian"
if vegan:
    diet_filter += "&diet=vegan"
if keto:
    diet_filter += "&diet=keto-friendly"



if st.button("Search"):
    url = f"https://api.edamam.com/search?q={ingredients}&app_id={EDAMAM_APP_ID}&app_key={EDAMAM_APP_KEY}{diet_filter}"
    response = requests.get(url)

    # Check if the API request was successful
    if response.status_code == 200:
        data = response.json()

        # Display results
        for recipe in data["hits"]:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f'<img src="{recipe["recipe"]["image"]}" class="recipe-image">', unsafe_allow_html=True)

            with col2:
                st.markdown(f"<div class='recipe-title'>{recipe['recipe']['label']}</div>", unsafe_allow_html=True)

            with col3:
                with st.expander("View Details"):
                    st.write(recipe["recipe"]["url"])
                    st.write(f"Calories: {recipe['recipe']['calories']:.2f}")
                    st.write(f"Total time: {recipe['recipe']['totalTime']} minutes")

    else:
        st.write("Error with the API request:", response.text)






