"""
Created on: 01/05/23
"""
import importlib
import inspect
import json
import re

import graphene
from corsheaders.conf import conf
from django.db import connection, transaction
from django.http import HttpResponse, HttpResponseNotAllowed
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View
from graphene import Schema
from graphql import OperationType, get_operation_ast, parse, validate
from graphql.error import GraphQLError
from graphql.error.graphql_error import format_error as format_graphql_error
from graphql.execution import ExecutionResult
from graphql.execution.middleware import MiddlewareManager

from graphql_service.context import Context
from graphql_service.utils import get_logger

unhandled_errors_logger = get_logger(__name__)

ACCESS_CONTROL_ALLOW_ORIGIN = "Access-Control-Allow-Origin"
ACCESS_CONTROL_EXPOSE_HEADERS = "Access-Control-Expose-Headers"
ACCESS_CONTROL_ALLOW_CREDENTIALS = "Access-Control-Allow-Credentials"
ACCESS_CONTROL_ALLOW_HEADERS = "Access-Control-Allow-Headers"
ACCESS_CONTROL_ALLOW_METHODS = "Access-Control-Allow-Methods"
ACCESS_CONTROL_MAX_AGE = "Access-Control-Max-Age"


class HttpError(Exception):
    def __init__(self, response, message=None, *args, **kwargs):
        self.response = response
        self.message = message = message or response.content.decode()
        super(HttpError, self).__init__(message, *args, **kwargs)


class NotSupportedEnvironment(Exception):
    pass


def get_accepted_content_types(request):
    def qualify(x):
        parts = x.split(";", 1)
        if len(parts) == 2:
            match = re.match(
                r"(^|;)q=(0(\.\d{,3})?|1(\.0{,3})?)(;|$)", parts[1]
            )
            if match:
                return parts[0].strip(), float(match.group(2))
        return parts[0].strip(), 1

    raw_content_types = request.META.get("HTTP_ACCEPT", "*/*").split(",")
    qualified_content_types = map(qualify, raw_content_types)
    return list(
        x[0]
        for x in sorted(
            qualified_content_types, key=lambda x: x[1], reverse=True
        )
    )


def instantiate_middleware(middlewares):
    for middleware in middlewares:
        if inspect.isclass(middleware):
            yield middleware()
            continue
        yield middleware


class GraphQLViewDev(View):
    graphiql_template = "graphiql.html"

    # Polyfill for window.fetch.
    whatwg_fetch_version = "3.6.2"
    whatwg_fetch_sri = "sha256-+pQdxwAcHJdQ3e/9S4RK6g8ZkwdMgFQuHvLuN5uyk5c="

    # React and ReactDOM.
    react_version = "17.0.2"
    react_sri = "sha256-Ipu/TQ50iCCVZBUsZyNJfxrDk0E2yhaEIz0vqI+kFG8="
    react_dom_sri = "sha256-nbMykgB6tsOFJ7OdVmPpdqMFVk4ZsqWocT6issAPUF0="

    # The GraphiQL React app.
    graphiql_version = "1.4.1"  # "1.0.3"
    graphiql_sri = "sha256-JUMkXBQWZMfJ7fGEsTXalxVA10lzKOS9loXdLjwZKi4="  # "sha256-VR4buIDY9ZXSyCNFHFNik6uSe0MhigCzgN4u7moCOTk="
    graphiql_css_sri = "sha256-Md3vdR7PDzWyo/aGfsFVF4tvS5/eAUWuIsg9QHUusCY="  # "sha256-LwqxjyZgqXDYbpxQJ5zLQeNcf7WVNSJ+r8yp2rnWE/E="

    # The websocket transport library for subscriptions.
    subscriptions_transport_ws_version = "0.9.18"
    subscriptions_transport_ws_sri = (
        "sha256-i0hAXd4PdJ/cHX3/8tIy/Q/qKiWr5WSTxMFuL9tACkw="
    )

    graphiql = False
    middleware = None
    root_value = None
    pretty = False
    batch = False
    subscription_path = None
    execution_context_class = None

    def __init__(
        self,
        middleware=None,
        root_value=None,
        graphiql=False,
        pretty=False,
        batch=False,
        execution_context_class=None,
    ):
        if middleware is not None:
            if isinstance(middleware, MiddlewareManager):
                self.middleware = middleware
            else:
                self.middleware = list(instantiate_middleware(middleware))
        self.root_value = root_value
        self.pretty = self.pretty or pretty
        self.graphiql = self.graphiql or graphiql
        self.batch = self.batch or batch
        self.execution_context_class = execution_context_class

        assert not all(
            (graphiql, batch)
        ), "Use either graphiql or batch processing"

    # noinspection PyUnusedLocal
    def get_root_value(self, request):
        return self.root_value

    def get_middleware(self, request):
        return self.middleware

    def get_context(self, request):
        from graphql_service.context import get_context_value

        return get_context_value(request)

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        from django.conf import settings

        if settings.STAGE not in ["local", "alpha", "beta"]:
            raise NotSupportedEnvironment()

        request.exec_time = 0
        try:
            if request.method.lower() not in ("get", "post"):
                raise HttpError(
                    HttpResponseNotAllowed(
                        ["GET", "POST"],
                        "GraphQL only supports GET and POST requests.",
                    )
                )

            data = self.parse_body(request)
            show_graphiql = self.graphiql and self.can_display_graphiql(
                request, data
            )

            if show_graphiql:
                return self.render_graphiql(
                    request,
                    # Dependency parameters.
                    whatwg_fetch_version=self.whatwg_fetch_version,
                    whatwg_fetch_sri=self.whatwg_fetch_sri,
                    react_version=self.react_version,
                    react_sri=self.react_sri,
                    react_dom_sri=self.react_dom_sri,
                    graphiql_version=self.graphiql_version,
                    graphiql_sri=self.graphiql_sri,
                    graphiql_css_sri=self.graphiql_css_sri,
                    subscriptions_transport_ws_version=self.subscriptions_transport_ws_version,
                    subscriptions_transport_ws_sri=self.subscriptions_transport_ws_sri,
                    # The SUBSCRIPTION_PATH setting.
                    subscription_path=self.subscription_path,
                    # GraphiQL headers tab,
                    graphiql_header_editor_enabled=True,
                    graphiql_should_persist_headers=True,
                )

            if self.batch:
                responses = [
                    self.get_response(request, entry) for entry in data
                ]
                result = "[{}]".format(
                    ",".join([response[0] for response in responses])
                )
                status_code = (
                    responses
                    and max(responses, key=lambda response: response[1])[1]
                    or 200
                )
            else:
                result, status_code = self.get_response(
                    request, data, show_graphiql
                )

            response = HttpResponse(
                status=status_code,
                content=result,
                content_type="application/json",
            )

            origin = request.META.get("HTTP_ORIGIN")

            if conf.CORS_ALLOW_CREDENTIALS:
                response[ACCESS_CONTROL_ALLOW_CREDENTIALS] = "true"

            is_cors_origin_allow_all = getattr(
                conf, "CORS_ORIGIN_ALLOW_ALL", None
            ) or getattr(conf, "CORS_ALLOW_ALL_ORIGINS", None)
            if is_cors_origin_allow_all and not conf.CORS_ALLOW_CREDENTIALS:
                response[ACCESS_CONTROL_ALLOW_ORIGIN] = "*"
            else:
                response[ACCESS_CONTROL_ALLOW_ORIGIN] = origin

            if len(conf.CORS_EXPOSE_HEADERS):
                response[ACCESS_CONTROL_EXPOSE_HEADERS] = ", ".join(
                    conf.CORS_EXPOSE_HEADERS
                )

            if request.method == "OPTIONS":
                response[ACCESS_CONTROL_ALLOW_HEADERS] = ", ".join(
                    conf.CORS_ALLOW_HEADERS
                )
                response[ACCESS_CONTROL_ALLOW_METHODS] = ", ".join(
                    conf.CORS_ALLOW_METHODS
                )
                if conf.CORS_PREFLIGHT_MAX_AGE:
                    response[
                        ACCESS_CONTROL_MAX_AGE
                    ] = conf.CORS_PREFLIGHT_MAX_AGE

            return response

        except HttpError as e:
            response = e.response
            response["Content-Type"] = "application/json"
            response.content = self.json_encode(
                request, {"errors": [self.format_error(e)]}
            )
            return response

    def get_response(self, request, data, show_graphiql=False):
        query, variables, operation_name, id = self.get_graphql_params(
            request, data
        )

        execution_result = self.execute_graphql_request(
            request, data, query, variables, operation_name, show_graphiql
        )

        status_code = 200
        if execution_result:
            response = {}

            if execution_result.errors:
                response["errors"] = [
                    self.format_error(e) for e in execution_result.errors
                ]

            if execution_result.errors and any(
                not getattr(e, "path", None) for e in execution_result.errors
            ):
                status_code = 400
            else:
                response["data"] = execution_result.data

            if self.batch:
                response["id"] = id
                response["status"] = status_code

            result = self.json_encode(request, response, pretty=show_graphiql)
        else:
            result = None

        return result, status_code

    def render_graphiql(self, request, **data):
        return render(request, self.graphiql_template, data)

    def json_encode(self, request, d, pretty=False):
        if not (self.pretty or pretty) and not request.GET.get("pretty"):
            return json.dumps(d, separators=(",", ":"))

        return json.dumps(d, sort_keys=True, indent=2, separators=(",", ": "))

    def parse_body(self, request):
        content_type = self.get_content_type(request)

        if content_type == "application/graphql":
            return {"query": request.body.decode()}

        elif content_type == "application/json":
            # noinspection PyBroadException
            try:
                body = request.body.decode("utf-8")
            except Exception as e:
                raise HttpError(HttpResponseBadRequest(str(e)))

            try:
                request_json = json.loads(body)
                if self.batch:
                    assert isinstance(request_json, list), (
                        "Batch requests should receive a list, but received {}."
                    ).format(repr(request_json))
                    assert (
                        len(request_json) > 0
                    ), "Received an empty list in the batch request."
                else:
                    assert isinstance(
                        request_json, dict
                    ), "The received data is not a valid JSON query."
                return request_json
            except AssertionError as e:
                raise HttpError(HttpResponseBadRequest(str(e)))
            except (TypeError, ValueError):
                raise HttpError(
                    HttpResponseBadRequest("POST body sent invalid JSON.")
                )

        elif content_type in [
            "application/x-www-form-urlencoded",
            "multipart/form-data",
        ]:
            return request.POST

        return {}

    def execute_graphql_request(
        self,
        request,
        data,
        query,
        variables,
        operation_name,
        show_graphiql=False,
    ):
        if not query:
            if show_graphiql:
                return None
            raise HttpError(
                HttpResponseBadRequest("Must provide query string.")
            )

        try:
            document = parse(query)
        except Exception as e:
            return ExecutionResult(errors=[e])

        if request.method.lower() == "get":
            operation_ast = get_operation_ast(document, operation_name)
            if (
                operation_ast
                and operation_ast.operation != OperationType.QUERY
            ):
                if show_graphiql:
                    return None

                raise HttpError(
                    HttpResponseNotAllowed(
                        ["POST"],
                        "Can only perform a {} operation from a POST request.".format(
                            operation_ast.operation.value
                        ),
                    )
                )

        try:
            extra_options = {}
            if self.execution_context_class:
                extra_options[
                    "execution_context_class"
                ] = self.execution_context_class

            options = {
                "source": query,
                "root_value": self.get_root_value(request),
                "variable_values": variables,
                "operation_name": operation_name,
                "context_value": self.get_context(request),
                "middleware": self.get_middleware(request),
            }
            options.update(extra_options)

            operation_ast = get_operation_ast(document, operation_name)
            if (
                operation_ast
                and operation_ast.operation == OperationType.MUTATION
                and connection.settings_dict.get("ATOMIC_MUTATIONS", False)
                is True
            ):
                with transaction.atomic():
                    result = self.execute_graphql_as_sync(**options)

                return result

            return self.execute_graphql_as_sync(**options)
        except Exception as e:
            return ExecutionResult(errors=[e])

    def execute_graphql_as_sync(self, **options):
        from django.conf import settings

        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(schema.execute_async(**options))
        loop.close()
        return result

    @classmethod
    def can_display_graphiql(cls, request, data):
        raw = "raw" in request.GET or "raw" in data
        return not raw and cls.request_wants_html(request)

    @classmethod
    def request_wants_html(cls, request):
        accepted = get_accepted_content_types(request)
        accepted_length = len(accepted)
        # the list will be ordered in preferred first - so we have to make
        # sure the most preferred gets the highest number
        html_priority = (
            accepted_length - accepted.index("text/html")
            if "text/html" in accepted
            else 0
        )
        json_priority = (
            accepted_length - accepted.index("application/json")
            if "application/json" in accepted
            else 0
        )

        return html_priority > json_priority

    @staticmethod
    def get_graphql_params(request, data):
        query = request.GET.get("query") or data.get("query")
        variables = request.GET.get("variables") or data.get("variables")
        id = request.GET.get("id") or data.get("id")

        if variables and isinstance(variables, str):
            try:
                variables = json.loads(variables)
            except Exception:
                raise HttpError(
                    HttpResponseBadRequest("Variables are invalid JSON.")
                )

        operation_name = request.GET.get("operationName") or data.get(
            "operationName"
        )
        if operation_name == "null":
            operation_name = None

        return query, variables, operation_name, id

    @staticmethod
    def format_error(error):
        import traceback

        if isinstance(error, GraphQLError):
            result = format_graphql_error(error)
        else:
            result = {"message": str(error)}

        if "extensions" not in result:
            result["extensions"] = {}

        exc = error
        while isinstance(exc, GraphQLError) and hasattr(exc, "original_error"):
            exc = exc.original_error
        if isinstance(exc, AssertionError):
            exc = GraphQLError(str(exc))

        unhandled_errors_logger.error(
            "A query failed unexpectedly", exc_info=exc
        )
        result["extensions"]["exception"] = {"code": type(exc).__name__}

        from django.conf import settings

        if settings.DEBUG:
            lines = []
            if isinstance(exc, BaseException):
                for line in traceback.format_exception(
                    type(exc), exc, exc.__traceback__
                ):
                    lines.extend(line.rstrip().splitlines())
            result["extensions"]["exception"]["stacktrace"] = lines
        return result

    @staticmethod
    def get_content_type(request):
        meta = request.META
        content_type = meta.get(
            "CONTENT_TYPE", meta.get("HTTP_CONTENT_TYPE", "")
        )
        return content_type.split(";", 1)[0].lower()
