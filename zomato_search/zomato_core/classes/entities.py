class Restaurant:
    def __init__(self):
        self.id = None
        self.name = None
        self.url = None
        self.rating = None
        self.average_cost_for_two = None
        self.thumbnail_url = None
        self.has_online_delivery = None
        self.cuisines = None
        self.phone_numbers = None
        self.address = None
        self.location = None
        self.photos_url = None
        self.menu_url = None


class Cuisine:
    def __init__(self):
        self.id = None
        self.name = None


class Category:
    def __init__(self):
        self.id = None
        self.name = None

class Type:
    def __init__(self):
        self.id = None
        self.name = None
