import pytest

from trip.tests.factories.models import DestinationFactory, HotelFactory
from trip_gql.tests.destination.test_get_destinations.base_test import GetDestinationsTest



@pytest.mark.django_db
class TestCase(GetDestinationsTest):

    USER_ID = "valid_test_user"

    def test_get_destinations(self, snapshot):
        # Arrange
        user_id = "test_user_id"
        # UserProfileFactory.create(user_id=user_id)
        destinations = DestinationFactory.create_batch(5, tags="beach")
        DestinationFactory.create_batch(5, tags="hills")
        HotelFactory.create_batch(5, destination_id=destinations[0].id)

        variables = {
            "params": {
                "tag": "beach",
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