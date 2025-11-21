from enum import Enum

class OrderStatus(Enum):
    PLACED = "placed"
    PACKAGED = "packaged"
    SHIPPED = "shipped"
    RECEIVED = "received"

# Shared dictionary for orders
# Key: order_id (str)
# Value: dict with keys 'cart', 'address', 'order_status'
orders = {
    "ORDER_001": {
        "cart": ["P001"],
        "address": None,
        "order_status": None
    }
}
