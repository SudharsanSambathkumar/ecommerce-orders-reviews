"""Part B.2: model customers, products and categories as a graph and query it.

Customer -purchased-> Product -belongsTo-> Category
Customer -reviewed-> Product (the edge holds the review's sentiment)
"""
import json
from pathlib import Path

import networkx as nx

from orders import clean_orders, load_orders
from sentiment_eval import load_reviews

CUSTOMER_ORDERS_PATH = Path(__file__).parent / "data" / "customer_orders.json"


def build_graph(orders, customer_orders, reviews):
    graph = nx.MultiDiGraph()
    orders_by_id = {order["order_id"]: order for order in orders}

    for order in orders:
        product = f"product:{order['product']}"
        category = f"category:{order['category']}"
        graph.add_node(product, kind="product", name=order["product"])
        graph.add_node(category, kind="category", name=order["category"])
        if not graph.has_edge(product, category, key="belongsTo"):
            graph.add_edge(product, category, key="belongsTo", label="belongsTo")

    for customer, order_ids in customer_orders.items():
        node = f"customer:{customer}"
        graph.add_node(node, kind="customer", name=customer)
        for order_id in order_ids:
            product = f"product:{orders_by_id[order_id]['product']}"
            graph.add_edge(node, product, label="purchased", order_id=order_id)

    for review in reviews:
        graph.add_edge(
            f"customer:{review['customer']}",
            f"product:{review['product']}",
            label="reviewed",
            sentiment=review["reference"],
        )

    return graph


def load_graph():
    customer_orders = json.loads(CUSTOMER_ORDERS_PATH.read_text(encoding="utf-8"))
    return build_graph(clean_orders(load_orders()), customer_orders, load_reviews())


def products_from_negative_reviewers(graph):
    """Products bought by any customer who left at least one negative review."""
    edges = list(graph.edges(data=True))
    negative_reviewers = {
        source
        for source, _, data in edges
        if data["label"] == "reviewed" and data["sentiment"] == "negative"
    }
    return sorted(
        {
            graph.nodes[target]["name"]
            for source, target, data in edges
            if data["label"] == "purchased" and source in negative_reviewers
        }
    )


def main():
    print("Products purchased by customers with a negative review")
    for product in products_from_negative_reviewers(load_graph()):
        print(f"  {product}")


if __name__ == "__main__":
    main()
