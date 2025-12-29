from enum import Enum

class OrderStatus(Enum):
    PENDING = "pending"
    PLACED = "placed"
    PACKAGED = "packaged"
    SHIPPED = "shipped"
    RECEIVED = "received"

# Shared dictionary
# Key: order_id (str or int)
# Value: dict with keys 'cart', 'address', 'order_status'
orders = {
    "1001": {
        "cart": ["P001", "P002"],
        "address": {
            "name": "John Doe",
            "address_1": "123 Main St",
            "address_2": "",
            "city": "Anytown",
            "state": "CA",
            "postal_code": "90210"
        },
        "order_status": OrderStatus.PLACED
    },
    "1002": {
        "cart": ["P002", "P004"]
    },
    "1003": {
        "cart": ["P001"]
    }
}
