from graphql_service.utils.base_test import GraphQLBaseTestCase


class GetHotelTest(GraphQLBaseTestCase):
    QUERY = """
        query Query($params: GetHotelParams!) {
          getHotel(params: $params) {
          __typename
            ... on Hotel {
              id
              name
              description
              imageUrls
              destinationId
              tariff
            }
            ... on HotelNotFound {
              id
            }
          }
        }
    """



