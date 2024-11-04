import pytest

from trip.tests.factories.models import UserFactory, DestinationFactory
from trip_gql.tests.hotel.test_add_hotel.base_test import AddHotelTest


@pytest.mark.django_db
class TestCase(AddHotelTest):

    USER_ID = "test_user"

    def test_add_hotel_with_invalid_destination_id(self, snapshot):
        # Arrange

        user = UserFactory(id="test_user")
        destination = DestinationFactory(user_id = user.id)

        variables ={
              "params": {
                "name": "hotel1",
                "description": "del",
                "tariff": 1000,
                "imageUrls": "urls",
                "destinationId": 1
              }
            }

        # Act
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )