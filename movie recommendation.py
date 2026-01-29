# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 17:13:23 2026

@author: gatik
"""

import streamlit as st
import pickle
import difflib

# Load model
model = pickle.load(open(
    "C:/Users/gatik/Downloads/movie system/movie_recomendation_model.sav",
    "rb"
))

movies_data = model['movies_data']
similarity = model['similarity']

st.title("🎬 Movie Recommendation App")

movie_name = st.text_input("Movie Name")

if st.button("Recommend"):
    if movie_name.strip() == "":
        st.warning("Please enter a movie name")
        st.stop()

    list_of_all_titles = movies_data['title'].tolist()

    find_close_match = difflib.get_close_matches(
        movie_name,
        list_of_all_titles,
        n=1,
        cutoff=0.5
    )

    if not find_close_match:
        st.error("Movie not found. Please check spelling.")
        st.stop()

    close_match = find_close_match[0]

    index_of_movie = movies_data[movies_data['title'] == close_match].index[0]

    similarity_score = list(enumerate(similarity[index_of_movie]))

    sorted_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    st.success("Movies recommended for you:")
    st.write(f"0. {close_match} (Selected Movie)")


    i = 1
    for movie in sorted_movies:
        index = movie[0]
        title = movies_data.iloc[index]['title']

        if title == close_match:
            continue

        if i <= 10:
            st.write(f"{i}. {title}")
            i += 1
