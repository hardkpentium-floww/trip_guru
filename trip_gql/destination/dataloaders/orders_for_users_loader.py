from feasto_core_clean_arch.models import Order
from graphql_service.dataloaders import BaseDataLoader


class AllOrdersForAllUsersLoader(BaseDataLoader):
    async def batch_load_fn(self, keys):
        pass

