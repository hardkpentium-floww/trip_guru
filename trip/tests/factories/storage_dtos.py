from datetime import timedelta

import factory


from trip.interactors.storage_interfaces.storage_interface import *


class AccessTokenDTOFactory(factory.Factory):
    class Meta:
        model = AccessTokenDTO

    token = factory.Faker('uuid4')
    user_id = factory.Faker('uuid4')
    application_name = 'trip-guru'
    expires = factory.Faker('date_time')
    scope = 'read write'
    source_refresh_token = factory.Faker('uuid4')

class RefreshTokenDTOFactory(factory.Factory):
    class Meta:
        model = RefreshTokenDTO

    access_token_id =  factory.Faker('uuid4')
    user_id =  factory.Faker('uuid4')
    application_name = 'trip-guru'
    token =  factory.Faker('uuid4')


class AddDestinationDTOFactory(factory.Factory):
    class Meta:
        model = MutateDestinationDTO

    name = factory.Faker('name')
    description = factory.Faker('sentence')
    destination_id = factory.Faker('random_int', min=1, max=10000)
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

    id = factory.Faker('random_int', min=1, max=10000)
    name = factory.Faker('name')
    description = factory.Faker('sentence')
    tags = factory.Faker('sentence')
    user_id = factory.Faker('uuid4')


class HotelDTOFactory(factory.Factory):
    class Meta:
        model = HotelDTO

    id = factory.Faker('random_int', min=1, max=10000)
    name = factory.Faker('name')
    description = factory.Faker('sentence')
    tariff = factory.Faker('random_int', min=1, max=10000)
    image_urls = factory.Faker('sentence')
    destination_id = factory.Faker('random_int', min=1, max=10000)

class AddRatingDTOFactory(factory.Factory):
    class Meta:
        model = MutateRatingDTO

    user_id = factory.Faker('uuid4')
    destination_id = factory.Faker('random_int', min=1, max=10000)
    rating = factory.Faker('random_int', min=1, max=5)
    review = factory.Faker('sentence')

class BookHotelDTOFactory(factory.Factory):
    class Meta:
        model = BookHotelDTO

    hotel_id = factory.Faker('random_int',min=1, max=10000)
    user_id = factory.Faker('uuid4')
    checkin_date = factory.Faker('date_time')
    checkout_date = factory.Faker('date_time')
    destination_id= factory.Faker('random_int',min=1, max=10000)
    total_amount = factory.Faker('random_int',min=1, max=10000)
    tariff = factory.Faker('random_int',min=1, max=10000)

class UpdateBookingDTOFactory(factory.Factory):
    class Meta:
        model = MutateBookingDTO

    booking_id =  factory.Faker('random_int', min=1, max=10000)
    checkin_date = factory.LazyFunction(lambda: datetime.now() + timedelta(days=1))
    checkout_date = factory.LazyFunction(lambda: datetime.now() + timedelta(days=2))
    total_amount =  factory.Faker('random_int', min=1, max=10000)
    
class UpdateDestinationDTOFactory(factory.Factory):
    class Meta:
        model = MutateDestinationDTO

    name = factory.Faker('name')
    description = factory.Faker('sentence')
    tags = factory.Faker('sentence')
    destination_id = factory.Faker('random_int', min=1, max=10000)
    user_id = factory.Faker('uuid4')

class UpdateHotelDTOFactory(factory.Factory):
    class Meta:
        model = MutateHotelDTO

    name = factory.Faker('name')
    description = factory.Faker('sentence')
    tariff =factory.Faker('random_int', min=1, max=10000)
    image_urls = factory.Faker('sentence')
    destination_id = factory.Faker('random_int', min=1, max=10000)
    hotel_id = factory.Faker('random_int', min=1, max=10000)
