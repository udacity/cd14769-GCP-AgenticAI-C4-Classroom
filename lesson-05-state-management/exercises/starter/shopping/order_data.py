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

# Global counter for generating unique order IDs
_order_counter = 1000

def get_next_order_id() -> str:
    """Generates the next sequential order ID."""
    global _order_counter
    _order_counter += 1
    return f"ORDER_{_order_counter}"

