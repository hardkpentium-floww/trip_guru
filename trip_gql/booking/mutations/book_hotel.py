import graphene

from trip.exceptions.custom_exceptions import BookingScheduleOverlap
from trip.interactors.book_hotel_interactor import BookHotelInteractor
from trip.interactors.storage_interfaces.storage_interface import MutateBookingDTO
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.booking.types.types import BookingNotPossible, BookHotelResponse, BookHotelParams, Booking
from trip_gql.hotel.types.types import Hotel


class BookHotel(graphene.Mutation):
    class Arguments:
        params = BookHotelParams(required=True)

    Output = BookHotelResponse

    @staticmethod
    def mutate(root, info, params):
        storage = StorageImplementation()
        interactor = BookHotelInteractor(storage=storage)
        days = params.checkout_date - params.checkin_date
        if days:
            total_amount = params.tariff * days.days
        else:
            total_amount = params.tariff

        booking_dto = MutateBookingDTO(
            user_id=params.user_id,
            checkin_date=params.checkin_date,
            checkout_date=params.checkout_date,
            total_amount = total_amount,
            destination_id = params.destination_id
        )
        try:
            hotel_dto = interactor.book_hotel(hotel_id=params.hotel_id, book_hotel_dto=booking_dto)
        except BookingScheduleOverlap:
            return BookingNotPossible(hotel_id=params.user_id)


        return BookHotelResponse(
            Booking(
                booking_id = hotel_dto.id,
                user_id = hotel_dto.user_id,
                destination_id = hotel_dto.destination_id,
                hotel_id = hotel_dto.hotel_id,
                checkin_date = hotel_dto.checkin_date,
                checkout_date = hotel_dto.checkout_date,
                total_amount = hotel_dto.total_amount
            )
        )
