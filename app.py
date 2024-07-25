import streamlit as st
import pickle
import pandas as pd
import requests


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]  # fetch index of particular movie
    distances = similarity[movie_index]  # fetch all 4806 similarities
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommend_poster = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append((movies.iloc[i[0]]).title)
        # fetch poster from API
        recommend_poster.append(fetch_poster(movie_id))

    return recommended_movies,recommend_poster


def fetch_poster(movie_id):
    language = 'en-US'
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=481898ef3e66d74acc76d8796dba17be&language={}'.format(movie_id,
                                                                                                          language))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']  #poster path


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))  # it is equal to new_df
movies = pd.DataFrame(movies_dict)


similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie from drop down menu',
    movies['title'].values)

if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
