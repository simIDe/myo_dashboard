import pandas as pd


def import_emg(filename):
    df = pd.read_csv(filename)
    df = df[20000:35000]
    df['time'] = pd.to_datetime(df["time"], unit='s')  # .dt.time
    return df
