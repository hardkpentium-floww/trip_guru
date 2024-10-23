from feasto_core_clean_arch.models import Restaurant
from feasto_gql.restaurant.dataloaders.restaurant_user_loader import RestaurantUserLoader


def resolve_all_restaurants(root, info, **kwargs):
    user_loader = RestaurantUserLoader(context= info.context)
    restaurants = Restaurant.objects.all()
    for restaurant in restaurants:
        restaurant.user = user_loader.load(restaurant.user.id)
    return restaurants