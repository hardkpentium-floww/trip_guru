import json
from unittest.mock import create_autospec
import pytest

from trip.exceptions.custom_exceptions import InvalidAdminUser, InvalidUser
from trip.interactors.add_destination_interactor import AddDestinationInteractor
from trip.interactors.add_hotel_interactor import AddHotelInteractor
from trip.interactors.add_rating_interactor import AddRatingInteractor
from trip.interactors.book_hotel_interactor import BookHotelInteractor
from trip.interactors.get_destinations_interactor import GetDestinationsInteractor
from trip.interactors.login_interactor import LoginInteractor
from trip.interactors.storage_interfaces.storage_interface import StorageInterface, HotelDTO, MutateHotelDTO, \
    MutateRatingDTO, RatingDTO, BookHotelDTO, DestinationDTO
from trip.models import Destination
from trip.tests.factories.storage_dtos import AddDestinationDTOFactory, DestinationDTOFactory, HotelDTOFactory, \
    AddRatingDTOFactory, BookHotelDTOFactory, GetDestinationsDTOFactory


class TestInteractor:
    @pytest.fixture
    def storage(self):
        storage = create_autospec(StorageInterface)
        return storage


    def test_add_destination(self, storage):
        interactor = AddDestinationInteractor(storage=storage)
        add_destination_dto = AddDestinationDTOFactory()

        storage.add_destination.return_value = DestinationDTOFactory(
            description=add_destination_dto.description,
            name=add_destination_dto.name,
            tags=add_destination_dto.tags,
            user_id=add_destination_dto.user_id
        )

        destination_dto = interactor.add_destination(add_destination_dto=add_destination_dto)

        storage.add_destination.assert_called_once_with(add_destination_dto=add_destination_dto)
        assert destination_dto.description == add_destination_dto.description
        assert destination_dto.name == add_destination_dto.name
        assert destination_dto.tags == add_destination_dto.tags
        assert destination_dto.user_id == add_destination_dto.user_id

    def test_add_hotel(self, storage):
        interactor = AddHotelInteractor(storage=storage)
        add_hotel_dto = HotelDTOFactory()

        storage.add_hotel.return_value = HotelDTO(
            id= add_hotel_dto.id,
            description=add_hotel_dto.description,
            name=add_hotel_dto.name,
            tariff=add_hotel_dto.tariff,
            image_urls=add_hotel_dto.image_urls,
            destination_id = add_hotel_dto.destination_id
        )

        storage.validate_admin_user.side_effect = [InvalidAdminUser, True]
        with pytest.raises(InvalidAdminUser):
            hotel_dto = interactor.add_hotel(user_id="e9ab68e1-93c2-41bc-966d-615a9cfd175d", add_hotel_dto=add_hotel_dto)

        hotel_dto = interactor.add_hotel(user_id="e9ab68e1-95c2-41bc-966d-615a9cfd175d", add_hotel_dto=add_hotel_dto)
        storage.add_hotel.assert_called_once_with(user_id="e9ab68e1-95c2-41bc-966d-615a9cfd175d",add_hotel_dto=add_hotel_dto)
        assert hotel_dto.description == add_hotel_dto.description
        assert hotel_dto.name == add_hotel_dto.name
        assert  hotel_dto.id == add_hotel_dto.id
        assert hotel_dto.tariff == add_hotel_dto.tariff
        assert hotel_dto.image_urls == add_hotel_dto.image_urls
        assert hotel_dto.destination_id == add_hotel_dto.destination_id


    def test_add_rating(self, storage):
        interactor = AddRatingInteractor(storage=storage)

        add_rating_dto = AddRatingDTOFactory()
        storage.validate_hotel_customer.side_effect = [InvalidUser, True]

        storage.add_rating.return_value = MutateRatingDTO(
                 user_id =add_rating_dto.user_id,
                 review =add_rating_dto.review,
                 destination_id =add_rating_dto.destination_id,
                 rating = add_rating_dto.rating
                )

        with pytest.raises(InvalidUser):
            rating_dto = interactor.add_rating(add_rating_dto=add_rating_dto)

        rating_dto = interactor.add_rating(add_rating_dto=add_rating_dto)

        assert storage.validate_hotel_customer.call_count == 2
        assert rating_dto.user_id == add_rating_dto.user_id
        assert rating_dto.review == add_rating_dto.review
        assert rating_dto.destination_id == add_rating_dto.destination_id
        assert rating_dto.rating == add_rating_dto.rating




    def test_book_hotel(self, storage):
        interactor = BookHotelInteractor(storage=storage)
        book_hotel_dto = BookHotelDTOFactory()

        storage.book_hotel.return_value = BookHotelDTO(
            hotel_id=book_hotel_dto.hotel_id,
            checkin_date=book_hotel_dto.checkin_date,
            checkout_date=book_hotel_dto.checkout_date,
            total_amount=book_hotel_dto.total_amount,
            user_id=book_hotel_dto.user_id,
            tariff=book_hotel_dto.tariff,
            destination_id = book_hotel_dto.destination_id
        )

        hotel_dto = interactor.book_hotel(hotel_id=book_hotel_dto.hotel_id, book_hotel_dto=book_hotel_dto)

        storage.book_hotel.assert_called_once_with(hotel_id=book_hotel_dto.hotel_id, book_hotel_dto=book_hotel_dto)
        assert hotel_dto.hotel_id == book_hotel_dto.hotel_id
        assert hotel_dto.checkin_date == book_hotel_dto.checkin_date
        assert hotel_dto.checkout_date == book_hotel_dto.checkout_date
        assert hotel_dto.total_amount == book_hotel_dto.total_amount
        assert hotel_dto.user_id == book_hotel_dto.user_id
        assert hotel_dto.tariff == book_hotel_dto.tariff
        assert hotel_dto.destination_id == book_hotel_dto.destination_id


    def test_get_bookings_for_user(self, storage):
        pass
        # interactor = GetBookingsForUserInteractor(storage=storage)
        # get_bookings_for_user_dto = GetBookingsForUserDTOFactory()
        #
        # storage.get_bookings_for_user.return_value = [GetBookingsForUserDTO(
        #     user_id = get_bookings_for_user_dto.user_id,
        #     checkin_date = get_bookings_for_user_dto.checkin_date,
        #     checkout_date = get_bookings_for_user_dto.checkout_date,

    def test_get_destination(self,storage):
        interactor = GetDestinationsInteractor(storage=storage)
        get_destinations_dto = GetDestinationsDTOFactory()
        mock_destination_dtos = DestinationDTOFactory.create_batch(5)
        storage.get_destinations.return_value = [
            DestinationDTO(
                id = destination_dto.id,
                name = destination_dto.name,
                description = destination_dto.description,
                tags = destination_dto.tags,
                user_id = destination_dto.user_id
            )
            for destination_dto in mock_destination_dtos
        ]


        destination_dtos = interactor.get_destinations(get_destinations_dto=get_destinations_dto)

        storage.get_destinations.assert_called_once_with(get_destinations_dto=get_destinations_dto)
        for i in range(5):
            assert destination_dtos[i].id == mock_destination_dtos[i].id
            assert destination_dtos[i].name == mock_destination_dtos[i].name
            assert destination_dtos[i].description == mock_destination_dtos[i].description
            assert destination_dtos[i].tags == mock_destination_dtos[i].tags
            assert destination_dtos[i].user_id == mock_destination_dtos[i].user_id




    def test_get_destinations(self, storage):
        interactor = GetDestinationsInteractor(storage=storage)
        get_destinations_dto = GetDestinationsDTOFactory()

        mock_destination_dtos = DestinationDTOFactory.create_batch(5)
        storage.get_destinations.return_value = [
            DestinationDTO(
                id = destination_dto.id,
                name = destination_dto.name,
                description = destination_dto.description,
                tags = destination_dto.tags,
                user_id = destination_dto.user_id
            )
            for destination_dto in mock_destination_dtos
        ]

        destination_dtos = interactor.get_destinations(get_destinations_dto=get_destinations_dto)

        storage.get_destinations.assert_called_once_with(get_destinations_dto=get_destinations_dto)
        for i in range(5):
            assert destination_dtos[i].id == mock_destination_dtos[i].id
            assert destination_dtos[i].name == mock_destination_dtos[i].name
            assert destination_dtos[i].description == mock_destination_dtos[i].description
            assert destination_dtos[i].tags == mock_destination_dtos[i].tags
            assert destination_dtos[i].user_id == mock_destination_dtos[i].user_id

