from datetime import datetime

import factory
from oauth2_provider.models import Application
from ib_users.models import UserAccount
from oauth2_provider.models import AccessToken, RefreshToken

from trip.models import Destination, Hotel, Booking


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


class AccessTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AccessToken

    id = factory.Faker('uuid4')
    token = factory.Faker('uuid4')
    expires = datetime.now()
    scope = "read write"
    application = factory.SubFactory(ApplicationFactory)
    user = None
    token_type = "bearer"


class RefreshTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RefreshToken

    id = factory.Faker('uuid4')
    token = factory.Faker('uuid4')
    application = factory.SubFactory(ApplicationFactory)
    user = None
    access_token = factory.SubFactory(AccessTokenFactory)


class UserAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserAccount

    user_id = factory.Faker('uuid4')
    username = factory.Faker('user_name')
    phone_number = factory.Faker('phone_number')
    email = factory.Faker('email')
    is_password_reset = True


class DestinationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Destination

    id = factory.Faker('integer')
    name = factory.Faker('name')
    description = factory.Faker('sentence')
    tags = factory.Faker('sentence')
    user = None



class HotelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Hotel

    id = factory.Faker('integer')
    name = factory.Faker('name')
    description = factory.Faker('sentence')
    tariff = factory.Faker('integer')
    user = None
    destination = factory.SubFactory(DestinationFactory)
    image_urls = factory.Faker('sentence')


class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking

    id = factory.Faker('integer')
    hotel = factory.SubFactory(HotelFactory)
    user = None
    destination = factory.SubFactory(DestinationFactory)
    checkin_date = factory.Faker('date')
    checkout_date = factory.Faker('date')
    tariff = factory.Faker('integer')
    total_amount = factory.Faker('integer')




