import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

def main():
    file_path = RAW_DIR / "orders_raw.csv"
    df = pd.read_csv(file_path)

    print("Rows, Columns:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nFirst 5 rows:")
    print(df.head())

if __name__ == "__main__":
    main()

