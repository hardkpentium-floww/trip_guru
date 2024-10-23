import functools
import importlib
import json
import os
from typing import Dict, List

from django.core.management.base import BaseCommand, CommandError
from django.utils import autoreload

from graphql_service.schema_printer import print_schema


def is_public_operation(field) -> bool:
    if not field.args.get("isPublicOperation"):
        return False
    return True


class CommandArguments(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--schema",
            type=str,
            dest="schema",
            help="Django app containing schema to dump, e.g. myproject.core.schema.schema",
        )

        parser.add_argument(
            "--out",
            type=str,
            dest="out",
            help="Output file, --out=- prints to stdout (default: schema.json)",
        )

        parser.add_argument(
            "--indent",
            type=int,
            dest="indent",
            default=2,
            help="Output file indent (default: None)",
        )

        parser.add_argument(
            "--watch",
            dest="watch",
            default=False,
            action="store_true",
            help="Updates the schema on file changes (default: False)",
        )

        parser.add_argument(
            "--schema_enum",
            dest="schema_enum",
            type=str,
            help="Picks the schema object respective to given schema enum",
        )


class Command(CommandArguments):
    help = "Dump Graphene schema as a JSON or GraphQL file"
    can_import_settings = True
    requires_system_checks = []

    def save_json_file(self, out, schema_dict, indent):
        with open(out, "w") as outfile:
            json.dump(schema_dict, outfile, indent=indent, sort_keys=True)

    def save_graphql_file(self, out, schema):
        with open(out, "w", encoding="utf-8") as outfile:
            outfile.write(print_schema(schema.graphql_schema))

    @staticmethod
    def get_operations_schema_config(
        operation_classes,
    ) -> Dict[str, List[str]]:
        operations_config = {}
        for query_class in operation_classes:
            operations = query_class().__dict__.keys()
            query_class_path = (
                f"{query_class.__module__}.{query_class.__qualname__}"
            )
            for operation in operations:
                op_words = operation.split("_")
                capitalized_op_words = []
                for index, word_ in enumerate(op_words):
                    if index == 0:
                        capitalized_op_words.append(word_)
                        continue
                    capitalized_op_words.append(word_.capitalize())
                op_name = "".join(capitalized_op_words)
                operations_config[op_name] = [query_class_path]
        return operations_config

    @staticmethod
    def get_public_operations(schema) -> List[str]:
        public_operations = []

        query_type = schema.query_type
        mutation_type = schema.mutation_type
        for i, (name, field) in enumerate(query_type.fields.items()):
            if is_public_operation(field):
                public_operations.append(name)

        for i, (name, field) in enumerate(mutation_type.fields.items()):
            if is_public_operation(field):
                public_operations.append(name)

        return public_operations

    def get_schema(self, schema, out, indent):
        schema_dict = {"data": schema.introspect()}
        if out == "-" or out == "-.json":
            self.stdout.write(
                json.dumps(schema_dict, indent=indent, sort_keys=True)
            )
        elif out == "-.graphql":
            self.stdout.write(print_schema(schema))
        else:
            # Determine format
            _, file_extension = os.path.splitext(out)

            if file_extension == ".graphql":
                self.save_graphql_file(out, schema)
            elif file_extension == ".json":
                self.save_json_file(out, schema_dict, indent)
            else:
                raise CommandError(
                    'Unrecognised file format "{}"'.format(file_extension)
                )

            style = getattr(self, "style", None)
            success = getattr(style, "SUCCESS", lambda x: x)

            self.stdout.write(
                success("Successfully dumped GraphQL schema to {}".format(out))
            )

    def handle(self, *args, **options):
        options_schema = options.get("schema")
        schema_file_name = options.get("out")

        schema = None

        if options_schema and type(options_schema) is str:
            module_str, schema_name = options_schema.rsplit(".", 1)
            mod = importlib.import_module(module_str)
            schema = getattr(mod, schema_name)

        elif options_schema:
            schema = options_schema

        if schema_file_name:
            out = f"graphql_service/{schema_file_name}.graphql"
        else:
            out = "graphql_service/schema.graphql"

        if not schema:
            raise CommandError(
                "Specify schema on GRAPHENE.SCHEMA setting or by using --schema"
            )

        indent = options.get("indent")
        watch = options.get("watch")
        if watch:
            autoreload.run_with_reloader(
                functools.partial(self.get_schema, schema, out, indent)
            )
        else:
            self.get_schema(schema, out, indent)
