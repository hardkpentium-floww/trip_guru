from graphql_service.dataloaders import BaseDataLoader
from feasto_core_clean_arch.models.user import User


class RestaurantUserLoader(BaseDataLoader):
    async def batch_load(self, keys):
        users = User.objects.filter(id__in=keys)
        user_map = {user.id: user for user in users}
        return [user_map.get(key) for key in keys]

