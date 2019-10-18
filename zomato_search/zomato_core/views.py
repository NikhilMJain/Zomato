from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View

from zomato_search.zomato_core.classes.entities import Restaurant, Cuisine, Category, Type
from zomato_search.zomato_core.classes.zomato_handler import ZomatoHandler, NoSearchCriteriaException, \
    NoMoreResultsException
from zomato_search.zomato_core.forms.review_form import ReviewForm
from zomato_search.zomato_core.models import Review


class Home(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'home.html', {})


class SearchCuisine(LoginRequiredMixin, View):
    def get(self, request):
        cuisines = self._get_cuisines()
        context = {'items': cuisines}
        return render(request, 'search_cuisine.html', context)

    def _get_cuisines(self):
        cuisines = list()
        data = ZomatoHandler().get_cuisines()
        for item in data['cuisines']:
            cuisine = Cuisine()
            item_dict = item['cuisine']
            cuisine.id = item_dict['cuisine_id']
            cuisine.name = item_dict['cuisine_name']
            cuisines.append(cuisine)
        return cuisines


class SearchCategory(LoginRequiredMixin, View):
    def get(self, request):
        categories = self._get_categories()
        context = {'items': categories}
        return render(request, 'search_category.html', context)

    def _get_categories(self):
        categories = list()
        data = ZomatoHandler().get_categories()
        for item in data['categories']:
            category = Category()
            item_dict = item['categories']
            category.id = item_dict['id']
            category.name = item_dict['name']
            categories.append(category)
        return categories


class SearchType(LoginRequiredMixin, View):
    def get(self, request):
        types = self._get_types()
        context = {'items': types}
        return render(request, 'search_type.html', context)

    def _get_types(self):
        types = list()
        data = ZomatoHandler().get_types()
        for item in data['establishments']:
            type = Type()
            item_dict = item['establishment']
            type.id = item_dict['id']
            type.name = item_dict['name']
            types.append(type)
        return types


class SearchResults(LoginRequiredMixin, View):
    def post(self, request):
        by = request.POST.get('by')
        ids = request.POST.getlist('ids')
        search_text = request.POST.get('search_dish')

        try:
            if 'next' not in request.POST and 'previous' not in request.POST:
                kwargs = {by: ids}
                data = ZomatoHandler().search(q=search_text, **kwargs)
                next_value = data['results_shown'] + 1
                previous_value = 0
            elif 'next' in request.POST:
                kwargs = {by: ids, 'start': request.POST.get('next_page')}
                data = ZomatoHandler().search(q=search_text, **kwargs)
                next_value = int(request.POST.get('next_page')) + data['results_shown']
                previous_value = int(request.POST.get('previous_page')) + 20
            else:
                kwargs = {by: ids, 'start': int(request.POST.get('previous_page')) - 20}
                data = ZomatoHandler().search(q=search_text, **kwargs)
                next_value = int(request.POST.get('next_page')) - data['results_shown']
                previous_value = int(request.POST.get('previous_page')) - 20

        except NoSearchCriteriaException:
            message = 'Select at least one item'
            messages.error(request, message)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        try:
            context = self._get_context(data, next_value, previous_value, by, ids)
        except NoMoreResultsException:
            return HttpResponse('End of results')

        return render(request, 'search_results.html', context)

    def _get_context(self, data, next_value, previous_value, by, ids):
        context = {
            'restaurants': self._get_restaurants(data),
            'next': self._get_next(data),
            'previous': self._previous(data),
            'next_value': next_value,
            'previous_value': previous_value,
            'search_by': by,
            'ids': ','.join(ids)
        }
        return context

    def _get_restaurants(self, data):
        restaurants = list()
        for item in data['restaurants']:
            restaurant = Restaurant()
            item = item['restaurant']
            restaurant.id = item['id']
            restaurant.name = item['name']
            restaurant.url = item['url'].split('?')[0]
            restaurant.has_online_delivery = item['has_online_delivery']
            restaurant.cuisines = item['cuisines']
            restaurant.average_cost_for_two = item['average_cost_for_two']
            restaurant.phone_numbers = item['phone_numbers']
            restaurant.thumbnail_url = item['thumb']
            restaurant.location = item['location']['locality']
            restaurants.append(restaurant)
        return restaurants

    def _get_next(self, data):
        if data['results_shown'] == 0:
            raise NoMoreResultsException('No Results')
        return data['results_shown'] == 20

    def _previous(self, data):
        return data['results_start'] != 0


class RestaurantDetails(LoginRequiredMixin, View):
    def get(self, request, id):
        context = self._get_context(id)
        return render(request, 'restaurant_details.html', context)

    def post(self, request, id):
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            self._save_review(id, form.cleaned_data, request.user)
            context = self._get_context(id)
            return render(request, 'restaurant_details.html', context)

    def _get_reviews(self, id):
        return list(Review.objects.filter(restaurant_id=id))

    def _get_restaurant_details(self, id):
        details = ZomatoHandler().get_restaurant_details(id)
        restaurant = Restaurant()
        restaurant.id = id
        restaurant.name = details['name']
        restaurant.url = details['url'].split('?')[0]
        restaurant.has_online_delivery = details['has_online_delivery']
        restaurant.cuisines = details['cuisines']
        restaurant.average_cost_for_two = details['average_cost_for_two']
        restaurant.phone_numbers = details['phone_numbers']
        restaurant.thumbnail_url = details['featured_image']
        restaurant.address = details['location']['address']
        restaurant.rating = details['user_rating']['aggregate_rating']
        restaurant.photos_url = details['photos_url']
        restaurant.menu_url = details['menu_url']

        return restaurant

    def _save_review(self, id, data, user):
        defaults = {'rating': data['rating'],
                  'text': data['text']}
        kwargs = {'restaurant_id': id, 'user': user}

        Review.objects.update_or_create(defaults=defaults, **kwargs)

    def _get_context(self, id):
        reviews = self._get_reviews(id)
        context = {
            'restaurant': self._get_restaurant_details(id),
            'reviews': reviews,
            'review_form': ReviewForm()
        }
        return context
