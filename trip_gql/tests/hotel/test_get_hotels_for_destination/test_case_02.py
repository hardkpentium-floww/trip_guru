import pytest

from trip.tests.factories.models import UserFactory, DestinationFactory, HotelFactory
from trip_gql.tests.hotel.test_get_hotels_for_destination.base_test import GetHotelsForDestinationTest


@pytest.mark.django_db
class TestCase(GetHotelsForDestinationTest):

    USER_ID = "test_user"

    def test_get_hotels_for_destination_with_invalid_destination_id(self, snapshot):
        # Arrange

        destination = DestinationFactory()
        hotel = HotelFactory.create_batch(5, destination_id=destination.id)

        variables ={
          "params": {
            "destinationId": 1
          }
        }

        # Act
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )