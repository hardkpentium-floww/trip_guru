from feasto_gql.restaurant.types.types import Order
from feasto_core_clean_arch.models import Order as OrderModel

def resolve_get_all_orders_for_all_users(root, info):
    order_ids = OrderModel.objects.all().values('id')

    return [Order(id=order_id) for order_id in order_ids]

    order_items_ids = OrderItem.objects.filter(order_id__in=order_ids).values('item_id')

    return order_items_ids