import graphene
from future.backports.datetime import datetime

from trip.exceptions.custom_exceptions import BookingScheduleOverlap, InvalidAdminUser, InvalidDestination, \
    InvalidCheckinCheckoutDate
from trip.interactors.book_hotel_interactor import BookHotelInteractor
from trip.interactors.storage_interfaces.storage_interface import MutateBookingDTO, AddBookingDTO
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.booking.types.types import BookingNotPossible, BookHotelResponse, BookHotelParams, Booking, \
    BookingDateNotValid
from trip.models import Hotel
from trip_gql.common_errors import DestinationNotFound


class BookHotel(graphene.Mutation):
    class Arguments:
        params = BookHotelParams(required=True)

    Output = BookHotelResponse

    @staticmethod
    def mutate(root, info, params):
        storage = StorageImplementation()
        interactor = BookHotelInteractor(storage=storage)
        checkin_date = params.checkin_date
        checkout_date = params.checkout_date
        tariff = Hotel.objects.get(id=params.hotel_id).tariff

        days = abs(checkin_date-checkout_date).days

        if days:
            total_amount =tariff * days
        else:
            total_amount = tariff

        # checkin_date_str = '-'.join(date for date in checkin_date),
        # checkout_date_str = '-'.join(date for date in checkout_date),

        booking_dto = AddBookingDTO(
            user_id=params.user_id,
            checkin_date=params.checkin_date,
            checkout_date = params.checkout_date,
            total_amount = total_amount,
            destination_id = params.destination_id,
            hotel_id= params.hotel_id,
            tariff = tariff
        )
        try:
            hotel_dto = interactor.book_hotel(hotel_id=params.hotel_id, book_hotel_dto=booking_dto)
        except BookingScheduleOverlap:
            return BookingNotPossible(hotel_id=params.hotel_id)
        except InvalidDestination:
            return DestinationNotFound(destination_id = params.destination_id)
        except InvalidCheckinCheckoutDate:
            return BookingDateNotValid(checkin_date= params.checkin_date, checkout_date=params.checkout_date)


        return Booking(
                id = hotel_dto.booking_id,
                user_id = hotel_dto.user_id,
                destination_id = hotel_dto.destination_id,
                hotel_id = hotel_dto.hotel_id,
                checkin_date = hotel_dto.checkin_date,
                checkout_date = hotel_dto.checkout_date,
                total_amount = hotel_dto.total_amount,
                tariff = tariff
            )

