import pytest

from trip.tests.factories.models import UserFactory, DestinationFactory
from trip_gql.tests.rating.test_add_rating.base_test import AddRatingTest


@pytest.mark.django_db
class TestCase(AddRatingTest):

    USER_ID = "invalid_test_user"

    def test_add_rating(self, snapshot):
        # Arrange

        user = UserFactory(id="test_user")
        destination = DestinationFactory(user_id = user.id)

        variables ={
              "params": {
                "destinationId": destination.id,
                "rating": 3.2,
                "review": "great place"
              }
            }

        # Act
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )