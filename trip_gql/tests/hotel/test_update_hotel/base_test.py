from graphql_service.utils.base_test import GraphQLBaseTestCase


class UpdateHotelTest(GraphQLBaseTestCase):
    QUERY = """
        mutation Mutation($params: UpdateHotelParams!) {
          updateHotel(params: $params) {
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
            ... on HotelWithNameAlreadyExists {
              hotelName
            }
          }
        }
    """



