import graphene

from trip.exceptions.custom_exceptions import BookingScheduleOverlap
from trip.interactors.storage_interfaces.storage_interface import MutateBookingDTO
from trip.interactors.update_booking import UpdateBookingInteractor
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.booking.types.types import BookingNotPossible, Booking, UpdateBookingParams, UpdateBookingResponse


class UpdateBooking(graphene.Mutation):
    class Arguments:
        params = UpdateBookingParams(required=True)

    Output = UpdateBookingResponse

    @staticmethod
    def mutate(root, info, params):
        storage = StorageImplementation()
        interactor = UpdateBookingInteractor(storage=storage)
        days = params.checkout_date - params.checkin_date
        if days:
            total_amount = params.tariff * days.days
        else:
            total_amount = params.tariff

        update_booking_dto = MutateBookingDTO(
            checkin_date=params.checkin_date,
            checkout_date=params.checkout_date,
            total_amount=total_amount,
            booking_id=params.booking_id

        )
        try:
            booking_dto = interactor.update_booking(update_booking_dto=update_booking_dto)
        except BookingScheduleOverlap:
            return BookingNotPossible(hotel_id=params.user_id)


        return UpdateBookingResponse(
            Booking(
                booking_id=booking_dto.id,
                user_id=booking_dto.user_id,
                destination_id=booking_dto.destination_id,
                hotel_id=booking_dto.hotel_id,
                checkin_date=booking_dto.checkin_date,
                checkout_date=booking_dto.checkout_date,
                total_amount=booking_dto.total_amount
            )
        )
