from pymongo import MongoClient
from datetime import datetime, timedelta
import random

class Film:
    def __init__(self, info, proposed_by):
        self.info = info
        self.week_f = False
        self.start = None
        self.end = None
        self.ratings = {}
        self.proposed_by = proposed_by
        self.special = False
        self.watched = False
    
    def __str__(self):
        return self.info
    
    def to_dict(self):
        return {
            'info': self.info,
            'week_f': self.week_f,
            'start': self.start,
            'end': self.end,
            'ratings': self.ratings,
            'proposed_by': self.proposed_by,
            'special': self.special,
            'watched': self.watched
        }
    
    @classmethod
    def from_dict(cls, data):
        film = cls(data['info'], data['proposed_by'])
        film.week_f = data['week_f']
        film.start = data['start']
        film.end = data['end']
        film.ratings = data['ratings']
        film.special = data['special']
        film.watched = data['watched']
        return film
    
    def create_rating(self, user, rating):
        self.ratings[user] = rating
    
    def set_special(self):
        self.special = True

class Catalogue:
    def __init__(self, mongodb_uri="mongodb+srv://user:So6fB5dMOkCcQiTl@cluster0.mxnrotu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"):
        self.client = MongoClient(mongodb_uri)
        self.db = self.client['film_catalogue']
        self.collection = self.db['films']
    
    def add_film(self, film):
        if isinstance(film, Film):
            self.collection.insert_one(film.to_dict())
    
    def random_film(self):
        pipeline = [
            {'$match': {'week_f': False, 'watched': False}},
            {'$sample': {'size': 1}}
        ]
        film_doc = list(self.collection.aggregate(pipeline))
        
        if not film_doc:
            return None
            
        film = Film.from_dict(film_doc[0])
        film.week_f = True
        film.start = datetime.now()
        film.end = datetime.now() + timedelta(days=7)
        
        self.collection.update_one(
            {'info': film.info},
            {'$set': {
                'week_f': True,
                'start': film.start,
                'end': film.end
            }}
        )
        return film
    
    def check_film(self):
        result = self.collection.update_many(
            {
                'week_f': True,
                'end': {'$lt': datetime.now()}
            },
            {
                '$set': {
                    'week_f': False,
                    'watched': True
                }
            }
        )
        return result.modified_count > 0
    
    def get_all_films(self):
        return [Film.from_dict(doc) for doc in self.collection.find()]
    
    def close(self):
        self.client.close()

# Usage example:
if __name__ == "__main__":
    catalogue = Catalogue()
    
    # Add a film
    new_film = Film("The Matrix", "John")
    catalogue.add_film(new_film)
    
    # Get random film
    weekly_film = catalogue.random_film()
    
    # Check expired films
    catalogue.check_film()
    
    # Clean up
    catalogue.close()