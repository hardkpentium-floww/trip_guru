from graphql_service.utils.base_test import GraphQLBaseTestCase


class GetDestinationTest(GraphQLBaseTestCase):
    QUERY = """
       query GetDestination($params: GetDestinationParams!) {
          getDestination(params: $params) {
          __typename
            ... on Destination {
              id
              name
              description
              userId
              tags
              hotels {
                id
                name
                description
                imageUrls
                destinationId
                tariff
              }
            }
            ... on DestinationNotFound {
              destinationId
            }
          }
        }
    """



