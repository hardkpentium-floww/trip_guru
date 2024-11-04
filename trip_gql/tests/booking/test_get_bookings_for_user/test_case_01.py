import pytest
from future.backports.datetime import datetime, timedelta

from trip.tests.factories.models import UserFactory, DestinationFactory, HotelFactory, BookingFactory
from trip_gql.tests.booking.test_get_bookings_for_user.base_test import GetBookingsForUserTest


@pytest.mark.django_db
class TestCase(GetBookingsForUserTest):

    USER_ID = "test_user"

    def test_get_bookings_for_user(self, snapshot):
        # Arrange

        user = UserFactory(id="test_user")
        booking = BookingFactory.create_batch(13,user_id=user.id)

        variables ={
          "params": {
            "userId": self.USER_ID,
            "offset": 0,
            "limit": 10
          }
        }

        # Act
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )