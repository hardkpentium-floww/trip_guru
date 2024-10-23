from functools import wraps
from typing import Iterable, List, Optional

import graphene
from graphene import ResolveInfo

from graphql_service.enums import BasePermissionEnum


class CrmGraphQL:
    def __init__(self):
        self.appsync_subscribe_to = {}
        self.internal_fields = []


crm_graphql = CrmGraphQL()


appsync_mutation_to_subscribe = crm_graphql.appsync_subscribe_to
internal_fields = crm_graphql.internal_fields


class PermissionDenied(Exception):
    def __init__(self, perms: List[BasePermissionEnum]):
        super().__init__()
        self.perms = perms

    def __str__(self):
        perms_str = ", ".join([str(perm) for perm in self.perms])

        return f"{perms_str} only can access this field"


def message_one_of_permissions_required(
    permissions: Iterable[BasePermissionEnum],
) -> str:
    permission_msg = ", ".join([p for p in permissions])
    return f"\n\nRequires one of the following permissions: {permission_msg}."


def context(f):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            info = next(arg for arg in args if isinstance(arg, ResolveInfo))
            return func(info.context, *args, **kwargs)

        return wrapper

    return decorator


def one_of_permissions_required(
    perms: List[BasePermissionEnum], check_permission: callable
):
    def check_perms(context):
        if not check_permission(context.user_id, perms):
            raise PermissionDenied(perms=perms)

    return account_passes_test(check_perms)


def account_passes_test(test_func):
    """Determine if user/app has permission to access to content."""

    def decorator(f):
        @wraps(f)
        @context(f)
        def wrapper(context, *args, **kwargs):
            test_func(context)
            return f(*args, **kwargs)

        return wrapper

    return decorator


class CrmInternalField(graphene.Field):
    def __init__(self, *args, **kwargs):
        kwargs.update({"is_tf_internal_field": graphene.Boolean()})
        super().__init__(*args, **kwargs)


class CrmPublicQuery(graphene.Field):
    def __init__(self, *args, **kwargs):
        kwargs.update({"is_public_operation": graphene.Boolean()})
        super().__init__(*args, **kwargs)


class CrmPublicMutation(graphene.Field):
    def __init__(self, *args, **kwargs):
        kwargs.update({"is_public_operation": graphene.Boolean()})
        super().__init__(*args, **kwargs)


class CrmPermissionsField(graphene.Field):
    description: Optional[str]

    def __init__(self, *args, **kwargs):
        self.permissions = kwargs.pop("permissions", [])
        self.check_perms = kwargs.pop("check_perms", None)
        auto_permission_message = kwargs.pop("auto_permission_message", True)
        assert isinstance(self.permissions, list), (
            "FieldWithPermissions `permissions` argument must be a list: "
            f"{self.permissions}"
        )
        assert isinstance(self.permissions, list), (
            "FieldWithPermissions `check_perms` argument must be a callable: "
            f"{self.check_perms}"
        )

        assert (
            len(self.permissions) > 0
        ), "Permissions `permissions` are required for PermissionField"
        assert (
            self.check_perms is not None
        ), "Function `check_perms` is required to check permission"

        super().__init__(*args, **kwargs)
        if auto_permission_message and self.permissions:
            permissions_msg = message_one_of_permissions_required(
                self.permissions
            )
            description = self.description or ""
            self.description = description + permissions_msg

    def get_resolver(self, parent_resolver):
        resolver = self.resolver or parent_resolver

        if self.permissions:
            one_of_permissions_required(self.permissions, self.check_perms)(
                resolver
            )
        return resolver
