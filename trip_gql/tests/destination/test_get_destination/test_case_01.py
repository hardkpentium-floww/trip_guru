import pytest

from trip.tests.factories.models import DestinationFactory, HotelFactory
from trip_gql.tests.destination.test_get_destination.base_test import GetDestinationTest



@pytest.mark.django_db
class TestCase(GetDestinationTest):

    USER_ID = "valid_test_user"

    def test_get_destination(self, snapshot):
        # Arrange
        destination = DestinationFactory()

        variables = {
            "params": {
                "destinationId": destination.id
                }
        }

        # Act
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )