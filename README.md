# E-Commerce Orders & Reviews

## Run it

```
pip install -r requirements.txt
python orders.py
python sentiment_eval.py
python graph.py
pytest
```

## Part A: orders

Cleaning steps in `orders.py`:

- Product and category names are trimmed and put in title case, so `wireless mouse` and `Wireless Mouse` count as one product.
- A blank category is filled from another order of the same product. O3 (Yoga Mat) gets `Fitness` from O5. A product with no category on any order would become `Unknown`.

Revenue per category:

| Category | Revenue |
|---|---|
| Fitness | 105.00 |
| Electronics | 100.00 |
| Home | 25.00 |

Top 2 products by quantity:

| Product | Quantity |
|---|---|
| Yoga Mat | 7 |
| Wireless Mouse | 5 |

## Part B.1: sentiment evaluation

Accuracy is **50% (2 of 4)**.

| Review | Reference | LLM | Match |
|---|---|---|---|
| Works fine but the battery died in a week. | mixed | positive | No |
| Exactly what I needed, five stars! | positive | positive | Yes |
| Arrived broken, waste of money. | negative | negative | Yes |
| It's okay, nothing special. | neutral | positive | No |

Borderline cases:

- **"Works fine but the battery died in a week."** The reference of `mixed` is reasonable because the review has one good and one bad point. You could argue for `negative`, since a battery failing within a week outweighs "works fine". `positive` is the hardest label to defend because it ignores the complaint. The miss is still a real error.
- **"It's okay, nothing special."** This is the more ambiguous one. "Okay" is mildly favourable and "nothing special" takes it back, so the line between neutral and weakly positive depends on the labelling guidelines. A reviewer could accept the LLM's answer here. If it were accepted, accuracy would be 75%.

Both misses go the same way: the LLM picked `positive` when the review was less than fully positive. That could point to a positive bias, but four reviews are too few to confirm it. Each label class has only one example, so the per-class recall of 100% or 0% says very little. A larger set with written label definitions would give a more reliable score.

## Part B.2: graph

```
Customer -purchased-> Product -belongsTo-> Category
Customer -reviewed {sentiment}-> Product
```

The assignment's data doesn't say which customer placed each order or wrote each review, so **I made up these links** to have something to query. They are in `data/customer_orders.json` and `data/reviews.json`.

| Customer | Orders | Review |
|---|---|---|
| C1 | O1 (Wireless Mouse) | Wireless Mouse, mixed |
| C2 | O3 (Yoga Mat) | Yoga Mat, positive |
| C3 | O2 (Wireless Mouse), O4 (Desk Lamp) | Desk Lamp, negative |
| C4 | O5 (Yoga Mat) | Yoga Mat, neutral |

The graph is built with NetworkX and queried by `products_from_negative_reviewers` in `graph.py`. A review counts as negative based on its reference label, not the LLM's label.

The same query in Cypher, for a graph database such as Neo4j. This version has not been run, since the project only uses NetworkX:

```cypher
MATCH (c:Customer)-[:REVIEWED {sentiment: "negative"}]->(:Product)
WITH DISTINCT c
MATCH (c)-[:PURCHASED]->(p:Product)
RETURN DISTINCT p.name
ORDER BY p.name
```

Result: **Desk Lamp, Wireless Mouse**. C3 is the only customer with a negative review. Wireless Mouse is included because C3 bought it too, even though the negative review was for the lamp.
