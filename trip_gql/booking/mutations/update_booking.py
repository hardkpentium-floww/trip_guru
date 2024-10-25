import graphene

from trip.exceptions.custom_exceptions import BookingScheduleOverlap
from trip.interactors.storage_interfaces.storage_interface import MutateBookingDTO
from trip.interactors.update_booking import UpdateBookingInteractor
from trip.models import Booking as BookingModel
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.booking.types.types import BookingNotPossible, UpdateBookingParams, UpdateBookingResponse, Booking


class UpdateBooking(graphene.Mutation):
    class Arguments:
        params = UpdateBookingParams(required=True)

    Output = UpdateBookingResponse

    @staticmethod
    def mutate(root, info, params):
        storage = StorageImplementation()
        interactor = UpdateBookingInteractor(storage=storage)
        checkin_date = params.checkin_date.split(" ")[0].split("-")
        checkout_date = params.checkout_date.split(" ")[0].split("-")
        tariff = BookingModel.objects.get(id=params.booking_id).hotel.tariff

        days = int(checkout_date[2]) - int(checkin_date[2])

        if days:
            total_amount = tariff * days
        else:
            total_amount = tariff

        update_booking_dto = MutateBookingDTO(
            checkin_date='-'.join(date for date in checkin_date),
            checkout_date='-'.join(date for date in checkout_date),
            total_amount=total_amount,
            booking_id=params.booking_id

        )
        try:
            booking_dto = interactor.update_booking(update_booking_dto=update_booking_dto)
        except BookingScheduleOverlap:
            return BookingNotPossible(booking_id=params.booking_id)


        return Booking(
                id=booking_dto.booking_id,
                user_id=booking_dto.user_id,
                destination_id=booking_dto.destination_id,
                hotel_id=booking_dto.hotel_id,
                checkin_date=booking_dto.checkin_date,
                checkout_date=booking_dto.checkout_date,
                total_amount=booking_dto.total_amount
            )

