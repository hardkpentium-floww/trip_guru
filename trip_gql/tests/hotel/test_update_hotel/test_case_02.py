import pytest

from trip.tests.factories.models import UserFactory, DestinationFactory, HotelFactory
from trip_gql.tests.hotel.test_update_hotel.base_test import UpdateHotelTest


@pytest.mark.django_db
class TestCase(UpdateHotelTest):

    USER_ID = "invalid_test_user"

    def test_update_hotel(self, snapshot):
        # Arrange

        destination = DestinationFactory()
        hotel = HotelFactory(destination_id=destination.id)

        variables ={
              "params": {
                "hotelId": hotel.id,
                "name": "hotel4",
                "description": "this is a hotel",
                "imageUrls": "image_urls",
                "destinationId": destination.id,
                "tariff": 5000
              }
            }

        # Act
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )