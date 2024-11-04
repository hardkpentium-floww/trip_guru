from graphql_service.utils.base_test import GraphQLBaseTestCase


class UpdateBookingTest(GraphQLBaseTestCase):
    QUERY = """
    mutation Mutation($params: UpdateBookingParams!) {
      updateBooking(params: $params) {
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
      }
    }
    """



