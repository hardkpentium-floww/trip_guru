import datetime
from typing import Optional

import graphene
from graphene.types import Scalar
from graphql import GraphQLError
from graphql.language import ast

from graphql_service.constants import DATE_FORMAT, DATE_TIME_FORMAT, TIME_FORMAT


class GQLDateTimeScalar(Scalar):
    date_time_string_format = DATE_TIME_FORMAT

    @staticmethod
    def serialize(dt):
        return GQLDateTimeScalar.convert_datetime_object_to_string(
            datetime_obj=dt
        )

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return datetime.datetime.strptime(
                node.value, GQLDateTimeScalar.date_time_string_format
            )

    @staticmethod
    def parse_value(value):
        return datetime.datetime.strptime(
            value, GQLDateTimeScalar.date_time_string_format
        )

    @staticmethod
    def convert_datetime_object_to_string(
        datetime_obj: datetime,
    ) -> Optional[str]:
        if not datetime_obj:
            return None
        datetime_in_string_format = datetime_obj.strftime(DATE_TIME_FORMAT)
        return datetime_in_string_format


class GQLDateScalar(Scalar):
    date_string_format = DATE_FORMAT

    @staticmethod
    def serialize(dt):
        return GQLDateScalar.convert_date_object_to_string(datetime_obj=dt)

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return datetime.datetime.strptime(
                node.value, GQLDateScalar.date_string_format
            ).date()

    @staticmethod
    def parse_value(value):
        return datetime.datetime.strptime(
            value, GQLDateScalar.date_string_format
        ).date()

    @staticmethod
    def convert_date_object_to_string(
        datetime_obj: datetime,
    ) -> Optional[str]:
        if not datetime_obj:
            return None
        date_in_string_format = datetime_obj.strftime(DATE_FORMAT)
        return date_in_string_format


class GQLTimeScalar(Scalar):
    time_string_format = TIME_FORMAT

    @staticmethod
    def serialize(dt):
        return GQLTimeScalar.convert_time_object_to_string(datetime_obj=dt)

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return datetime.datetime.strptime(
                node.value, GQLTimeScalar.time_string_format
            ).time()

    @staticmethod
    def parse_value(value):
        return datetime.datetime.strptime(
            value, GQLTimeScalar.time_string_format
        ).time()

    @staticmethod
    def convert_time_object_to_string(
        datetime_obj: datetime,
    ) -> Optional[str]:
        if not datetime_obj:
            return None
        time_in_string_format = datetime_obj.strftime(TIME_FORMAT)
        return time_in_string_format


class GQLRequiredList(graphene.List):
    def __init__(self, of_type, *args, **kwargs):
        super().__init__(of_type, *args, **kwargs, required=True)
        self._of_type = graphene.NonNull(of_type)


class GQLRequiredStringScalar(Scalar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, required=True)

    @staticmethod
    def serialize(value):
        value = GQLRequiredStringScalar._parse_value_with_validation(
            value=value
        )
        return value

    @staticmethod
    def parse_value(value):
        value = GQLRequiredStringScalar._parse_value_with_validation(
            value=value
        )
        return value

    @staticmethod
    def parse_literal(node):
        # Custom literal parsing logic
        return node.value

    @staticmethod
    def _parse_value_with_validation(value):
        value = value.strip()
        if value:
            return value

        error_message = "Expected non-nullable type, not to be empty strings"
        raise GraphQLError(error_message)


CUSTOM_SCALARS_TO_REPLACE_WITH_STRING_IN_APPSYNC = [
    GQLDateTimeScalar,
    GQLDateScalar,
    GQLTimeScalar,
    GQLRequiredStringScalar,
]


CUSTOM_LIST_SCALARS = [GQLRequiredList]
