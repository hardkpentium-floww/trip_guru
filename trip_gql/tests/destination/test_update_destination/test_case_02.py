import pytest

from trip.tests.factories.models import UserFactory, DestinationFactory
from trip_gql.tests.destination.test_update_destination.base_test import UpdateDestinationTest


@pytest.mark.django_db
class TestCase(UpdateDestinationTest):

    USER_ID = "invalid_test_user"

    def test_add_destination(self, snapshot):
        # Arrange

        user = UserFactory(id="test_user")
        destination = DestinationFactory(user_id = user.id)

        variables ={
          "params": {
            "destinationId": destination.id,
            "name": "hotel1",
            "description": "123123",
            "userId": user.id,
            "tags": "beachh"
          }
        }

        # Act
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )