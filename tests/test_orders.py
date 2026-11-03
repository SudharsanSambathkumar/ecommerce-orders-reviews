from orders import clean_orders, load_orders, revenue_by_category, top_products


def order(order_id, product, category, qty=1, unit_price=10.0):
    return {
        "order_id": order_id,
        "product": product,
        "category": category,
        "qty": qty,
        "unit_price": unit_price,
    }


def test_product_casing_and_spacing_are_normalised():
    cleaned = clean_orders([order("O1", "  wireless MOUSE ", "Electronics")])
    assert cleaned[0]["product"] == "Wireless Mouse"


def test_category_casing_is_normalised():
    cleaned = clean_orders([order("O1", "Mouse", "electronics")])
    assert cleaned[0]["category"] == "Electronics"


def test_missing_category_is_taken_from_another_order_of_the_same_product():
    cleaned = clean_orders([order("O1", "Yoga Mat", ""), order("O2", "yoga mat", "fitness")])
    assert cleaned[0]["category"] == "Fitness"


def test_category_is_unknown_when_no_order_of_the_product_has_one():
    cleaned = clean_orders([order("O1", "Mystery Box", "  ")])
    assert cleaned[0]["category"] == "Unknown"


def test_clean_does_not_change_the_input():
    raw = [order("O1", "wireless mouse", "")]
    clean_orders(raw)
    assert raw[0]["product"] == "wireless mouse"
    assert raw[0]["category"] == ""


def test_revenue_is_qty_times_price_summed_per_category():
    orders = [
        order("O1", "A", "X", qty=2, unit_price=5.0),
        order("O2", "B", "X", qty=1, unit_price=3.0),
        order("O3", "C", "Y", qty=4, unit_price=1.0),
    ]
    assert revenue_by_category(orders) == {"X": 13.0, "Y": 4.0}


def test_top_products_ranks_by_total_quantity_not_order_count():
    orders = [
        order("O1", "A", "X", qty=1),
        order("O2", "A", "X", qty=1),
        order("O3", "B", "X", qty=5),
        order("O4", "C", "X", qty=1),
    ]
    assert top_products(orders, 2) == [("B", 5), ("A", 2)]


def test_top_products_breaks_ties_alphabetically():
    orders = [order("O1", "Zed", "X", qty=3), order("O2", "Abe", "X", qty=3)]
    assert top_products(orders, 1) == [("Abe", 3)]


def test_assignment_dataset_answers():
    cleaned = clean_orders(load_orders())
    assert revenue_by_category(cleaned) == {"Electronics": 100.0, "Fitness": 105.0, "Home": 25.0}
    assert top_products(cleaned, 2) == [("Yoga Mat", 7), ("Wireless Mouse", 5)]
