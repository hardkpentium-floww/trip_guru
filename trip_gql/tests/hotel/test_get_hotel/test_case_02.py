import pytest

from trip.tests.factories.models import UserFactory, DestinationFactory, HotelFactory
from trip_gql.tests.hotel.test_get_hotel.base_test import GetHotelTest


@pytest.mark.django_db
class TestCase(GetHotelTest):

    USER_ID = "test_user"

    def test_get_hotel(self, snapshot):
        # Arrange

        hotel = HotelFactory()

        variables ={
              "params": {
                "hotelId": 1
              }
            }

        # Act
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )