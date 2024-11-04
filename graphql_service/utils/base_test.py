"""
Created on: 04/02/23
"""
from typing import Dict

from snapshottest.pytest import PyTestSnapshotTest


class Context:
    def __init__(self, user_id: str):
        self.user_id = user_id


class GraphQLBaseTestCase:
    USER_ID = "valid_test_user"

    def execute_schema(
        self,
        query: str,
        variables: Dict,
        snapshot: PyTestSnapshotTest,
    ):
        from trip_gql.schema import execute_schema

        result = execute_schema(
            query,
            user_id=self.USER_ID,
            variables=variables,
        )

        # Assert
        if result.errors:
            error = getattr(result.errors[0], "original_error")
            if error:
                raise error
            else:
                content = result.errors
        else:
            content = result.data
        snapshot.assert_match(name="Result", value=content)
        return result
