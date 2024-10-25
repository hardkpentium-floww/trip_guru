import graphene

from trip.exceptions.custom_exceptions import BookingScheduleOverlap
from trip.interactors.book_hotel_interactor import BookHotelInteractor
from trip.interactors.storage_interfaces.storage_interface import MutateBookingDTO
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.booking.types.types import BookingNotPossible, BookHotelResponse, BookHotelParams, Booking
from trip.models import Hotel


class BookHotel(graphene.Mutation):
    class Arguments:
        params = BookHotelParams(required=True)

    Output = BookHotelResponse

    @staticmethod
    def mutate(root, info, params):
        storage = StorageImplementation()
        interactor = BookHotelInteractor(storage=storage)
        checkin_date = params.checkin_date.split(" ")[0].split("-")
        checkout_date = params.checkout_date.split(" ")[0].split("-")
        tariff = Hotel.objects.get(id=params.hotel_id).tariff

        days = int(checkout_date[2]) - int(checkin_date[2])

        if days:
            total_amount =tariff * days
        else:
            total_amount = tariff

        booking_dto = MutateBookingDTO(
            user_id=params.user_id,
            checkin_date='-'.join(date for date in checkin_date),
            checkout_date='-'.join(date for date in checkout_date),
            total_amount = total_amount,
            destination_id = params.destination_id
        )
        try:
            hotel_dto = interactor.book_hotel(hotel_id=params.hotel_id, book_hotel_dto=booking_dto)
        except BookingScheduleOverlap:
            return BookingNotPossible(hotel_id=params.hotel_id)


        return Booking(
                id = hotel_dto.booking_id,
                user_id = hotel_dto.user_id,
                destination_id = hotel_dto.destination_id,
                hotel_id = hotel_dto.hotel_id,
                checkin_date = hotel_dto.checkin_date,
                checkout_date = hotel_dto.checkout_date,
                total_amount = hotel_dto.total_amount
            )

