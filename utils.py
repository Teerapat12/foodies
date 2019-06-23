import pandas as pd
def read_csv(table_name):
    return pd.read_csv("data/foodies_table_%s.csv"%table_name)