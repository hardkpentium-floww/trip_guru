from graphql_service.utils.base_test import GraphQLBaseTestCase


class AddRatingTest(GraphQLBaseTestCase):
    QUERY = """
        mutation Mutation($params: AddRatingParams!) {
          addRating(params: $params) {
          __typename
            ... on Rating {
              ratingId
              userId
              destinationId
              rating
              review
            }
            ... on DestinationNotFound {
              destinationId
            }
            ... on UserNotAuthorized {
              userId
            }
            ... on RatingNotValid {
              rating
            }
          }
        }
    """



