import pytest
from future.backports.datetime import datetime, timedelta

from trip.tests.factories.models import UserFactory, DestinationFactory, HotelFactory, BookingFactory
from trip_gql.tests.booking.test_book_hotel.base_test import BookHotelTest


@pytest.mark.django_db
class TestCase(BookHotelTest):

    USER_ID = "test_user"

    def test_book_hotel_with_overlapping_dates(self, snapshot):
        # Arrange

        user = UserFactory(id="test_user")
        destination = DestinationFactory(user_id = user.id)
        hotel = HotelFactory(destination_id = destination.id)
        booking = BookingFactory(checkin_date=datetime.now(), checkout_date=datetime.now()+ timedelta(3), user_id=user.id, destination_id=destination.id, hotel_id=hotel.id)

        variables ={
              "params": {
                "userId": user.id,
                "checkinDate": datetime.now() + timedelta(1),
                "checkoutDate": datetime.now()+ timedelta(9),
                "hotelId": hotel.id,
                "destinationId": destination.id
              }
            }

        # Act
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )