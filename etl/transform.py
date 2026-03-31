import pandas as pd

def transform_data(records):
    df = pd.DataFrame(records)
    bad = []
    required = ["id","primary_type","date","latitude","longitude"]

    for _, r in df.iterrows():
        if any(pd.isnull(r.get(c)) for c in required):
            bad.append(r.to_dict())

    df = df.dropna(subset=required).copy()
    df["date"] = pd.to_datetime(df["date"])
    df["hour_of_day"] = df["date"].dt.hour
    df["day_of_week"] = df["date"].dt.day_name()
    df["season"] = (df["date"].dt.month%12//3+1).map({1:"Winter",2:"Spring",3:"Summer",4:"Fall"})
    df["is_violent"] = df["primary_type"].isin(["ASSAULT","BATTERY","ROBBERY","HOMICIDE"])
    return df, bad
