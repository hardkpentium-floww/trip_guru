from graphql_service.utils.base_test import GraphQLBaseTestCase


class AddHotelTest(GraphQLBaseTestCase):
    QUERY = """
    mutation Mutation($params: AddHotelParams!) {
          addHotel(params: $params) {
          __typename
            ... on Hotel {
              id
              name
              description
              imageUrls
              destinationId
              tariff
            }
            ... on UserNotAuthorized {
              userId
            }
            ... on TariffNotValid {
              tariff
            }
            ... on DestinationNotFound {
              destinationId
            }
          }
        }
    """



