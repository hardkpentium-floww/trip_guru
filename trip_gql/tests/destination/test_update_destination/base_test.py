from graphql_service.utils.base_test import GraphQLBaseTestCase


class UpdateDestinationTest(GraphQLBaseTestCase):
    QUERY = """
      mutation UpdateDestination($params: UpdateDestinationParams!) {
          updateDestination(params: $params) {
          __typename
            ... on Destination {
              id
              name
              description
              userId
              tags
            }
            ... on UserNotAdmin {
              userId
            }
            ... on DestinationNotFound {
              destinationId
            }
          }
        }
    """



