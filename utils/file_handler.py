import pandas as pd

def load_file(path):
    return pd.read_excel(path)

def save_file(df, path):
    df.to_excel(path, index=False)