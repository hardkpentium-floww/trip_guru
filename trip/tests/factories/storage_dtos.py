
import factory


from trip.interactors.storage_interfaces.storage_interface import *


class AccessTokenDTOFactory(factory.Factory):
    class Meta:
        model = AccessTokenDTO

    token = factory.Faker('uuid4')
    user_id = "e9ab68e1-95c2-41bc-966d-615a9cfd175d"
    application_name = 'trip-guru'
    expires = factory.Faker('date_time')
    scope = 'read write'
    source_refresh_token = factory.Faker('uuid4')


class RefreshTokenDTOFactory(factory.Factory):
    class Meta:
        model = RefreshTokenDTO

    access_token_id = factory.Faker('integer')
    user_id = factory.Faker('uuid4')
    application_name = 'trip-guru'
    token = factory.Faker('uuid4')


class AddDestinationDTOFactory(factory.Factory):
    class Meta:
        model = MutateDestinationDTO

    name = factory.Faker('name')
    description = factory.Faker('sentence')
    destination_id = 1
    user_id = factory.Faker('uuid4')
    tags = factory.Faker('sentence')

class GetDestinationsDTOFactory(factory.Factory):
    class Meta:
        model = GetDestinationsDTO

    offset = 0
    limit = 10
    tag = 'beach'

class DestinationDTOFactory(factory.Factory):
    class Meta:
        model = DestinationDTO

    id = factory.Faker('integer')
    name = factory.Faker('name')
    description = factory.Faker('sentence')
    tags = factory.Faker('sentence')
    user_id = factory.Faker('uuid4')


class HotelDTOFactory(factory.Factory):
    class Meta:
        model = HotelDTO

    id = factory.Faker('uuid4')
    name = factory.Faker('name')
    description = factory.Faker('sentence')
    tariff = factory.Faker('sentence')
    image_urls = factory.Faker('sentence')
    destination_id = factory.Faker('integer')

class AddRatingDTOFactory(factory.Factory):
    class Meta:
        model = MutateRatingDTO

    user_id = factory.Faker('uuid4')
    destination_id = factory.Faker('integer')
    rating = factory.Faker('sentence')
    review = factory.Faker('sentence')

class BookHotelDTOFactory(factory.Factory):
    class Meta:
        model = BookHotelDTO

    hotel_id = factory.Faker('integer')
    user_id = factory.Faker('uuid4')
    checkin_date = factory.Faker('date_time')
    checkout_date = factory.Faker('date_time')
    total_amount = factory.Faker('sentence')
    tariff = factory.Faker('integer')
    

class UpdateBookingDTOFactory(factory.Factory):
    class Meta:
        model = MutateBookingDTO

    booking_id = factory.Faker('uuid4')
    checkin_date = factory.Faker('date_time')
    checkout_date = factory.Faker('date_time')
    total_amount = factory.Faker('sentence')
    
class UpdateDestinationDTOFactory(factory.Factory):
    class Meta:
        model = MutateDestinationDTO

    name = factory.Faker('name')
    description = factory.Faker('sentence')
    tags = factory.Faker('sentence')
    id = factory.Faker('integer')
    user_id = factory.Faker('uuid4')

class UpdateHotelDTOFactory(factory.Factory):
    class Meta:
        model = MutateHotelDTO

    name = factory.Faker('name')
    description = factory.Faker('sentence')
    tariff = factory.Faker('integer')
    image_urls = factory.Faker('sentence')
    destination_id = factory.Faker('integer')
    id = factory.Faker('int')
    user_id = factory.Faker('uuid4')