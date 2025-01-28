import requests

def search_movies(api_key, query):
    """
    Search for a movie using TMDB API and return its poster path and full title.
    
    Args:
        api_key (str): Your TMDB API key
        query (str): Movie title to search for
    
    Returns:
        list: List of dictionaries containing movie information
    """
    
    # TMDB API endpoints
    base_url = "https://api.themoviedb.org/3"
    search_endpoint = f"{base_url}/search/movie"
    image_base_url = "https://image.tmdb.org/t/p/original"
    
    # Parameters for the API request
    params = {
        'api_key': api_key,
        'query': query,
        'language': 'en-US',
        'page': 1,
        'include_adult': False
    }
    
    try:
        # Make the API request
        response = requests.get(search_endpoint, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the response
        results = response.json()['results']
        
        # Extract relevant information
        movies = []
        for movie in results:
            movie_info = {
                'title': movie['title'],
                'original_title': movie.get('original_title', ''),
                'release_date': movie.get('release_date', ''),
                'poster_url': f"{image_base_url}{movie['poster_path']}" if movie.get('poster_path') else None
            }
            movies.append(movie_info)
            
        return movies
        
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return []
    except KeyError as e:
        print(f"Error parsing response: {e}")
        return []