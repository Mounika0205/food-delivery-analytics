import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

def main():
    file_path = RAW_DIR / "orders_raw.csv"
    df = pd.read_csv(file_path)

    # Keep only useful columns (adjust if your file has slightly different names)
    cols_to_keep = [
        "order_id",
        "order_time",
        "delivery_time",
        "delivery_duration_min",
        "city",
        "state",
        "latitude",
        "longitude",
        "restaurant",
        "is_canceled",
        "cancel_reason",
        "customer_rating",
    ]
    df = df[cols_to_keep]

    # Convert times to datetime
    df["order_time"] = pd.to_datetime(df["order_time"])
    df["delivery_time"] = pd.to_datetime(df["delivery_time"])

    # Delivered flag (True if not canceled)
    df["is_delivered"] = ~df["is_canceled"]

    # Late flag (example: late if > 45 mins)
    df["is_late"] = df["delivery_duration_min"] > 45

    # Make sure processed folder exists
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Save cleaned file
    output_path = PROCESSED_DIR / "orders_clean.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved cleaned data to: {output_path}")
    print("Cleaned shape:", df.shape)

if __name__ == "__main__":
    main()
