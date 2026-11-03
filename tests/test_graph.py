from graph import build_graph, load_graph, products_from_negative_reviewers


def order(order_id, product, category):
    return {"order_id": order_id, "product": product, "category": category, "qty": 1, "unit_price": 1.0}


def review(customer, product, reference):
    return {"customer": customer, "product": product, "text": "t", "reference": reference, "llm": "positive"}


def edge_labels(graph, source, target):
    return {data["label"] for data in graph.get_edge_data(source, target).values()}


def test_builds_purchased_and_belongs_to_edges():
    graph = build_graph([order("O1", "Mat", "Fitness")], {"C1": ["O1"]}, [])
    assert edge_labels(graph, "customer:C1", "product:Mat") == {"purchased"}
    assert edge_labels(graph, "product:Mat", "category:Fitness") == {"belongsTo"}


def test_builds_reviewed_edge_carrying_sentiment():
    graph = build_graph(
        [order("O1", "Mat", "Fitness")], {"C1": ["O1"]}, [review("C1", "Mat", "negative")]
    )
    edges = graph.get_edge_data("customer:C1", "product:Mat").values()
    reviewed = [data for data in edges if data["label"] == "reviewed"]
    assert reviewed[0]["sentiment"] == "negative"


def test_query_includes_products_the_customer_did_not_review():
    orders = [order("O1", "Lamp", "Home"), order("O2", "Mouse", "Tech")]
    graph = build_graph(orders, {"C1": ["O1", "O2"]}, [review("C1", "Lamp", "negative")])
    assert products_from_negative_reviewers(graph) == ["Lamp", "Mouse"]


def test_query_ignores_customers_without_a_negative_review():
    orders = [order("O1", "Lamp", "Home"), order("O2", "Mouse", "Tech")]
    graph = build_graph(
        orders,
        {"C1": ["O1"], "C2": ["O2"]},
        [review("C1", "Lamp", "negative"), review("C2", "Mouse", "mixed")],
    )
    assert products_from_negative_reviewers(graph) == ["Lamp"]


def test_assignment_data_query_result():
    assert products_from_negative_reviewers(load_graph()) == ["Desk Lamp", "Wireless Mouse"]
