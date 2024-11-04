from graphql_service.utils.base_test import GraphQLBaseTestCase


class GetHotelsForDestinationTest(GraphQLBaseTestCase):
    QUERY = """
       query Query($params: GetHotelsParams!) {
          getHotelsForDestination(params: $params) {
          __typename
            ... on Hotels {
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



