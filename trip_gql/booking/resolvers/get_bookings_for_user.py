from trip.exceptions.custom_exceptions import InvalidUser, NoBookingsExists
from trip.interactors.get_bookings_for_user import GetBookingsForUserInteractor
from trip.interactors.get_destination_interactor import GetDestinationInteractor
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.booking.types.types import UserNotFound, Bookings, Booking
from trip_gql.common_errors import BookingsNotFound


def resolve_get_bookings_for_user(root, info, params):
    storage = StorageImplementation()
    interactor = GetBookingsForUserInteractor(storage=storage)

    try:
        booking_dtos = interactor.get_bookings_for_user(user_id=params.user_id, offset=params.offset, limit=params.limit)
    except NoBookingsExists:
        return BookingsNotFound(user_id=params.user_id)

    return Bookings(
            bookings=[Booking(
                id=booking_dto.booking_id,
                user_id=booking_dto.user_id,
                hotel_id=booking_dto.hotel_id,
                checkin_date=booking_dto.checkin_date,
                checkout_date=booking_dto.checkout_date,
                total_amount=booking_dto.total_amount,
                destination_id=booking_dto.destination_id

            ) for booking_dto in booking_dtos]
        )
