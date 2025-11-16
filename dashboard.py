import pandas as pd
from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

@st.cache_data
def load_data():
    file_path = PROCESSED_DIR / "orders_clean.csv"
    df = pd.read_csv(file_path, parse_dates=["order_time", "delivery_time"])
    return df

def main():
    st.title("🍔 Food Delivery Analytics Dashboard")

    df = load_data()

    # ----- Overview KPIs -----
    st.subheader("Overview")

    total_orders = len(df)
    delivered_orders = df["is_delivered"].sum()
    avg_duration = df.loc[df["is_delivered"], "delivery_duration_min"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Orders", total_orders)
    col2.metric("Delivered Orders", delivered_orders)
    col3.metric("Avg Delivery Time (min)", f"{avg_duration:.1f}")

    st.write("---")

    # ----- Average delivery duration by city -----
    st.subheader("Average Delivery Time by City (Delivered Orders Only)")

    avg_by_city = (
        df[df["is_delivered"]]
        .groupby("city")["delivery_duration_min"]
        .agg(["count", "mean"])
        .reset_index()
        .rename(columns={"count": "num_orders", "mean": "avg_duration_min"})
        .sort_values("avg_duration_min")
    )

    st.dataframe(avg_by_city)

    st.bar_chart(
        data=avg_by_city,
        x="city",
        y="avg_duration_min",
    )

    st.write("---")

    # ----- Top restaurants by number of delivered orders -----
    st.subheader("Top Restaurants by Delivered Orders")

    top_n = st.slider("Number of restaurants to show", min_value=5, max_value=30, value=10, step=5)

    top_restaurants = (
        df[df["is_delivered"]]
        .groupby("restaurant")
        .agg(num_orders=("order_id", "count"),
             avg_rating=("customer_rating", "mean"))
        .reset_index()
        .sort_values("num_orders", ascending=False)
        .head(top_n)
    )

    st.dataframe(top_restaurants)

    st.bar_chart(
        data=top_restaurants,
        x="restaurant",
        y="num_orders",
    )

    st.write("---")

    # ----- Cancellation rate by city -----
    st.subheader("Cancellation Rate by City")

    cancels_by_city = (
        df
        .groupby("city")
        .agg(
            total_orders=("order_id", "count"),
            canceled_orders=("is_canceled", "sum")
        )
        .reset_index()
    )
    cancels_by_city["cancel_rate"] = (
        cancels_by_city["canceled_orders"] / cancels_by_city["total_orders"]
    )

    cancels_by_city = cancels_by_city.sort_values("cancel_rate", ascending=False)

    st.dataframe(cancels_by_city)

    st.bar_chart(
        data=cancels_by_city,
        x="city",
        y="cancel_rate",
    )

if __name__ == "__main__":
    main()
