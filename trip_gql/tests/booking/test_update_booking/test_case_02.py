import pytest
from future.backports.datetime import datetime, timedelta

from trip.tests.factories.models import UserFactory, DestinationFactory, HotelFactory, BookingFactory
from trip_gql.tests.booking.test_update_booking.base_test import UpdateBookingTest


@pytest.mark.django_db
class TestCase(UpdateBookingTest):

    USER_ID = "test_user"

    def test_update_booking_with_overlapping_dates(self, snapshot):
        # Arrange

        user = UserFactory(id="test_user")
        booking = BookingFactory(user_id=user.id, checkin_date=datetime.now(), checkout_date=datetime.now() + timedelta(3))
        variables ={
              "params": {
                "bookingId": booking.id,
                "checkinDate": datetime.now(),
                "checkoutDate": datetime.now() + timedelta(9),
                "totalAmount": 3000
              }
            }

        # Act
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )