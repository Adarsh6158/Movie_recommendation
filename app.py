import pickle
import streamlit as st
import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    namesMovie = []
    posters = []
    for i in distances[1:13]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        posters.append(fetch_poster(movie_id))
        namesMovie.append(movies.iloc[i[0]].title)

    return namesMovie, posters
from PIL import Image
import base64

# Define a function to convert an image to Base64
def get_base64(image):
    with open(image, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode()
    return base64_image

# Define the set_background function
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f'''
    <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
        }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)


background_image = 'bg.jpg' 

set_background(background_image)

# CSS styles with animations
st.markdown("""
<style>
    .title-text {
        font-size: 36px;
        color: #FF5733;
        text-align: center;
        animation: fadeInUp 2s ease;
    }
    .header-text {
        font-size: 24px;
        color: #009688;
        text-align: center;
        animation: fadeInDown 2s ease;
    }
    
    @keyframes fadeInUp {
        0% {
            opacity: 0;
            transform: translateY(20px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInDown {
        0% {
            opacity: 0;
            transform: translateY(-20px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }
</style>
""", unsafe_allow_html=True)


st.markdown('<p class="title-text">Welcome to the Movie Recommendation App</p>', unsafe_allow_html=True)

st.markdown('<p class="header-text">Movie Recommendation</p>', unsafe_allow_html=True)
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
# selected_movie = st.selectbox(
#     "Type or select a movie from the dropdown",
#     movie_list
# )
st.markdown("<h3 style='color: white;'>Type or select a movie from the dropdown</h3>", unsafe_allow_html=True)

# Use st.selectbox for the dropdown
selected_movie = st.selectbox("Select a movie", movie_list)


# Create a sidebar
st.sidebar.title("About me")
st.sidebar.header("Movie recomendation")
st.sidebar.write("Find awesome movies you'll love with our recommendation project that uses smart tech to suggest the perfect film for you.")
st.sidebar.write("Connect with me on:")
st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/adarsh-35a9931ba)")
st.sidebar.markdown("[GitHub](https://github.com/Adarsh6158)")
st.sidebar.markdown("[Website](https://adarsh11.netlify.app)")
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    num_columns = 4
    num_recommendations = min(len(recommended_movie_names), 12)
    
    for i in range(num_recommendations):
        if i % num_columns == 0:
            col = st.columns(num_columns)
        
        with col[i % num_columns]:
            st.markdown(f'<p style="color: white; font-weight: bold;">{recommended_movie_names[i]}</p>', unsafe_allow_html=True)
            st.image(recommended_movie_posters[i])
            imdb_search_query = recommended_movie_names[i].replace(" ", "+")
            imdb_url = f"https://www.imdb.com/find?q={imdb_search_query}"
            st.markdown(
                f'<a href="{imdb_url}" target="_blank" style="background-color: #FFA500; color: white; padding: 8px 12px; text-align: center; text-decoration: none; display: inline-block; border-radius: 4px;">IMDb</a>',
                unsafe_allow_html=True
            )