import pytest
from future.backports.datetime import datetime, timedelta

from trip.tests.factories.models import UserFactory, DestinationFactory, HotelFactory
from trip_gql.tests.booking.test_book_hotel.base_test import BookHotelTest


@pytest.mark.django_db
class TestCase(BookHotelTest):

    USER_ID = "test_user"

    def test_book_hotel_with_invalid_booking_dates(self, snapshot):
        # Arrange

        user = UserFactory(id="test_user")
        destination = DestinationFactory(user_id = user.id)
        hotel = HotelFactory(destination_id = destination.id)

        variables ={
              "params": {
                "userId": user.id,
                "checkinDate": datetime.now()+ timedelta(3),
                "checkoutDate": datetime.now(),
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