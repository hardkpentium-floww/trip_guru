from graphql_service.utils.base_test import GraphQLBaseTestCase


class GetDestinationsTest(GraphQLBaseTestCase):
    QUERY = """
        query Query($params: GetDestinationsParams!) {
          getDestinations(params: $params) {
            __typename
            ... on Destinations {
              destinations {
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
            }
            ... on DestinationNotFound {
              destinationId
            }
          }
        }
    """



