from graphql_service.context import DL
from graphql_service.decorators import decorators
from graphql_service.utils import get_logger

logger = get_logger(__name__)


class DataLoadersMiddleware:
    def resolve(self, next, root, info, **args):
        dataloaders_cls_map = decorators.dataloaders_cls_map
        loaders = info.context.loaders
        for attr, cls_ in dataloaders_cls_map.items():
            loader = getattr(loaders, attr, None)
            if not loader:
                setattr(loaders, attr, cls_(info.context))
        try:
            return next(root, info, **args)
        except Exception as err:
            logger.error(err, exc_info=True, stack_info=True)


class WSGIDataLoadersMiddleware:
    def resolve(self, next, root, info, **args):
        dataloaders_cls_map = decorators.dataloaders_cls_map
        loaders = getattr(info.context, "loaders", None)
        if not loaders:
            info.context.loaders = DL()
        for attr, cls_ in dataloaders_cls_map.items():
            loader = getattr(info.context.loaders, attr, None)
            if not loader:
                setattr(info.context.loaders, attr, cls_(info.context))
        return next(root, info, **args)


class AuthenticationMiddleware:
    def resolve(self, next, root, info, **args):
        context = info.context
        context.user_id = "user"
        return next(root, info, **args)


class RemoveAliasMiddleware(object):
    def resolve(self, next, root, info, **args):

        if info.path and info.path.prev:
            return next(root, info, **args)

        for query_value, fragment in info.fragments.items():
            selection_set = fragment.selection_set
            self.remove_alias([selection_set])

        for field_ast_obj in info.field_nodes:
            selection_set = field_ast_obj.selection_set
            self.remove_alias([selection_set])
        return next(root, info, **args)

    def remove_alias(self, selection_sets):
        from graphql.language.ast import (
            FieldNode,
            InlineFragmentNode,
            SelectionSetNode,
        )

        if not selection_sets:
            return
        new_selection_sets = []
        for selection_set in selection_sets:
            if not selection_set:
                continue
            is_selection_set = type(selection_set) == SelectionSetNode
            if not is_selection_set:
                continue
            selections = selection_set.selections
            for selection_obj in selections:
                is_line_fragment_obj = (
                    type(selection_obj) == InlineFragmentNode
                )
                is_field_obj = type(selection_obj) == FieldNode
                if is_field_obj:
                    selection_obj.alias = None
                    new_selection_sets.append(selection_obj.selection_set)
                if is_line_fragment_obj:
                    new_selection_sets.append(selection_obj.selection_set)
        if new_selection_sets:
            return self.remove_alias(selection_sets=new_selection_sets)


wsgi_middlewares = []
middlewares = [RemoveAliasMiddleware()]
