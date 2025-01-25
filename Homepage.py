import streamlit as st
from class_methods import Film, Catalogue
from info import get_movie_info, display_info
import datetime as dt

st.title('Film: La :red[Condivisa]')

userbase = ['reactorr', 'Joy', 'Pietro', 'Luca C.', 'Tiziana', 'Luca I.', 'Carmine']
select = st.selectbox('Select user:', userbase)

if select:
    st.write(f"Welcome back, {select}!")
    catalogue = Catalogue()

    # MOVIE OF THE WEEK
    st.header('Film della settimana')
    check = catalogue.check_film()
    
    # Get current week's film
    current_films = [Film.from_dict(f) for f in catalogue.collection.find({'week_f': True})]
    # rate 
    if current_films:
        film = current_films[0]
        st.write(f"Rate the film of the week: {film.info['title']}")
        rate = st.slider('Rate:', 0, 10, 5)
        if st.button('Submit rate'):
            film.rate = rate
            catalogue.collection.update_one(
                {'info': film.info},
                {'$set': {f'{select}_rate': rate}}
            )
            st.success('Rate submitted!')
    
    if select == 'reactorr':
        st.button('Reset week', on_click=catalogue.reset_week())
    
    if current_films:
        film = current_films[0]
        display_info(film.info)
        st.write(f"Proposed by: *{film.proposed_by}*")
        st.write(f"Starts on: {film.start.strftime('%d/%m/%Y')}")
        st.write(f"Ends on: {film.end.strftime('%d/%m/%Y')}")
    else:
        if st.button('Pick the random film of the week'):
            film = catalogue.random_film()
            if film:
                st.success('Film of the week picked!')

    # FILMS LIST
    st.subheader('Film proposti')
    available_films = [Film.from_dict(f) for f in 
                      catalogue.collection.find({'week_f': False, 'watched': False})]
    
    for film in available_films:
        display_info(film.info)
        st.write(f"Proposed by: *{film.proposed_by}*")
        if select == 'reactorr':
            if st.button('Set as film of the week'):
                catalogue.set_week_film(film.info)

    # ADD FILM
    st.subheader('Propose a film')
    u_input = st.text_input('Film title:')
    
    if u_input:
        titolo = get_movie_info(u_input)
        display_info(titolo)
        check = False

        if st.button('Search'):
            # Check if film already exists
            existing_film = catalogue.collection.find_one({'info.title': titolo['title']})
            if existing_film:
                st.error('Film already proposed!')
                check = True
            
            # Check if user already proposed an unwatched film
            user_proposal = catalogue.collection.find_one({
                'proposed_by': select,
                'watched': False
            })
            if user_proposal:
                st.error('You have already proposed a film!')
                check = True
            
            if not check:
                film = Film(titolo, select)
                catalogue.add_film(film)
                st.success('Film proposed!')

    catalogue.close()