import os
import pandas as pd

def read_csv(table_name):
    return pd.read_csv("data/foodies_table_%s.csv"%table_name)



class FoodiesData:
    def __init__(self, path):
        self.path = path
        self.dfs = self._load_data()
        
    def summary(self):
        for df_name, df in self.dfs.items():
            print("%s's shape: %s"%(df_name, df.shape))
        
    
    def _load_data(self):
        files = []
        dfs = {}
        for _, _, f in os.walk(self.path):
            for file in f:
                if '.csv' in file:
                    file = self._get_table_name(file)
                    dfs[file] = self._read_csv(file)
        return dfs
    
    def _get_table_name(self, full_table_name):
        return full_table_name.replace("foodies_table_", "").replace(".csv","")
    
    def _read_csv(self, table_name):
        return pd.read_csv("data/foodies_table_%s.csv"%table_name)