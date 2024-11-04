from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from trip.exceptions.custom_exceptions import InvalidUser, InvalidDestination, BookingScheduleOverlap, NoBookingsExists, \
    InvalidAdminUser
from trip.storages.storage_implementation import StorageImplementation
from trip.tests.factories.models import ApplicationFactory, AccessTokenFactory, RefreshTokenFactory, UserAccountFactory, \
    DestinationFactory, HotelFactory, BookingFactory,UserFactory
from trip.tests.factories.storage_dtos import AccessTokenDTOFactory, RefreshTokenDTOFactory, AddDestinationDTOFactory, \
    GetDestinationsDTOFactory, DestinationDTOFactory, HotelDTOFactory, AddRatingDTOFactory, BookHotelDTOFactory, \
    UpdateBookingDTOFactory, UpdateDestinationDTOFactory, UpdateHotelDTOFactory
from trip_guru.wsgi import application


@pytest.mark.django_db
class TestStorageImplementation:

    @pytest.fixture
    def storage(self):
        storage = StorageImplementation()
        return storage

    @pytest.mark.django_db
    @patch.object(StorageImplementation, 'get_application_instance')
    @patch.object(StorageImplementation, 'get_user_account')
    def test_create_access_token(self,mock_get_user, mock_get_app,storage):
        # Arrange
        access_token_dto = AccessTokenDTOFactory()

        mock_user = UserAccountFactory(user_id=access_token_dto.user_id)
        mock_application = ApplicationFactory(name=access_token_dto.application_name)

        mock_get_user.return_value = mock_user
        mock_get_app.return_value = mock_application

        # Act
        access_token = storage.create_access_token(access_token_dto=access_token_dto)

        # Assert
        assert access_token.user.user_id == access_token_dto.user_id
        assert access_token.token == access_token_dto.token
        assert access_token.application.name == access_token_dto.application_name
        assert access_token.expires == access_token_dto.expires
        assert access_token.scope == 'read write'

        mock_get_user.assert_called_once_with(user_id=access_token_dto.user_id)
        mock_get_app.assert_called_once_with(application_name=access_token_dto.application_name)

    @patch.object(StorageImplementation, 'get_application_id')
    def test_create_refresh_token(self, mock_get_application_id,
                            storage):
        # Arrange
        user_id = UserAccountFactory().user_id
        application = ApplicationFactory(name = 'trip-guru')
        access_token = AccessTokenFactory(application=application)
        refresh_token_dto = RefreshTokenDTOFactory(token = access_token.token, user_id = user_id, application_name=application.name, access_token_id = access_token.id)

        mock_get_application_id.return_value = "1"

        # Act
        refresh_token = storage.create_refresh_token(refresh_token_dto=refresh_token_dto)

        # Assert
        assert refresh_token.token == refresh_token_dto.token
        assert refresh_token.application_id == "1"
        assert refresh_token.access_token_id == refresh_token_dto.access_token_id


    def test_validate_user_id_valid(self,
                            storage):
        # Arrange
        user = UserAccountFactory(user_id="550e8400-e29b-41d4-a716-446655440000")

        #Act
        storage.validate_user_id(user_id=user.user_id)  # Replace with a valid ID format

        # Assert
        assert True


    def test_validate_user_id_invalid(self,
                            storage):
        # Arrange
        user = UserAccountFactory(user_id="550e8400-b29b-41d4-a716-446655440000")

        # Act
        with pytest.raises(InvalidUser):
            storage.validate_user_id(user_id="550e8400-b29c-41d4-a716-446655440000")

        # Assert
        assert True


    def test_add_destination(self, storage):
        # Arrange
        user_id = UserFactory().id
        add_destination_dto = AddDestinationDTOFactory(user_id=user_id)

        # Act
        destination_dto = storage.add_destination(add_destination_dto=add_destination_dto)

        # Assert
        assert add_destination_dto.description == destination_dto.description
        assert add_destination_dto.name == destination_dto.name
        assert add_destination_dto.tags == destination_dto.tags
        assert add_destination_dto.user_id == destination_dto.user_id


    def test_validate_admin_user_valid(self, storage):
        # Arrange
        user_id = "e9ab68e1-95c2-41bc-966d-615a9cfd175d"
        #Act
        storage.validate_admin_user(user_id =user_id)

        # Assert
        assert True


    def test_validate_admin_user_invalid(self, storage):
        # Arrange
        user_id = "9aasdb68e1-95c2sd-41bc-966d-615a9cfd175d"
        #Act
        with pytest.raises(InvalidAdminUser):
            storage.validate_admin_user(user_id=user_id)

        # Assert
        assert True

    def test_validate_destination_id_valid(self, storage):
        # Arrange
        destination = DestinationFactory()

        #Act
        storage.validate_destination_id(destination_id=destination.id)

        # Assert
        assert True

    def test_validate_destination_id_invalid(self, storage):
        # Arrange
        destination = DestinationFactory()

        # Act
        with pytest.raises(InvalidDestination):
            storage.validate_destination_id(destination_id=1000)

        # Assert
        assert True


    def test_logout(self, storage):
        # Arrange
        mock_application = ApplicationFactory(name='trip-guru')
        mock_user = UserAccountFactory()
        mock_access_token = AccessTokenFactory(user_id = mock_user.user_id)
        mock_refresh_token = RefreshTokenFactory(token = mock_access_token.token, user = mock_user, access_token_id = mock_access_token.id)

        # Act
        storage.logout(user_id=mock_user.user_id)

        # Assert
        assert True

    def test_get_user_account(self,storage):
        # Arrange
        mock_user_account = UserAccountFactory()

        #Act
        user_account = storage.get_user_account(user_id=mock_user_account.user_id)

        #Assert
        assert mock_user_account.user_id == str(user_account.user_id)



    def test_get_application_instance(self,storage):
        # Arrange
        mock_application= ApplicationFactory()

        #Act
        application_object = storage.get_application_instance(application_name=mock_application.name)

        #Assert
        assert application_object.name == mock_application.name



    def test_get_destination(self, storage):
        # Arrange
        mock_destination= DestinationFactory()

        # Act
        destination_dto = storage.get_destination(destination_id=mock_destination.id)

        # Assert
        assert destination_dto.id == mock_destination.id
        assert destination_dto.name == mock_destination.name
        assert destination_dto.description == mock_destination.description
        assert destination_dto.tags == mock_destination.tags
        assert destination_dto.user_id  == mock_destination.user_id




    def test_get_destinations(self, storage):
        # Arrange
        destinations = DestinationFactory.create_batch(5)
        get_destinations_dto = GetDestinationsDTOFactory()

        test_destination_dtos=sorted(destinations, key=lambda x: x.id)

        #Act
        destination_dtos = storage.get_destinations(get_destinations_dto=get_destinations_dto)
        destination_dtos = sorted(destination_dtos, key=lambda x: x.id)

        #Assert
        assert len(destination_dtos) == len(test_destination_dtos)

        for i in range(5):
            assert test_destination_dtos[i].id == destination_dtos[i].id
            assert test_destination_dtos[i].name == destination_dtos[i].name
            assert test_destination_dtos[i].description == destination_dtos[i].description
            assert test_destination_dtos[i].tags == destination_dtos[i].tags
            assert test_destination_dtos[i].user_id == destination_dtos[i].user_id




    def test_validate_hotel_customer_valid(self, storage):
        # Arrange
        user = UserFactory()
        mock_destination = DestinationFactory(user_id=user.id, id=1)

        #Act
        storage.validate_hotel_customer(user_id=user.id, destination_id=1)

        #Assert
        assert True

    def test_validate_hotel_customer_invalid(self, storage):
        # Arrange
        user = UserFactory()
        mock_destination = DestinationFactory(user_id=user.id, id=1)

        #Act
        with pytest.raises(InvalidUser):
            storage.validate_hotel_customer(user_id="invalid_user_id", destination_id=1)

        #Assert
        assert True



    def test_get_hotel(self,storage):
        # Arrange
        mock_hotel = HotelFactory()

        #Act
        hotel_dto = storage.get_hotel(hotel_id=mock_hotel.id)

        #Assert
        assert hotel_dto.id == mock_hotel.id
        assert hotel_dto.name == mock_hotel.name
        assert hotel_dto.description == mock_hotel.description
        assert hotel_dto.tariff == mock_hotel.tariff
        assert hotel_dto.destination_id == mock_hotel.destination_id



    def test_add_hotel(self, storage):
        # Arrange
        add_hotel_dto = HotelDTOFactory()
        invalid_hotel_dto = HotelDTOFactory()
        user = UserFactory(id = "valid_user_id")
        destination = DestinationFactory(id=add_hotel_dto.destination_id, user_id="valid_user_id")

        #Act
        with pytest.raises(InvalidDestination):
            storage.add_hotel(user_id="valid_user_id", add_hotel_dto=invalid_hotel_dto)

        with pytest.raises(InvalidAdminUser):
            storage.add_hotel(user_id="invalid_user_id", add_hotel_dto=add_hotel_dto)

        #Assert
        hotel_dto = storage.add_hotel(user_id="valid_user_id", add_hotel_dto=add_hotel_dto)

        assert hotel_dto.name == add_hotel_dto.name
        assert hotel_dto.description == add_hotel_dto.description
        assert hotel_dto.tariff == add_hotel_dto.tariff
        assert hotel_dto.destination_id == add_hotel_dto.destination_id


    def test_add_hotels(self, storage):
        # Arrange
        add_hotels_dto = HotelDTOFactory.create_batch(5, destination_id=1)
        user_id = UserFactory().id
        mock_destination = DestinationFactory(user_id=user_id, id=1)

        #Act
        hotel_dtos = storage.add_hotels(user_id=user_id, add_hotel_dtos=add_hotels_dto, destination_id=1)

        #Assert
        assert len(hotel_dtos) == len(add_hotels_dto)

        for i in range(5):
            assert add_hotels_dto[i].name == hotel_dtos[i].name
            assert add_hotels_dto[i].description == hotel_dtos[i].description
            assert add_hotels_dto[i].tariff == hotel_dtos[i].tariff
            assert add_hotels_dto[i].destination_id == hotel_dtos[i].destination_id

    def test_add_rating(self, storage):
        # Arrange
        mock_destination = DestinationFactory()
        mock_user = UserFactory()
        add_rating_dto = AddRatingDTOFactory(destination_id = mock_destination.id, user_id = mock_user.id)
        invalid_rating_dto = AddRatingDTOFactory(destination_id = 1)

        #Act
        with pytest.raises(InvalidDestination):
            storage.add_rating(add_rating_dto=invalid_rating_dto)

        rating_dto = storage.add_rating(add_rating_dto=add_rating_dto)

        #Assert
        assert rating_dto.rating == add_rating_dto.rating
        assert rating_dto.user_id == add_rating_dto.user_id
        assert rating_dto.review == add_rating_dto.review
        assert  rating_dto.destination_id == add_rating_dto.destination_id




    def test_book_hotel(self, storage):
        # Arrange
        mock_destiantion= DestinationFactory()
        mock_user = UserFactory()
        mock_hotel = HotelFactory(destination_id=mock_destiantion.id)
        book_hotel_dto = BookHotelDTOFactory(user_id = mock_user.id, destination_id = mock_destiantion.id, hotel_id = mock_hotel.id)
        invalid_destination_hotel_dto = BookHotelDTOFactory(user_id = mock_user.id, destination_id = 1, hotel_id = 1)

        #Act
        with pytest.raises(InvalidDestination):
            storage.book_hotel(hotel_id=book_hotel_dto.hotel_id, book_hotel_dto=invalid_destination_hotel_dto)

        booking_dto = storage.book_hotel(hotel_id=mock_hotel.id, book_hotel_dto=book_hotel_dto)

        #Assert
        assert booking_dto.user_id == book_hotel_dto.user_id
        assert booking_dto.hotel_id == book_hotel_dto.hotel_id
        assert booking_dto.checkin_date == book_hotel_dto.checkin_date
        assert booking_dto.checkout_date == book_hotel_dto.checkout_date
        assert booking_dto.total_amount == book_hotel_dto.total_amount
        assert booking_dto.destination_id == book_hotel_dto.destination_id



    def test_update_booking(self, storage):
        # Arrange
        mock_booking = BookingFactory(checkin_date = datetime.now() + timedelta(days=1), checkout_date = datetime.now() + timedelta(days=2))

        update_booking_dto = UpdateBookingDTOFactory(user_id = mock_booking.user_id, checkin_date = datetime.now() + timedelta(days=3), checkout_date = datetime.now() + timedelta(days=5))
        invalid_booking_dto = UpdateBookingDTOFactory(user_id = mock_booking.user_id,checkin_date = datetime.now() + timedelta(days=1), checkout_date = datetime.now() + timedelta(days=2))

        #Act
        with pytest.raises(BookingScheduleOverlap):
            storage.update_booking(booking_id=mock_booking.id, update_booking_dto=invalid_booking_dto)

        booking_dto = storage.update_booking(booking_id=mock_booking.id, update_booking_dto=update_booking_dto)

        # Assert
        assert booking_dto.checkin_date == update_booking_dto.checkin_date
        assert booking_dto.checkout_date == update_booking_dto.checkout_date
        assert booking_dto.total_amount == update_booking_dto.total_amount
        assert booking_dto.booking_id == mock_booking.id

    def test_update_destination(self, storage):
        # Arrange
        mock_destiantion = DestinationFactory()
        update_destination_dto = UpdateDestinationDTOFactory(user_id = mock_destiantion.user_id)

        #Act
        destination_dto = storage.update_destination(destination_id=mock_destiantion.id, update_destination_dto= update_destination_dto)

        # Assert
        assert destination_dto.name == update_destination_dto.name
        assert destination_dto.description == update_destination_dto.description
        assert destination_dto.tags == update_destination_dto.tags
        assert destination_dto.user_id == update_destination_dto.user_id



    def test_update_hotel(self, storage):
        # Arrange
        mock_hotel = HotelFactory()
        update_hotel_dto = UpdateHotelDTOFactory(hotel_id=mock_hotel.id, destination_id = mock_hotel.destination_id )

        #Act
        hotel_dto = storage.update_hotel(hotel_id=mock_hotel.id, update_hotel_dto=update_hotel_dto)

        #Assert
        assert hotel_dto.id == update_hotel_dto.hotel_id
        assert hotel_dto.destination_id == update_hotel_dto.destination_id
        assert hotel_dto.name == update_hotel_dto.name
        assert hotel_dto.description == update_hotel_dto.description
        assert hotel_dto.image_urls == update_hotel_dto.image_urls
        assert hotel_dto.tariff == update_hotel_dto.tariff


    def test_get_bookings_for_user(self, storage):
        # Arrange
        mock_user= UserFactory()
        mock_booking = BookingFactory.create_batch(5, user_id=mock_user.id)

        # Act
        # with pytest.raises(NoBookingsExists):
        #     storage.get_bookings_for_user(user_id=mock_user.id, offset=0, limit=10)


        booking_dtos = storage.get_bookings_for_user(user_id=mock_user.id, offset=0, limit=10)
        mock_booking = sorted(mock_booking, key=lambda x: x.id)
        booking_dtos = sorted(booking_dtos, key=lambda x: x.booking_id)

        #Assert
        assert len(booking_dtos) == len(mock_booking)

        for i in range(5):
            assert booking_dtos[i].booking_id == mock_booking[i].id
            assert booking_dtos[i].user_id == mock_booking[i].user_id
            assert booking_dtos[i].checkin_date == mock_booking[i].checkin_date
            assert booking_dtos[i].checkout_date == mock_booking[i].checkout_date
            assert booking_dtos[i].total_amount == mock_booking[i].total_amount
            assert booking_dtos[i].destination_id == mock_booking[i].destination_id





    def test_get_hotels(self, storage):
        # Arrange

        mock_destinations = DestinationFactory.create_batch(5)
        mock_hotels = HotelFactory.create_batch(5, destination_id=mock_destinations[0].id)
        destination_ids = [
            destination.id for destination in mock_destinations
        ]
        
        
        
        # Act
        with pytest.raises(InvalidDestination):
            storage.get_hotels(destination_ids=[1,2])

        hotel_dtos = storage.get_hotels(destination_ids=destination_ids)

        hotel_dtos = sorted(hotel_dtos, key=lambda x: x.id)
        mock_hotels = sorted(mock_hotels, key=lambda x: x.id)

        # Assert
        assert len(hotel_dtos) == len(mock_hotels)

        for i in range(5):
            assert hotel_dtos[i].id == mock_hotels[i].id
            assert hotel_dtos[i].name == mock_hotels[i].name
            assert hotel_dtos[i].description == mock_hotels[i].description
            assert hotel_dtos[i].tariff == mock_hotels[i].tariff
            assert hotel_dtos[i].image_urls == mock_hotels[i].image_urls
            assert hotel_dtos[i].destination_id == mock_hotels[i].destination_id
















