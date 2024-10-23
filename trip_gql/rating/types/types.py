import graphene

from feasto_gql.restaurant.dataloaders.restaurant_user_loader import RestaurantUserLoader
from feasto_gql.order_item.types.types import OrderItem

class User(graphene.ObjectType):
    id = graphene.String(required=True)
    name = graphene.String(required=True)
    phone_no = graphene.String(required=True)
    orders = graphene.List(graphene.Field(Order))

class OrderItem(graphene.ObjectType):
    id = graphene.String(required=True)
    order = graphene.Field(Order)
    order_quantity = graphene.Int(required=True)




class Restaurant(graphene.ObjectType):
    id = graphene.String(required=True)
    name = graphene.String(required=True)
    location = graphene.String(required=True)
    status = graphene.String(required=True)
    user = graphene.Field(User)

    def resolve_user(root, info):
        user_loader = RestaurantUserLoader(context=info.context)
        return user_loader.load(root.user.id)

class AddRestaurantParams(graphene.InputObjectType):
    name = graphene.String(required=True)
    location = graphene.String(required=True)
    status = graphene.String(required=True)

class DeleteRestaurantParams(graphene.InputObjectType):
    id = graphene.String(required=True)
    user_id = graphene.String(required=True)

class GetOrdersResponse(graphene.ObjectType):
    orders = graphene.List(graphene.Int)

class UpdateRestaurantParams(graphene.InputObjectType):
    id = graphene.String(required=True)
    name = graphene.String()
    location = graphene.String()
    status = graphene.String()
    user_id = graphene.String()

    #
    #
    #
    # def resolve_order(self):
    #     loader =

class RestaurantNotFound(graphene.ObjectType):
    restaurant_id = graphene.String()

class GetRestaurantsParams(graphene.InputObjectType):
    limit = graphene.Int(required=True)
    offset = graphene.Int(required=True)
    status = graphene.String()
    location = graphene.String()

class GetRestaurantsResponse(graphene.ObjectType):
    restaurants = graphene.List(Restaurant)



class RestaurantResponse(graphene.Union):
    class Meta:
        types = (Restaurant,RestaurantNotFound)



class GetRestaurantParams(graphene.InputObjectType):
    id = graphene.String(required=True)

class GetRestaurantResponse(graphene.ObjectType):
    class Meta:
        types = (Restaurant,RestaurantNotFound)



