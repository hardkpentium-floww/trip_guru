from unittest.mock import create_autospec, patch
import pytest

from trip.exceptions.custom_exceptions import InvalidAdminUser, InvalidUser
from trip.interactors.add_destination_interactor import AddDestinationInteractor
from trip.interactors.add_hotel_interactor import AddHotelInteractor
from trip.interactors.add_hotels_interactor import AddHotelsInteractor
from trip.interactors.add_rating_interactor import AddRatingInteractor
from trip.interactors.book_hotel_interactor import BookHotelInteractor
from trip.interactors.get_destinations_interactor import GetDestinationsInteractor
from trip.interactors.get_hotel_interactor import GetHotelInteractor
from trip.interactors.get_hotels_interactor import GetHotelsInteractor
from trip.interactors.storage_interfaces.storage_interface import StorageInterface, HotelDTO, \
    DestinationDTO, BookingDTO, AddRatingDTO
from trip.interactors.update_booking import UpdateBookingInteractor
from trip.interactors.update_destination_interactor import UpdateDestinationInteractor
from trip.interactors.update_hotel_interactor import UpdateHotelInteractor
from trip.tests.factories.storage_dtos import AddDestinationDTOFactory, DestinationDTOFactory, HotelDTOFactory, \
    AddRatingDTOFactory, BookHotelDTOFactory, GetDestinationsDTOFactory, BookingDTOFactory, \
    UpdateDestinationDTOFactory, UpdateHotelDTOFactory


