from graphql_service.utils.base_test import GraphQLBaseTestCase


class GetBookingsForUserTest(GraphQLBaseTestCase):
    QUERY = """
    query GetBookingsForUser($params: GetBookingsForUserParams!) {
      getBookingsForUser(params: $params) {
      __typename
        ... on Bookings {
          bookings {
            id
            userId
            destinationId
            hotelId
            checkinDate
            checkoutDate
            tariff
            totalAmount
          }
        }
        ... on BookingsNotFound {
          userId
        }
      }
    }
    """



