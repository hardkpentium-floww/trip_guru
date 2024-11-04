import pytest

from trip.tests.factories.models import UserFactory, DestinationFactory
from trip_gql.tests.destination.test_update_destination.base_test import UpdateDestinationTest


@pytest.mark.django_db
class TestCase(UpdateDestinationTest):

    USER_ID = "test_user"

    def test_add_destination_with_invalid_destination_id(self, snapshot):
        # Arrange

        user = UserFactory(id="test_user")
        destination = DestinationFactory.create_batch(3,user_id = user.id, name="hotel1")

        variables ={
          "params": {
            "destinationId": destination[0].id,
            "name": destination[1].name,
            "description": "123123",
            "tags": "beachh"
          }
        }

        # Act
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )