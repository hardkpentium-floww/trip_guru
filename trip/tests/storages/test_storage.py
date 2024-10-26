from unittest.mock import patch, MagicMock

import pytest

from trip.exceptions.custom_exceptions import InvalidUser, InvalidDestination, BookingScheduleOverlap, NoBookingsExists
from trip.storages.storage_implementation import StorageImplementation
from trip.tests.factories.models import ApplicationFactory, AccessTokenFactory, RefreshTokenFactory, UserAccountFactory, \
    DestinationFactory, HotelFactory, BookingFactory
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
    def test_create_access_token(self, storage):
        # Create a DTO for testing
        access_token_dto = AccessTokenDTOFactory()
        from oauth2_provider.models import AccessToken

        # Mock the user and application retrieval methods
        with patch('trip.storages.storage_implementation.StorageImplementation.get_user_account') as mock_get_user, \
                patch('trip.storages.storage_implementation.StorageImplementation.get_application_instance') as mock_get_app:
            # Create mock user and application objects
            mock_user = UserAccountFactory(user_id = access_token_dto.user_id)
            mock_application = ApplicationFactory(name =  access_token_dto.application_name)

            # Configure the mock return values
            mock_get_user.return_value = mock_user
            mock_get_app.return_value = mock_application

            # Create a mock AccessToken instance
            access_token = storage.create_access_token(access_token_dto=access_token_dto)

            # Assertions to validate the returned access token
            assert access_token.user.user_id == access_token_dto.user_id
            assert access_token.token == access_token_dto.token
            assert access_token.application.name == access_token_dto.application_name
            assert access_token.expires == access_token_dto.expires
            assert access_token.scope == 'read write'

            # Ensure that the helper methods were called
            mock_get_user.assert_called_once_with(user_id=access_token_dto.user_id)
            mock_get_app.assert_called_once_with(application_name=access_token_dto.application_name)



    def test_create_refresh_token(self,
                            storage):
        refresh_token_dto = RefreshTokenDTOFactory()
        with patch('trip.storages.storage_implementation.StorageImplementation.get_application_id') as mock_get_application:

            mock_get_application.return_value = "1"
            # Create a mock RefreshToken instance


            refresh_token = storage.create_refresh_token(refresh_token_dto=refresh_token_dto)

            # Assertions to validate the returned refresh token
            assert refresh_token.token == refresh_token_dto.token
            assert refresh_token.application_id == "1"
            assert refresh_token.access_token_id == refresh_token_dto.access_token_id




    def test_validate_user_id_valid(self,
                            storage):
        with patch('trip.models.user.User') as mock_user:
            mock_user.objects.filter.return_value.exists.return_value = True
            # Call the method with a valid user ID
            storage.validate_user_id(user_id="e9ab68e1-95c2sd-41bc-966d-615a9cfd175d")  # Replace with a valid ID format

            # Ensure no exception is raised
            assert True


    def test_validate_user_id_invalid(self,
                            storage):
        with patch('trip.models.user.User') as mock_user:
            mock_user.objects.filter.return_value.exists.return_value = False
            # Call the method with a valid user ID
            storage.validate_user_id(user_id="e9ab68easdf1-95c2sd-41bc-966d-615a9cfd175d")  # Replace with a valid ID format

            # Ensure no exception is raised
            assert True



    def test_add_destination(self, storage):
        add_destination_dto = AddDestinationDTOFactory()


        destination_dto = storage.add_destination(add_destination_dto=add_destination_dto)

        assert add_destination_dto.descriptiion == destination_dto.id
        assert add_destination_dto.name == destination_dto.name
        assert add_destination_dto.tags == destination_dto.tags
        assert add_destination_dto.user_id == destination_dto.user_id


    def test_validate_admin_user_valid(self, storage):
        with patch("trip.models.user.User") as mock_user:
            mock_user.objects.filter.return_value.exists.return_value= True

            storage.validate_admin_user(user_id = "9ab68e1-95c2sd-41bc-966d-615a9cfd175d")

            assert True

    def test_validate_admin_user_invalid(self, storage):
        with patch("trip.models.user.User") as mock_user:
            mock_user.objects.filter.return_value.exists.return_value = False

            storage.validate_admin_user(user_id="9aasdb68e1-95c2sd-41bc-966d-615a9cfd175d")

            assert True



    def test_validate_destination_id_valid(self, storage):
        with patch("trip.models.destination.Destination") as mock_destination:
            mock_destination.objects.filter.return_value.exists.return_value = True

            storage.validate_destination_id(destination_id=1)

            assert True

    def test_validate_destination_id_invalid(self, storage):
        with patch("trip.models.destination.Destination") as mock_destination:
            mock_destination.objects.filter.return_value.exists.return_value = False

            storage.validate_destination_id(destination_id=1000)

            assert True





    def test_logout(self, storage):
        with patch('oauth2_provider.models.Application') as mock_application:
            mock_application_instance = ApplicationFactory()
            mock_application.objects.get.return_value= mock_application_instance

            with patch('oauth2_provider.models.AccessToken') as mock_access_token:
                mock_access_token_instance = AccessTokenFactory()
                mock_access_token.objects.get.return_value = mock_access_token_instance

                with patch('oauth2_provider.models.RefreshToken') as mock_refresh_token:
                    mock_refresh_token_instance = RefreshTokenFactory()
                    mock_access_token.objects.get.return_value = mock_refresh_token_instance

                    mock_access_token.delete = None
                    mock_refresh_token.delete = None

                    storage.logout(user_id="user_id")

                    mock_application.objects.get.assert_called_once_with(name='trip-guru')
                    mock_access_token.objects.get.assert_called_once_with(user_id="user_id",
                                                                          application=mock_application_instance)
                    mock_refresh_token.objects.get.assert_called_once_with(access_token=mock_access_token_instance)
                    mock_refresh_token_instance.delete.assert_called_once()
                    mock_access_token_instance.delete.assert_called_once()



    def test_get_user_account(self,storage):
        with patch('oauth2_provider.models.UserAccount') as mock_user_account:
            mock_user_account_instance = UserAccountFactory()
            mock_user_account.objects.get.return_value = mock_user_account_instance

            user_account = storage.get_user_account(user_id=mock_user_account_instance.user_id)

            assert mock_user_account_instance.user_id == user_account.user_id



    def test_get_application_instance(self,storage):
        with patch('oauth2_provider.models.Application') as mock_application:
            mock_application_instance = ApplicationFactory()

            mock_application.objects.filter.return_value = mock_application_instance


            application_object = storage.get_application_instance(application_name=mock_application.application_name)


            assert application_object.name == mock_application.application_name


    def test_get_destination(self, storage):
        with patch('trip.models.destination.Destination') as mock_destination:
            mock_destination_instance = DestinationFactory()
            mock_destination.objects.filter.return_value = mock_destination_instance


            destination_dto = storage.get_destination(destination_id=mock_destination.id)

            assert destination_dto.id == mock_destination.id
            assert destination_dto.name == mock_destination.name
            assert destination_dto.description == mock_destination.description
            assert destination_dto.tags == mock_destination.tags
            assert destination_dto.user_id  == mock_destination.user_id




    def test_get_destinations(self, storage):
        get_destinations_dto = GetDestinationsDTOFactory()

        test_destination_dtos = DestinationDTOFactory().create_batch(5)


        destination_dtos = storage.get_destinations(get_destinations_dto=get_destinations_dto)


        for i in range(5):
            assert test_destination_dtos[i].id == destination_dtos[i].id
            assert test_destination_dtos[i].name == destination_dtos[i].name
            assert test_destination_dtos[i].description == destination_dtos[i].description
            assert test_destination_dtos[i].tags == destination_dtos[i].tags
            assert test_destination_dtos[i].user_id == destination_dtos[i].user_id




    def test_validate_hotel_customer(self, storage):
        with patch('trip.models.destination.Destination') as mock_destination:
            mock_destination.objects.filter.return_value.exists.side_effect = [True, False]

            storage.validate_hotel_customer(user_id="valid_user_id", destination_id=1)

        with pytest.raises(InvalidUser):
            storage.validate_hotel_customer(user_id="invalid_user_id", destination_id=1)



    def test_get_hotel(self,storage):
        with patch('trip.models.hotel.Hotel') as mock_hotel:
            mock_hotel_instance = HotelFactory()
            mock_hotel.objects.filter.return_value.all.return_value = mock_hotel_instance




            hotel_dto = storage.get_hotel(hotel_id=1)

            assert hotel_dto.id == mock_hotel.id
            assert hotel_dto.name == mock_hotel.name
            assert hotel_dto.description == mock_hotel.description
            assert hotel_dto.tariff == mock_hotel.tariff
            assert hotel_dto.description_id == mock_hotel.destination_id



    def test_add_hotel(self, storage):
        with patch('trip.models.destination.Destination') as mock_destination:
            mock_destination.objects.filter.return_value.exists.side_effect = [False, True]

            hotel_obj = HotelFactory()
            add_hotel_dto = HotelDTOFactory()
            add_hotel_dto.id = hotel_obj.id,
            add_hotel_dto.name = hotel_obj.name,
            add_hotel_dto.description = hotel_obj.description,
            add_hotel_dto.tariff = hotel_obj.tariff,
            add_hotel_dto.image_urls = hotel_obj.image_urls,
            add_hotel_dto.destination_id = hotel_obj.destination_id

            with pytest.raises(InvalidDestination):
                storage.add_hotel(user_id="invalid_user_id", add_hotel_dto=add_hotel_dto)

            hotel_dto = storage.add_hotel(user_id="valid_user_id", add_hotel_dto=add_hotel_dto)

            assert hotel_dto.id == add_hotel_dto.id
            assert hotel_dto.name == add_hotel_dto.name
            assert hotel_dto.description == add_hotel_dto.description
            assert hotel_dto.tariff == add_hotel_dto.tariff
            assert hotel_dto.description_id == add_hotel_dto.destination_id




    def test_add_rating(self, storage):
        with patch('trip.models.destination.Destination') as mock_destination:
            mock_destination.objects.filter.return_value.exists.side_effect = [False, True]


            add_rating_dto = AddRatingDTOFactory()

            with pytest.raises(InvalidDestination):
                storage.add_rating(add_rating_dto=add_rating_dto)

            rating_dto = storage.add_rating(add_rating_dto=add_rating_dto)

            assert rating_dto.rating == add_rating_dto.rating
            assert rating_dto.user_id == add_rating_dto.user_id
            assert rating_dto.review == add_rating_dto.review
            assert  rating_dto.destination_id == add_rating_dto.destination_id




    def test_book_hotel(self, storage):
        with patch('trip.models.destination.Destination') as mock_destiantion:
            mock_destiantion.objects.filter.return_value.exists.side_effect = [False, True]

            hotel_id = 1
            book_hotel_dto = BookHotelDTOFactory()


            with pytest.raises(InvalidDestination):
                storage.book_hotel(hotel_id=hotel_id, book_hotel_dto=book_hotel_dto)

            with patch('trip.models.booking.Booking') as mock_booking:
                mock_booking.objects.filter.return_value.exists.side_effect = [False, True]

                with pytest.raises(BookingScheduleOverlap):
                    storage.book_hotel(hotel_id=hotel_id, book_hotel_dto=book_hotel_dto)

                booking_dto = storage.book_hotel(hotel_id=hotel_id, book_hotel_dto=book_hotel_dto)

                assert booking_dto.user_id == book_hotel_dto.user_id
                assert booking_dto.hotel_id == book_hotel_dto.hotel_id
                assert booking_dto.checkin_date == book_hotel_dto.checkin_date
                assert booking_dto.checkout_date == book_hotel_dto.checkout_date
                assert booking_dto.total_amount == book_hotel_dto.total_amount
                assert booking_dto.booking_id == book_hotel_dto.id
                assert booking_dto.destination_id == book_hotel_dto.destination_id



    def test_update_booking(self, storage):
        # Mock for the overlapping booking scenario
        with patch('trip.models.booking.Booking') as mock_overlapping_booking:
            update_booking_dto = UpdateBookingDTOFactory()
            booking_id = 1
            # First call: expects a BookingScheduleOverlap exception
            mock_overlapping_booking.objects.filter.return_value.exists.side_effect = [True]

            with pytest.raises(BookingScheduleOverlap):
                storage.update_booking(booking_id=booking_id, update_booking_dto=update_booking_dto)

        # Mock for the actual booking update
        with patch('trip.models.booking.Booking') as mock_booking:
            mock_booking_instance = BookingFactory()
            mock_booking.objects.get.return_value = mock_booking_instance

            # Second call: should succeed and return a booking_dto
            booking_dto = storage.update_booking(booking_id=1, update_booking_dto=update_booking_dto)

            # Assertions to verify the booking_dto
            assert booking_dto.user_id == mock_booking_instance.user_id
            assert booking_dto.hotel_id == mock_booking_instance.hotel_id
            assert booking_dto.checkin_date == mock_booking_instance.checkin_date
            assert booking_dto.checkout_date == mock_booking_instance.checkout_date
            assert booking_dto.total_amount == mock_booking_instance.total_amount
            assert booking_dto.booking_id == mock_booking_instance.id
            assert booking_dto.destination_id == mock_booking_instance.destination_id

    def test_update_destination(self, storage):
        with patch('trip.models.destination.Destination') as mock_destiantion:
            mock_destiantion_instance = DestinationFactory()
            mock_destiantion.objects.filter.return_value = mock_destiantion_instance

            update_destination_dto = UpdateDestinationDTOFactory()

            destination_dto = storage.update_destination(destination_id=mock_destiantion_instance.destination_id, update_destination_dto= update_destination_dto)


            assert destination_dto.id == mock_destiantion_instance.id
            assert destination_dto.name == mock_destiantion_instance.name
            assert destination_dto.description == mock_destiantion_instance.description
            assert destination_dto.tags == mock_destiantion_instance.tags
            assert destination_dto.user_id == mock_destiantion_instance.user_id



    def test_update_hotel(self, storage):
        with patch('trip.models.hotel.Hotel') as mock_hotel:
            mock_hotel_instance = HotelFactory()
            mock_hotel.objects.get.return_value = mock_hotel_instance

            update_hotel_dto = UpdateHotelDTOFactory()

            hotel_dto = storage.update_hotel(hotel_id=1, update_hotel_dto=update_hotel_dto)

            assert hotel_dto.id == update_hotel_dto.id
            assert hotel_dto.destination_id == update_hotel_dto.destination_id
            assert hotel_dto.name == update_hotel_dto.name
            assert hotel_dto.description == update_hotel_dto.description
            assert hotel_dto.image_urls == update_hotel_dto.image_urls
            assert hotel_dto.tariff == update_hotel_dto.tariff


    def test_get_bookings_for_user(self, storage):
        with patch('trip.models.user.User') as mock_user:
            mock_user.objects.filter.return_value.exists.side_effect = [True, False]
            user_id = "valid_user_id"
            offset = 0
            limit = 10
            with pytest.raises(NoBookingsExists):
                storage.get_bookings_for_user(user_id=user_id, offset=offset, limit=limit)

            with patch('trip.models.booking.Booking') as mock_booking:
                mock_booking_instances = BookingFactory().create_batch(5)

                mock_booking.objects.filter.return_value.all.return_value =mock_booking_instances

                booking_dtos = storage.get_bookings_for_user(user_id=user_id, offset=offset, limit=limit)

                assert len(booking_dtos) == len(mock_booking_instances)

                for i in range(5):
                    assert booking_dtos[i].booking_id == mock_booking_instances[i].booking_id
                    assert booking_dtos[i].user_id == mock_booking_instances[i].user_id
                    assert booking_dtos[i].hotel_id == mock_booking_instances[i].hotel_id
                    assert booking_dtos[i].checkin_date == mock_booking_instances[i].checkin_date
                    assert booking_dtos[i].checkout_date == mock_booking_instances[i].checkout_date
                    assert booking_dtos[i].total_amount == mock_booking_instances[i].total_amount
                    assert booking_dtos[i].destination_id == mock_booking_instances[i].destination_id





    def test_get_hotels(self, storage):
        with patch('trip.models.destination.Destination') as mock_destination:

            mock_destination.objects.filter.return_value.exists.return_value = [True, False]

            with pytest.raises(InvalidDestination):
                storage.get_hotels(destination_id=1)


            with patch("trip.models.hotel.Hotel") as mock_hotel:
                mock_hotel_instances = HotelFactory().create_batch(5)

                mock_hotel.objects.filter.return_value = mock_hotel_instances

                hotel_dtos = storage.get_hotels(destination_id=1)

                assert len(hotel_dtos) == len(mock_hotel_instances)

                for i in range(5):
                    assert hotel_dtos[i].id == mock_hotel_instances[i].id
                    assert hotel_dtos[i].name == mock_hotel_instances[i].name
                    assert hotel_dtos[i].description == mock_hotel_instances[i].description
                    assert hotel_dtos[i].tariff == mock_hotel_instances[i].tariff
                    assert hotel_dtos[i].image_urls == mock_hotel_instances[i].image_urls
                    assert hotel_dtos[i].destination_id == mock_hotel_instances[i].destination_id
















