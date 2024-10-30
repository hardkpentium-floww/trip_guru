from datetime import datetime, timedelta

import factory
from oauth2_provider.models import Application
from ib_users.models import UserAccount
from oauth2_provider.models import AccessToken, RefreshToken

from trip.models import Destination, Hotel, Booking, User


class ApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Application

    name = factory.Faker('name')
    client_id = factory.Faker('uuid4')
    client_secret = factory.Faker('uuid4')
    redirect_uris = factory.Faker('url')
    user = None
    authorization_grant_type = Application.GRANT_CLIENT_CREDENTIALS
    client_type = Application.CLIENT_CONFIDENTIAL
    skip_authorization = False


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    id = factory.Faker("uuid4")
    name = factory.Faker('user_name')
    phone_no = factory.Faker('phone_number')

class UserAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserAccount

    user_id = factory.Faker("uuid4")
    username = factory.Faker('user_name')
    phone_number = factory.Faker('phone_number')
    email = factory.Faker('email')
    is_password_reset = True



class AccessTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AccessToken

    id = factory.Faker('random_int', min=1, max=10000)
    token = factory.Faker('uuid4')
    expires = datetime.now() + timedelta(days=1)
    scope = "read write"
    application = factory.SubFactory(ApplicationFactory)
    user =  factory.SubFactory(UserAccountFactory)



class RefreshTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RefreshToken

    id = factory.Faker('random_int', min=1, max=10000)
    token = factory.Faker('uuid4')
    application = factory.SubFactory(ApplicationFactory)
    user = factory.SubFactory(UserAccountFactory)
    access_token = factory.SubFactory(AccessTokenFactory)



class DestinationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Destination

    id = factory.Faker('random_int', min=1, max=10000)
    name = factory.Faker('name')
    description = factory.Faker('sentence')
    tags = "beach"
    user = factory.SubFactory(UserFactory)



class HotelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Hotel

    id = factory.Faker('random_int', min=1, max=10000)
    name = factory.Faker('name')
    description = factory.Faker('sentence')
    tariff = factory.Faker('random_int', min=1, max=10000)
    destination = factory.SubFactory(DestinationFactory)
    image_urls = factory.Faker('sentence')


class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking

    id = factory.Faker('random_int', min=1, max=10000)
    hotel = factory.SubFactory(HotelFactory)
    user = factory.SubFactory(UserFactory)
    destination = factory.SubFactory(DestinationFactory)
    checkin_date = factory.LazyFunction(lambda: datetime.now() + timedelta(days=1))
    checkout_date = factory.LazyFunction(lambda: datetime.now() + timedelta(days=2))
    tariff =  factory.Faker('random_int', min=1, max=10000)
    total_amount = factory.Faker('random_int', min=1, max=10000)




