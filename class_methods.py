

class Film:
    def __init__ (self, info, proposed_by):
        self.info = info
        self.week_f = False
        self.start = 0
        self.end = 0
        self.ratings = {}
        self.proposed_by = proposed_by
        self.special = False
        self.watched = False
    
    def __str__ (self):
        return self.info
    
    def create_rating (self, user, rating):
        self.ratings[user] = rating

    def set_special (self):
        self.special = True


class Catalogue:
    def __init__ (self):
        self.films = []

    def add_film (self, film):
        if isinstance(film, Film):
            self.films.append(film)
    
    def random_film (self):
        import random
        import datetime as dt

        index = random.randint(0, len(self.films) - 1)
        self.films[index].week_f = True
        self.films[index].start = dt.datetime.today()
        self.films[index].end = dt.datetime.today() + dt.timedelta(days=7)
        return self.films[index]
    
    def check_film (self):
        import datetime as dt
        for film in self.films:
            if film.week_f and film.end < dt.datetime.today():
                film.week_f = False
                film.watched = True
                return True
    
    def save_data(self):
        import pickle
        with open('films.pkl', 'wb') as f:
            pickle.dump(self.films, f)
    
    def import_data(self):
        import pickle
        with open('films.pkl', 'rb') as f:
            self.films = pickle.load(f)
    


    