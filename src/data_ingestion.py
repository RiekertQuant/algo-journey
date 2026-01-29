import datetime
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

    
def validate_data(sym: str, data: pd.DataFrame) -> tuple[pd.DataFrame, dict]:

    """
    Validation checklist: required columns, numeric types, monotonic date index, no
    duplicate timestamps
    Validation prints: number of rows, start date, end date, count of missing values
    per column
    """

    print("\n")
    print("STARTING VALIDATION FOR:", sym)
    print("=======================================")

    req_cols = ["Open", "High", "Low", "Close", "Volume"]
    req_dtypes = {
        "Open": "float64",
        "High": "float64",
        "Low": "float64",
        "Close": "float64",
        "Volume": "int64",
    }

    data = data.copy()

    # 1) Required columns present?
    missing = [c for c in req_cols if c not in data.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # 2) Ensure datetime index + convert to NY time
    data.index = pd.to_datetime(data.index, utc=True, errors="coerce").tz_convert("America/New_York")
    data.index.name = "Datetime"

    # 3) Coerce numeric columns
    for c in ["Open", "High", "Low", "Close", "Volume"]:
        data[c] = pd.to_numeric(data[c], errors="coerce")

    # Volume -> int64 (handle NaN safely)
    data["Volume"] = data["Volume"].fillna(0).astype("int64")

    # 4) Checks
    is_mono = data.index.is_monotonic_increasing
    has_duplicates = data.index.duplicated().any()
    null_counts = data[req_cols].isna().sum().to_dict()
    bad_index = data.index.isna().any()

    # 5) Final dtype check (after coercion)
    wrong_dtypes = {
        col: str(data[col].dtype)
        for col, expected in req_dtypes.items()
        if str(data[col].dtype) != str(expected)
    }
    if wrong_dtypes:
        raise TypeError(f"Dtype mismatch after coercion: {wrong_dtypes}")

    if bad_index:
        raise ValueError("Datetime index contains NaT after parsing (bad/unparseable timestamps).")

    report = {
        "Symbol": sym,
        "timezone": str(data.index.tz),
        "is_monotonic_increasing": is_mono,
        "has_duplicate_datetimes": has_duplicates,
        "null_counts": null_counts,
        "dtypes": {c: str(data[c].dtype) for c in req_cols},
        "rows": int(len(data)),
        "datetime_min": None if len(data) == 0 else str(data.index.min()),
        "datetime_max": None if len(data) == 0 else str(data.index.max()), 
    }
    return data, report

def plot_close(data, sym):
    os.makedirs("./reports/figures", exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data.index, data["Close"], label=f"{sym} Close Price")
    ax.set_title(f"{sym} Close Price over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price ($)")
    ax.legend()
    ax.grid(True)

    fig.savefig(f"./reports/figures/{sym}.png", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close(fig)

def download_ticker(symbol, prd, intvl):
    data = yf.download(symbol, interval=intvl, period=prd,progress=False)
    

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel("Ticker")
    
    data = data.reset_index()[["Datetime", "Open", "High", "Low", "Close", "Volume"]]
    data.columns.name = None 
    data = data.set_index('Datetime')

    ########validation checks############
    data , report = validate_data(symbol, data)
    print(report)

    ########plots############
    plot_close(data, symbol)


    file_name = f"./data/raw/{symbol}_{prd}_{intvl}_raw.csv"
    data.to_csv(file_name,sep=",")


if __name__ == "__main__":
    my_symbols = ["AAPL", "SPY", "BTC-USD"]

    for s in my_symbols:
        download_ticker(s, "2y", "1h")