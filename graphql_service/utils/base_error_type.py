"""
Created on: 04/02/23
"""
import graphene


class GraphQLBaseError(graphene.Interface):
    """
    Base class for all GraphQL errors
    """

    message = graphene.String()
