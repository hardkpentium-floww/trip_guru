import pytest

from trip.tests.factories.models import UserFactory, DestinationFactory, HotelFactory
from trip_gql.tests.hotel.test_update_hotel.base_test import UpdateHotelTest


@pytest.mark.django_db
class TestCase(UpdateHotelTest):

    USER_ID = "test_user"

    def test_update_hotel(self, snapshot):
        # Arrange

        destination = DestinationFactory()
        hotel = HotelFactory.create_batch(5,destination_id=destination.id, name="hotel3")

        variables ={
              "params": {
                "hotelId": hotel[0].id,
                "name": "hotel3",
                "description": "this is a hotel",
                "imageUrls": "image_urls",
                "destinationId": destination.id,
                "tariff": 3000
              }
            }

        # Act
        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )