import streamlit as st
from class_methods import Film
from info import search_movies
import datetime as dt
from pymongo import MongoClient
import uuid


st.title('Film: La :red[Condivisa]')

connection = MongoClient("mongodb+srv://user:So6fB5dMOkCcQiTl@cluster0.mxnrotu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = connection['film']
collection = db['catalogo']

API_KEY = 'df8cf73ddd0a97c1a95b8aefba52afdb'

st.header('Chi sei?')
userbase = ['PioSan', 'paracetamuoio', 'Luca C.', 'RedWill93', 'NukularCoffee', 'Dolente2', 'reactorr', 'DarthValer', 'Gerardo']
user = st.selectbox('Select user:', userbase)
st.session_state['user'] = user

st.header('Proponi un film', divider=True)

lista = []
titolo = st.text_input('Titolo')
if st.button('Cerca'):
    lista = search_movies(API_KEY, titolo)
if lista:
    st.image(lista[0]['poster_url'], width=300)
    st.write(lista[0]['title'])
    st.write(lista[0]['release_date'])
    st.write(lista[0]['original_title'])
    st.session_state['film'] = lista[0]
    

if st.button('Aggiungi') and 'film' in st.session_state:
    info = st.session_state['film']
    film = Film(titolo, info['release_date'], info['title'], info['poster_url'], user)
    collection.insert_one(film.to_dict())
    st.success('Film aggiunto!')
    
st.header('Film in visione', divider=True)
# film in visione e non visto
film_in_visione = collection.find_one({'in_visione': True, 'watched': False})

if film_in_visione:
    st.subheader(film_in_visione['title'])
    st.image(film_in_visione['poster'], width=300)
    
    if st.button('Visto') and st.session_state['user'] == 'reactorr':
        collection.update_one({'in_visione': True}, {'$set': {'in_visione': False, 'watched': True}})
        st.success('Film segnato come visto!')
    
    #vota film
    rating = st.number_input('Voto:', 1.0, 10.0, step=0.25, key='rating')
    if st.button('Vota', key = 'special'):
        collection.update_one(
            {'title': film_in_visione['title']},
            {'$set': {f'rating.{user}': rating}}
        )
        
st.header('Film proposti', divider=True)
film_proposti = collection.find({'in_visione': False, 'watched': False})

i = 0
for film in film_proposti:
    st.subheader(film['title'])
    st.image(film['poster'], width=300)
    st.write(film['proposed_by'])
    if st.button('Ritira', key=i) and st.session_state['user'] == film['proposed_by']:
        collection.delete_one({'title': film['title']})
    if st.button('Vedi', key=i+1) and st.session_state['user'] == 'reactorr':
        collection.update_one({'in_visione': True}, {'$set': {'watched': True}})
        collection.update_one({'titolo': film['titolo']}, {'$set': {'in_visione': True}})
        st.success('Film in visione aggiornato!')
    i += 2
    
if st.button('Film random') and st.session_state['user'] == 'reactorr':
    one = collection.aggregate([{'$match': {'in_visione': False, 'watched': False}}, {'$sample': {'size': 1}}])
    for film in one:
        collection.update_one({'in_visione': True}, {'$set': {'watched': True}})
        collection.update_one({'titolo': film['titolo']}, {'$set': {'in_visione': True}})
        st.success('Film random aggiornato!')

st.header('Vota film', divider=True)
film_visti = collection.find({'watched': True})
film_visti_list = [film['title'] for film in film_visti]
film_visti_list = sorted(film_visti_list)

film_visto = st.selectbox('Seleziona film visto:', film_visti_list)
rating2 = st.number_input('Voto:', 1.0, 10.0, step=0.25, key='rating_week')
if st.button('Vota'):
    collection.update_one(
        {'title': film_visto},
        {'$set': {f'rating.{user}': rating2}}
    )
        
st.header('Classifica', divider=True)
film_rating = collection.find({'rating': {'$exists': True}})

classifica = []

for film in film_rating:
    if film['watched'] == True and len(film['rating']) > 0:
        rank = {
            film['title']: round(sum(film['rating'].values()) / len(film['rating']),2),
            'Ratings' : film['rating']
        }
        classifica.append(rank)

classifica = sorted(classifica, key=lambda x: list(x.values())[0], reverse=True)
st.write(classifica)