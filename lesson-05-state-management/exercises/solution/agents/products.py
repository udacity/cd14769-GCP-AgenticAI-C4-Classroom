# Shared dictionary for product catalog
# Key: product_id
# Value: dict with name, description, price
products = {
    "P001": {
        "name": "Wireless Headphones",
        "description": "Noise cancelling over-ear headphones",
        "price": 299.99
    },
    "P002": {
        "name": "Smartphone Stand",
        "description": "Adjustable aluminum stand for all smartphones",
        "price": 19.99
    },
    "P003": {
        "name": "Bluetooth Speaker",
        "description": "Portable waterproof speaker with 20h battery life",
        "price": 59.99
    },
    "P004": {
        "name": "USB-C Cable",
        "description": "2-meter braided fast charging cable",
        "price": 12.99
    },
    "P005": {
        "name": "Portable Charger",
        "description": "10000mAh power bank with fast charging",
        "price": 29.99,
    },
    "P006": {
        "name": "Laptop Sleeve",
        "description": "Protective sleeve for 13-inch laptops",
        "price": 24.99,
    },
    "P007": {
        "name": "Wireless Mouse",
        "description": "Ergonomic wireless mouse with USB receiver",
        "price": 19.99,
    },
    "P008": {
        "name": "Mechanical Keyboard",
        "description": "RGB backlit mechanical gaming keyboard",
        "price": 89.99,
    },
    "P009": {
        "name": "HDMI Cable",
        "description": "3-meter high-speed HDMI 2.1 cable",
        "price": 14.99,
    },
    "P010": {
        "name": "Smart Watch",
        "description": "Fitness tracker with heart rate monitor",
        "price": 149.99,
    },
    "P011": {
        "name": "Tablet Case",
        "description": "Rugged protective case for 10-inch tablets",
        "price": 19.99,
    },
    "P012": {
        "name": "Webcam",
        "description": "1080p HD webcam with built-in microphone",
        "price": 49.99,
    },
    "P013": {
        "name": "USB Hub",
        "description": "4-port USB 3.0 data hub",
        "price": 15.99,
    },
    "P014": {
        "name": "Monitor Stand",
        "description": "Dual monitor desk mount stand",
        "price": 39.99,
    }
}

# Shared dictionary for inventory counts
# Key: product_id
# Value: int (inventory count)
product_counts = {
    "P001": 50,
    "P002": 150,
    "P003": 0,  # Out of stock
    "P004": 500,
    "P005": 100,
    "P006": 75,
    "P007": 200,
    "P008": 40,
    "P009": 300,
    "P010": 60,
    "P011": 80,
    "P012": 45,
    "P013": 120,
    "P014": 25
}
