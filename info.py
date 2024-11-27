from bs4 import BeautifulSoup
import requests
import re
import streamlit as st


def get_movie_info(titolo):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    url = 'https://www.imdb.com/find/?q=' + titolo + '%20' + '&ref_=nv_sr_sm'

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    if soup:
        print("got page")
        link = soup.find('a', class_='ipc-metadata-list-summary-item__t', href=lambda href: href and '/title/' in href)
        image = soup.find("img", class_="ipc-image")
        image_src = image['src']
        href = link.get('href')
        title = link.get_text()
        title_id = href.split('/title/')[1].split('/')[0]

        info = {
            "title": title,
            "image": image_src
        }

        response = requests.get(f"https://www.imdb.com/title/{title_id}", headers=headers)
        if response.status_code != 200:
            print("Error")
        else:
            print("got id and info")
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup:
                items = soup.find_all("li", class_="ipc-inline-list__item")
        if items:
            print("got items")
        for i in range(4, 11):
            info["year"] = items[4].get_text()
            info["rating"] = items[5].get_text()
            info["duration"] = items[6].get_text()
            info["director"] = items[7].get_text()
            info["writer"] = items[8].get_text()
            info["with"] = items[9].get_text()
            info["and"] = items[10].get_text()
        return info


def display_info(info):
    col1, col2 = st.columns([1,7])
    with col1:
        st.text(" ")
        st.text(" ")
        st.image(info["image"], use_container_width=True)
    with col2:
        st.subheader(info["title"])
        st.text(f"{info['year']} | {info['rating']} | {info['duration']}")
        st.text(f"Director: {info['director']}\n"
                f"Writer: {info['writer']}\n"
                f"with: {info['with']}\n"
                f"and: {info['and']}")