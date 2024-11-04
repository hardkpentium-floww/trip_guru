from graphql_service.utils.base_test import GraphQLBaseTestCase


class BookHotelTest(GraphQLBaseTestCase):
    QUERY = """
    mutation Mutation($params: BookHotelParams!) {
      bookHotel(params: $params) {
      __typename
        ... on Booking {
          id
          userId
          destinationId
          hotelId
          checkinDate
          checkoutDate
          tariff
          totalAmount
        }
        ... on BookingNotPossible {
          hotelId
        }
        ... on BookingDateNotValid {
          checkinDate
          checkoutDate
        }
        ... on DestinationNotFound {
          destinationId
        }
      }
    }
    """



