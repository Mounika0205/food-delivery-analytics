import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

def main():
    db_path = BASE_DIR / "food_delivery.duckdb"
    con = duckdb.connect(database=str(db_path), read_only=False)

    # Turn the cleaned CSV into a table
    con.execute(f"""
        CREATE OR REPLACE TABLE fact_order AS
        SELECT * FROM read_csv_auto('{PROCESSED_DIR / "orders_clean.csv"}');
    """)

    print("Created table fact_order.")

    # 1) Average delivery duration by city
    print("\nAverage delivery duration (min) by city:")
    avg_by_city = con.execute("""
        SELECT city,
               COUNT(*) AS num_orders,
               AVG(delivery_duration_min) AS avg_duration_min
        FROM fact_order
        WHERE is_delivered = TRUE
        GROUP BY city
        ORDER BY avg_duration_min;
    """).fetchdf()
    print(avg_by_city)

    # 2) Top restaurants by number of delivered orders
    print("\nTop 10 restaurants by number of delivered orders:")
    top_restaurants = con.execute("""
        SELECT restaurant,
               COUNT(*) AS num_orders,
               AVG(customer_rating) AS avg_rating
        FROM fact_order
        WHERE is_delivered = TRUE
        GROUP BY restaurant
        ORDER BY num_orders DESC
        LIMIT 10;
    """).fetchdf()
    print(top_restaurants)

    # 3) Cancellation rate by city
    print("\nCancellation rate by city:")
    cancels_by_city = con.execute("""
        SELECT city,
               COUNT(*) AS total_orders,
               SUM(CASE WHEN is_canceled THEN 1 ELSE 0 END) AS canceled_orders,
               1.0 * SUM(CASE WHEN is_canceled THEN 1 ELSE 0 END) / COUNT(*) AS cancel_rate
        FROM fact_order
        GROUP BY city
        ORDER BY cancel_rate DESC;
    """).fetchdf()
    print(cancels_by_city)

if __name__ == "__main__":
    main()