class TestInteractor:
    @pytest.fixture
    def storage(self):
        storage = create_autospec(StorageInterface)
        return storage

    @patch.object(AddHotelsInteractor, 'add_hotels')
    def test_add_destination(self, mock_add_hotels,storage):
        #Arrange
        interactor = AddDestinationInteractor(storage=storage)
        add_destination_dto = AddDestinationDTOFactory()
        add_hotel_dtos = HotelDTOFactory.create_batch(3, destination_id=add_destination_dto.id)

        storage.add_destination.return_value = DestinationDTOFactory(
            description=add_destination_dto.description,
            name=add_destination_dto.name,
            tags=add_destination_dto.tags,
            user_id=add_destination_dto.user_id
        )

        mock_add_hotels.return_value = add_hotel_dtos

        # Act
        destination_dto = interactor.add_destination(add_destination_dto=add_destination_dto,add_hotel_dtos=add_hotel_dtos)

        #assert
        storage.add_destination.assert_called_once_with(add_destination_dto=add_destination_dto)
        mock_add_hotels.assert_called_once_with(user_id=add_destination_dto.user_id, add_hotel_dtos=add_hotel_dtos, destination_id = destination_dto.id)

        assert destination_dto.description == add_destination_dto.description
        assert destination_dto.name == add_destination_dto.name
        assert destination_dto.tags == add_destination_dto.tags
        assert destination_dto.user_id == add_destination_dto.user_id

    def test_add_hotel_with_invalid_admin(self, storage):
        # Arrange
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
        # Act
        storage.validate_admin_user.side_effect = InvalidAdminUser
        with pytest.raises(InvalidAdminUser):
            hotel_dto = interactor.add_hotel(user_id="e9ab78e1-93c2-41bc-966d-615a9cfd175d", add_hotel_dto=add_hotel_dto)
        # assert
        storage.validate_admin_user.assert_called_once_with(user_id="e9ab78e1-93c2-41bc-966d-615a9cfd175d")


    def test_add_hotel_with_valid_admin(self, storage):
        # Arrange
        interactor = AddHotelInteractor(storage=storage)
        add_hotel_dto = HotelDTOFactory()

        storage.add_hotel.return_value = HotelDTO(
            id=add_hotel_dto.id,
            description=add_hotel_dto.description,
            name=add_hotel_dto.name,
            tariff=add_hotel_dto.tariff,
            image_urls=add_hotel_dto.image_urls,
            destination_id=add_hotel_dto.destination_id
        )
        # Act

        hotel_dto = interactor.add_hotel(user_id="e9ab68e1-95c2-41bc-966d-615a9cfd175d", add_hotel_dto=add_hotel_dto)

        # assert
        storage.add_hotel.assert_called_once_with(user_id="e9ab68e1-95c2-41bc-966d-615a9cfd175d",
                                                  add_hotel_dto=add_hotel_dto)
        assert hotel_dto.description == add_hotel_dto.description
        assert hotel_dto.name == add_hotel_dto.name
        assert hotel_dto.id == add_hotel_dto.id
        assert hotel_dto.tariff == add_hotel_dto.tariff
        assert hotel_dto.image_urls == add_hotel_dto.image_urls
        assert hotel_dto.destination_id == add_hotel_dto.destination_id

    def test_add_rating_invalid_user(self, storage):
        # Arrange
        interactor = AddRatingInteractor(storage=storage)

        add_rating_dto = AddRatingDTOFactory(user_id ="invalid_user")
        storage.validate_hotel_customer.side_effect = InvalidUser

        storage.add_rating.return_value = AddRatingDTO(
                 user_id ="invalid_user",
                 review =add_rating_dto.review,
                 destination_id =add_rating_dto.destination_id,
                 rating = add_rating_dto.rating
                )
        # Act
        with pytest.raises(InvalidUser):
            rating_dto = interactor.add_rating(add_rating_dto=add_rating_dto)

        # assert
        storage.validate_hotel_customer.assert_called_once_with(destination_id=add_rating_dto.destination_id,user_id=add_rating_dto.user_id)

    def test_add_hotels(self, storage):
        # Arrange
        interactor = AddHotelsInteractor(storage=storage)
        user_id = "valid_user_id"
        destination_id = "valid_Destination_id"
        add_hotel_dtos = HotelDTOFactory.create_batch(5, destination_id=destination_id)
        storage.add_hotels.return_value = [HotelDTO(
            id= add_hotel_dto.id,
            description=add_hotel_dto.description,
            name=add_hotel_dto.name,
            tariff=add_hotel_dto.tariff,
            image_urls=add_hotel_dto.image_urls,
            destination_id = add_hotel_dto.destination_id
        ) for add_hotel_dto in add_hotel_dtos]

        # Act
        hotel_dtos = interactor.add_hotels(add_hotel_dtos=add_hotel_dtos, user_id=user_id, destination_id=destination_id)

        # assert
        storage.add_hotels.assert_called_once_with(add_hotel_dtos=add_hotel_dtos, user_id=user_id, destination_id=destination_id)
        assert add_hotel_dtos ==hotel_dtos



    def test_add_rating_valid_user(self, storage):
        # Arrange
        interactor = AddRatingInteractor(storage=storage)

        add_rating_dto = AddRatingDTOFactory()
        storage.validate_hotel_customer.side_effect = [True]

        storage.add_rating.return_value = AddRatingDTOFactory(
                 user_id =add_rating_dto.user_id,
                 review =add_rating_dto.review,
                 destination_id =add_rating_dto.destination_id,
                 rating = add_rating_dto.rating
                )

        # Act
        rating_dto = interactor.add_rating(add_rating_dto=add_rating_dto)

        # assert
        storage.add_rating.assert_called_once_with( add_rating_dto= add_rating_dto)
        assert rating_dto.user_id == add_rating_dto.user_id
        assert rating_dto.review == add_rating_dto.review
        assert rating_dto.destination_id == add_rating_dto.destination_id
        assert rating_dto.rating == add_rating_dto.rating




    def test_book_hotel(self, storage):
        # Arrange
        interactor = BookHotelInteractor(storage=storage)
        book_hotel_dto = BookHotelDTOFactory()

        storage.book_hotel.return_value = BookingDTO(
            hotel_id=book_hotel_dto.hotel_id,
            checkin_date=book_hotel_dto.checkin_date,
            checkout_date=book_hotel_dto.checkout_date,
            total_amount=book_hotel_dto.total_amount,
            user_id=book_hotel_dto.user_id,
            destination_id = book_hotel_dto.destination_id,
            booking_id = book_hotel_dto.booking_id
        )
        # Act
        hotel_dto = interactor.book_hotel(hotel_id=book_hotel_dto.hotel_id, book_hotel_dto=book_hotel_dto)
        # assert
        storage.book_hotel.assert_called_once_with(hotel_id=book_hotel_dto.hotel_id, book_hotel_dto=book_hotel_dto)
        assert hotel_dto.hotel_id == book_hotel_dto.hotel_id
        assert hotel_dto.checkin_date == book_hotel_dto.checkin_date
        assert hotel_dto.checkout_date == book_hotel_dto.checkout_date
        assert hotel_dto.total_amount == book_hotel_dto.total_amount
        assert hotel_dto.user_id == book_hotel_dto.user_id
        assert hotel_dto.destination_id == book_hotel_dto.destination_id


    def test_get_destination(self,storage):
        # Arrange
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

        # Act
        destination_dtos = interactor.get_destinations(get_destinations_dto=get_destinations_dto)
        # assert
        storage.get_destinations.assert_called_once_with(get_destinations_dto=get_destinations_dto)
        for i in range(5):
            assert destination_dtos[i].id == mock_destination_dtos[i].id
            assert destination_dtos[i].name == mock_destination_dtos[i].name
            assert destination_dtos[i].description == mock_destination_dtos[i].description
            assert destination_dtos[i].tags == mock_destination_dtos[i].tags
            assert destination_dtos[i].user_id == mock_destination_dtos[i].user_id




    def test_get_destinations(self, storage):
        # Arrange
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
        # Act
        destination_dtos = interactor.get_destinations(get_destinations_dto=get_destinations_dto)
        # assert
        storage.get_destinations.assert_called_once_with(get_destinations_dto=get_destinations_dto)
        for i in range(5):
            assert destination_dtos[i].id == mock_destination_dtos[i].id
            assert destination_dtos[i].name == mock_destination_dtos[i].name
            assert destination_dtos[i].description == mock_destination_dtos[i].description
            assert destination_dtos[i].tags == mock_destination_dtos[i].tags
            assert destination_dtos[i].user_id == mock_destination_dtos[i].user_id



    def test_get_hotel(self, storage):
        # Arrange
        interactor = GetHotelInteractor(storage=storage)
        get_hotel_dto = HotelDTOFactory()

        storage.get_hotel.return_value = HotelDTO(
            id = get_hotel_dto.id,
            name = get_hotel_dto.name,
            description= get_hotel_dto.description,
            tariff = get_hotel_dto.tariff,
            image_urls= get_hotel_dto.image_urls,
            destination_id= get_hotel_dto.destination_id
        )

        # Act
        hotel_dto = storage.get_hotel(hotel_id=get_hotel_dto.id)
        # assert
        storage.get_hotel.assert_called_once_with(hotel_id=get_hotel_dto.id)
        assert get_hotel_dto.id == hotel_dto.id
        assert get_hotel_dto.name == hotel_dto.name
        assert get_hotel_dto.description == hotel_dto.description
        assert get_hotel_dto.tariff == hotel_dto.tariff
        assert get_hotel_dto.image_urls == hotel_dto.image_urls
        assert get_hotel_dto.destination_id == hotel_dto.destination_id


    def test_get_hotels(self, storage):
        # Arrange
        interactor = GetHotelsInteractor(storage=storage)
        destination_id = 1

        mock_hotel_dtos = HotelDTOFactory.create_batch(5)
        storage.get_hotels.return_value = [HotelDTO(
            id=mock_hotel_dto.id,
            name=mock_hotel_dto.name,
            description=mock_hotel_dto.description,
            tariff=mock_hotel_dto.tariff,
            image_urls=mock_hotel_dto.image_urls,
            destination_id=mock_hotel_dto.destination_id
        ) for mock_hotel_dto in mock_hotel_dtos]

        # Act
        hotel_dtos = interactor.get_hotels(destination_ids=[destination_id])
        # assert
        storage.get_hotels.assert_called_once_with(destination_ids=[destination_id])
        for i in range(5):
            assert hotel_dtos[i] == mock_hotel_dtos[i]


    def test_update_booking(self, storage):
        # Arrange
        interactor = UpdateBookingInteractor(storage= storage)

        update_booking_dto = BookingDTOFactory()

        storage.update_booking.return_value = BookingDTO(
            booking_id=update_booking_dto.booking_id,
            checkin_date= update_booking_dto.checkin_date,
            checkout_date=update_booking_dto.checkout_date,
            total_amount=update_booking_dto.total_amount,
            user_id = update_booking_dto.user_id,
            destination_id=update_booking_dto.destination_id,
            hotel_id= update_booking_dto.hotel_id
        )
        # Act
        booking_dto = interactor.update_booking( update_booking_dto=update_booking_dto)
        # assert
        storage.update_booking.assert_called_once_with(
            booking_id= update_booking_dto.booking_id,
            update_booking_dto= update_booking_dto
        )

        assert booking_dto == update_booking_dto


    def test_update_destination(self, storage):
        # Arrange
        interactor = UpdateDestinationInteractor(storage=storage)
        destination_id = 1
        update_destination_dto = UpdateDestinationDTOFactory()

        storage.update_destination.return_value = DestinationDTO(
            id=update_destination_dto.id,
            name = update_destination_dto.name,
            description= update_destination_dto.description,
            tags = update_destination_dto.tags,
            user_id= update_destination_dto.user_id,

        )
        # Act
        destination_dto = interactor.update_destination(destination_id=destination_id, update_destination_dto= update_destination_dto)
        # assert
        storage.update_destination.assert_called_once_with(destination_id=destination_id, update_destination_dto= update_destination_dto)

        assert destination_dto.name == update_destination_dto.name
        assert destination_dto.description == update_destination_dto.description
        assert destination_dto.tags == update_destination_dto.tags
        assert destination_dto.user_id == update_destination_dto.user_id
        assert destination_dto.id == update_destination_dto.id


    def test_update_hotel_with_valid_admin(self, storage):
        # Arrange
        interactor = UpdateHotelInteractor(storage=storage)
        user_id = 'e9ab68e1-95c2-41bc-966d-615a9cfd175d'

        update_hotel_dto = UpdateHotelDTOFactory(hotel_id = 1)

        storage.update_hotel.return_value = HotelDTO(
            id = update_hotel_dto.hotel_id,
            name = update_hotel_dto.name,
            description= update_hotel_dto.description,
            tariff= update_hotel_dto.tariff,
            image_urls= update_hotel_dto.image_urls,
            destination_id= update_hotel_dto.destination_id
        )
        # Act
        hotel_dto = interactor.update_hotel(hotel_id=1,user_id=user_id, update_hotel_dto=update_hotel_dto)
        # assert
        storage.update_hotel.assert_called_once_with(hotel_id=1, update_hotel_dto=update_hotel_dto)

        assert  hotel_dto.id ==update_hotel_dto.hotel_id
        assert  hotel_dto.name == update_hotel_dto.name
        assert  hotel_dto.description== update_hotel_dto.description
        assert  hotel_dto.tariff== update_hotel_dto.tariff
        assert  hotel_dto.image_urls== update_hotel_dto.image_urls
        assert  hotel_dto.destination_id== update_hotel_dto.destination_id


    def test_update_hotel_with_invalid_admin(self, storage):
        # Arrange
        interactor = UpdateHotelInteractor(storage=storage)
        user_id = 'invalid_user_id'

        update_hotel_dto = UpdateHotelDTOFactory(hotel_id = 1)

        storage.update_hotel.return_value = HotelDTO(
            id = update_hotel_dto.hotel_id,
            name = update_hotel_dto.name,
            description= update_hotel_dto.description,
            tariff= update_hotel_dto.tariff,
            image_urls= update_hotel_dto.image_urls,
            destination_id= update_hotel_dto.destination_id
        )

        storage.validate_admin_user.side_effect = InvalidAdminUser
        # Act
        with pytest.raises(InvalidAdminUser):
            hotel_dto = interactor.update_hotel(hotel_id=1,user_id=user_id, update_hotel_dto=update_hotel_dto)

        # assert
        storage.validate_admin_user.assert_called_once_with(user_id=user_id)