from django.urls import path

from zomato_search.zomato_core.views import RestaurantDetails, Home, SearchCuisine, SearchResults, SearchCategory, \
    SearchType

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('details/<int:id>', RestaurantDetails.as_view(), name='restaurant_details'),
    path('search/cuisine/', SearchCuisine.as_view(), name='search_cuisine'),
    path('search/category/', SearchCategory.as_view(), name='search_category'),
    path('search/type/', SearchType.as_view(), name='search_type'),
    path('search-results/', SearchResults.as_view(), name='search_results')
]
