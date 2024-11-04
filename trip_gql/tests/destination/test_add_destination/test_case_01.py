import pytest

from trip.tests.factories.models import UserFactory
from trip_gql.tests.destination.test_add_destination.base_test import AddDestinationTest


@pytest.mark.django_db
class TestCase(AddDestinationTest):

    USER_ID = "test_user"

    def test_add_destination(self, snapshot):
        # Arrange

        user = UserFactory(id="test_user")

        variables ={
          "params": {
            "name": "Dedlhzxci",
            "description": "pollution free city",
            "tags": "smog",
            "hotels": [
              {
                "name": "testdz_hotel_name",
                "description": "test_hotel_name",
                "tariff": 2000,
                "imageUrls": "test_hotel_images"
              }
            ]
          }
        }

        # Act
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )