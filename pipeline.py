import pandas as pd


def import_emg(filename):
    """Import emg files

    Args:
        filename (str): name or path of the file to import

    Returns:
        pandas.DataFrame: Dataframe containing emg records
        pandas.Series: Series containing time array
    """
    # FIXME:  Avoid too large upload for not slowing down the App - should be resolved
    df = pd.read_csv(filename, skiprows=range(1, 100000), nrows=30000)
    time_array = pd.to_datetime(df["time"], unit='s')
    # df["time"] = df["time"]-df["time"].iloc[0]
    df.rename(columns={"bic": "Biceps", "bra": "Brachio-radialis",
              "tlat": "Triceps lateral head", "tlng": "Triceps long head"}, inplace=True)

    return df, time_array
