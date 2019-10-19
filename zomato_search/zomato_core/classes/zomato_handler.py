from django.conf import settings
from zomathon import ZomatoAPI


class NoSearchCriteriaException(Exception):
    pass


class NoMoreResultsException(Exception):
    pass


class ZomatoHandler:
    CITY_ID = 4
    KEY = settings.ZOMATO_KEY

    def __init__(self):
        self.api = ZomatoAPI(key=self.KEY)

    def search(self, q='', categories=None, cuisines=None, types=None, start=0):
        if categories:
            categories = ','.join(categories)
            response = self.api.search(q=q, category=categories, entity_type='city', entity_id=self.CITY_ID, start=start)
        elif cuisines:
            cuisines = ','.join(cuisines)
            response = self.api.search(q=q, cuisines=cuisines, entity_type='city', entity_id=self.CITY_ID, start=start)
        elif types:
            types = ','.join(types)
            response = self.api.search(q=q, establishment_type=types, entity_type='city', entity_id=self.CITY_ID, start=start)
        else:
            raise NoSearchCriteriaException('Invalid search criteria')
        return response

    def get_cuisines(self):
        cuisines = self.api.cuisines(city_id=self.CITY_ID)
        return cuisines

    def get_restaurant_details(self, id):
        restaurant = self.api.restaurant(res_id=id)
        return restaurant

    def get_categories(self):
        categories = self.api.category()
        return categories

    def get_types(self):
        types = self.api.establishments(city_id=self.CITY_ID)
        return types
