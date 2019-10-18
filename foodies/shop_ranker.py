import pandas as pd
import math

## Code from Here: https://janakiev.com/blog/gps-points-distance-python/
def euclidean_distance_calculator(lat1, lon1):
    def calculate(row):
    
        R = 6372800  # Earth radius in meters
        lat2, lon2 = row["lat"], row["lng"]

        phi1, phi2 = math.radians(lat1), math.radians(lat2) 
        dphi       = math.radians(lat2 - lat1)
        dlambda    = math.radians(lon2 - lon1)

        a = math.sin(dphi/2)**2 + \
            math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2

        return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return calculate

def distance_score_calculator(score):
    if(score<1):
        return 1.1
    elif(score<5):
        return 1
    else:
        return 0.8


# TODO: Move me as file
class ShopRanker():
    def __init__(
        self,
        preped_shop_df,
        default_weights, 
        distance_calculator = euclidean_distance_calculator,
        distance_scorer = distance_score_calculator
    ):
        self.origin_df = preped_shop_df.copy()
        self.default_weights = default_weights
        self.distance_calculator = distance_calculator
        self.distance_scorer = distance_scorer
        self.df = self.calculate_scores()
    
    def calculate_scores(self):
        scores_summary = self.origin_df.apply(self._apply_score(self.default_weights), axis=1)
        df = self.origin_df.copy()
        df['scores_breakdown'] = scores_summary
        df['scores'] = scores_summary.apply(sum)
        df["normalized_scores"] = df.scores + abs(df.scores.min()) + 1 # Ensure no negative
        return df
        
    def _apply_score(self, weights):
        def f(row):
            return [row[weight]*weights[weight] for weight in weights]
        return f
    
    def get_top_rank(self, n=10, location=None):
        if location is None:
            return self.default_search()
        else:
            lat, lng = location["lat"], location["lng"]
            calculator = self.distance_calculator(lat, lng)
            df = self.df.copy()
            df["distance"] = df[["lat", "lng"]].apply(calculator, axis=1)
            
            nearest_shops = df.sort_values("distance").head(250)
            
            nearest_shops["distance_weight"] = nearest_shops.distance.apply(self.distance_scorer)
            nearest_shops["weighted_scores"] = nearest_shops["distance_weight"] * nearest_shops["normalized_scores"]
            return nearest_shops.sort_values("weighted_scores", ascending=False).head(n)[["name", "description", "lat", "lng", "distance", "normalized_scores", "weighted_scores"]]
            
    def default_search(self):
        return self.df_with_scores.sort_values("scores")