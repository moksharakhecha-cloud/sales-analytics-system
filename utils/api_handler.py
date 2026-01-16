# utils/api_handler.py

import json
import random

# ---------------- Fetch all products from API ----------------
def fetch_all_products():
    """
    Simulate fetching product list from an API.
    Returns a list of product dictionaries.
    """
    products = []
    for i in range(1, 101):  # 100 dummy products
        products.append({
            "ProductID": f"P{i:03d}",
            "ProductName": f"Product{i:03d}",
            "Category": random.choice(["Electronics", "Accessories", "Office"]),
            "Price": round(random.uniform(100, 10000), 2)
        })
    print(f"Successfully fetched {len(products)} products from API.")
    return products

# ---------------- Create product mapping ----------------
def create_product_mapping(products):
    """
    Create a dictionary mapping ProductName -> Product info
    """
    mapping = {prod["ProductName"]: prod for prod in products}
    return mapping

# ---------------- Enrich sales transactions ----------------
def enrich_sales_data(transactions, product_mapping):
    """
    Add API product info to each transaction.
    Adds keys:
        - API_Match (True/False)
        - ProductID
        - Category
        - Price
    """
    enriched = []
    for tx in transactions:
        prod_name = tx.get("Product")
        info = product_mapping.get(prod_name)
        if info:
            tx["API_Match"] = True
            tx["ProductID"] = info["ProductID"]
            tx["Category"] = info["Category"]
            tx["Price"] = info["Price"]
        else:
            tx["API_Match"] = False
            tx["ProductID"] = None
            tx["Category"] = None
            tx["Price"] = None
        enriched.append(tx)
    return enriched

# ---------------- Save enriched data ----------------
def save_enriched_data(transactions, output_file='data/enriched_sales_data.txt'):
    """
    Save enriched transactions to a JSON file.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(transactions, f, indent=4)
        print(f"Enriched data saved to {output_file}")
    except Exception as e:
        print(f"Error saving enriched data: {e}")
