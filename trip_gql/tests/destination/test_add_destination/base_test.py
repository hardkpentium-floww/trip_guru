from graphql_service.utils.base_test import GraphQLBaseTestCase


class AddDestinationTest(GraphQLBaseTestCase):
    QUERY = """
        mutation Mutation($params: AddDestinationParams!) {
        
          addDestination(params: $params) {
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
            ... on UserNotAdmin {
              userId
            }
          }
        }
    """



