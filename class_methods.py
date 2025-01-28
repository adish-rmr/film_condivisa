from pymongo import MongoClient

class Film:
    def __init__(self, titolo, anno, title, poster, proposed_by, in_visione=False, watched=False, rating={}):
        self.info = titolo
        self.anno = anno
        self.title = title
        self.poster = poster
        self.proposed_by = proposed_by
        self.in_visione = in_visione
        self.watched = watched
        self.rating = rating
    
    def to_dict(self):
        return {
            'titolo': self.info,
            'anno': self.anno,
            'title': self.title,
            'poster': self.poster,
            'proposed_by': self.proposed_by,
            'in_visione': self.in_visione,
            'watched': self.watched,
            'rating': self.rating
        }