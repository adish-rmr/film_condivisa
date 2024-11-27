import streamlit as st
from class_methods import Film, Catalogue
from info import get_movie_info, display_info
import os, pickle
import random
import datetime as dt

st.title('Film: La :red[Condivisa]')

userbase = ['reactorr', 'Joy', 'Pietro', 'Luca C.', 'Tiziana', 'Luca I.', 'Carmine']

select = st.selectbox('Select user:', userbase)

if select:
    st.write(f"Welcome back, {select}!")

    catalogue = Catalogue()
    if os.path.exists('films.pkl'):
        catalogue.import_data()

    # MOVIE OF THE WEEK

    st.header('Film della settimana')
    check = catalogue.check_film()
    if check:
        catalogue.save_data()
    flag = False
    for film in catalogue.films:
        if film.week_f:
            display_info(film.info)
            st.write(f"Proposed by: *{film.proposed_by}*")
            st.write(f"Starts on: {film.start.strftime('%d/%m/%Y')}")
            st.write(f"Ends on: {film.end.strftime('%d/%m/%Y')}")
            flag = True
    if not flag:
        if st.button('Pick the random film of the week'):
            film = catalogue.random_film()
            st.success('Film of the week picked!')
            catalogue.save_data()

    # FILMS LIST

    st.subheader('Film proposti')
    for film in catalogue.films:
        if not film.week_f and not film.watched:
            display_info(film.info)
            st.write(f"Proposed by: *{film.proposed_by}*")

    # ADD FILM

    st.subheader('Propose a film')
    u_input = st.text_input('Film title:')
    if u_input:
        titolo = get_movie_info(u_input)
        display_info(titolo)
        check = False
    if st.button('Search'):
        for film in catalogue.films:
            if film.info['title'] == titolo['title']:
                st.error('Film already proposed!')
                check = True
                break
            elif film.proposed_by == select and not film.watched:
                st.error('You already proposed a film!')
                check = True
                break
        if not check or catalogue.films == []:
            film = Film(titolo, select)
            catalogue.add_film(film)
            st.success('Film proposed!')
            catalogue.save_data()
            
    


