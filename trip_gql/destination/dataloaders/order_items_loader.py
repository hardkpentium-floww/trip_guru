from feasto_core_clean_arch.models import OrderItem
from graphql_service.dataloaders import BaseDataLoader


class OrderItemsLoader(BaseDataLoader):
    async def batch_load_fn(self, keys):
        pass

