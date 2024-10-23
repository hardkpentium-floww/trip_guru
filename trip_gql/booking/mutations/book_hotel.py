import graphene

from trip.exceptions.custom_exceptions import BookingScheduleOverlap
from trip.interactors.book_hotel_interactor import BookHotelInteractor
from trip.interactors.storage_interfaces.storage_interface import HotelDTO, BookingDTO
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.booking.types.types import BookingNotPossible, BookHotelResponse, BookHotelParams
from trip_gql.hotel.types.types import Hotel


class BookHotel(graphene.Mutation):
    class Arguments:
        params = BookHotelParams(required=True)

    Output = BookHotelResponse

    @staticmethod
    def mutate(root, info, params):
        storage = StorageImplementation()
        interactor = BookHotelInteractor(storage=storage)

        booking_dto = BookingDTO(
            user_id=params.user_id,
            hotel_id=params.hotel_id,
            checkin_date=params.checkin_date,
            checkout_date=params.checkout_date
        )
        try:
            hotel_dto = interactor.book_hotel(book_hotel_dto=booking_dto)
        except BookingScheduleOverlap:
            return BookingNotPossible(hotel_id=params.user_id)


        return BookHotelResponse(
            Hotel(
                id=str(hotel_dto.id),
                name=hotel_dto.name,
                description=hotel_dto.description,
                tariff=hotel_dto.tariff,
                image_urls=hotel_dto.image_urls,
                destination_id=hotel_dto.destination_id
            )
        )
        )