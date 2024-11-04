


from graphql.type.definition import (
    GraphQLArgument,
    GraphQLList,
    GraphQLNonNull,
)
from graphql.type.directives import DirectiveLocation, GraphQLDirective
from graphql.type.scalars import GraphQLString

AwsSubscribe = GraphQLDirective(
    name="aws_subscribe",
    description="Appsync Subscriptions",
    locations=[DirectiveLocation.FIELD_DEFINITION],
    args={
        "mutations": GraphQLArgument(
            type_=GraphQLNonNull(GraphQLList(GraphQLNonNull(GraphQLString)))
        )
    },
)
