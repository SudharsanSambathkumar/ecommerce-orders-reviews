"""Part A: clean the orders dataset, then report revenue and best sellers."""
import json
from collections import defaultdict
from pathlib import Path

ORDERS_PATH = Path(__file__).parent / "data" / "orders.json"


def load_orders(path=ORDERS_PATH):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def clean_orders(orders):
    """Return new orders with tidy names and every category filled in.

    A blank category is taken from another order of the same product. If no
    order of that product has one, it becomes "Unknown".
    """
    cleaned = [
        {
            **order,
            "product": order["product"].strip().title(),
            "category": order["category"].strip().title(),
        }
        for order in orders
    ]

    known = {o["product"]: o["category"] for o in cleaned if o["category"]}
    for order in cleaned:
        if not order["category"]:
            order["category"] = known.get(order["product"], "Unknown")
    return cleaned


def revenue_by_category(orders):
    totals = defaultdict(float)
    for order in orders:
        totals[order["category"]] += order["qty"] * order["unit_price"]
    return dict(totals)


def top_products(orders, n=2):
    totals = defaultdict(int)
    for order in orders:
        totals[order["product"]] += order["qty"]
    ranked = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
    return ranked[:n]


def main():
    orders = clean_orders(load_orders())

    print("Revenue per category")
    for category, revenue in sorted(revenue_by_category(orders).items()):
        print(f"  {category}: {revenue:.2f}")

    print("Top 2 products by quantity")
    for product, qty in top_products(orders):
        print(f"  {product}: {qty}")


if __name__ == "__main__":
    main()
