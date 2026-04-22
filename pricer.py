import math
from datetime import datetime

def suggest_price(sku, now, competitor_snapshot, unit_cost, shelf_life_hours, margin_floor=1.1):
    """
    Calcule un prix dynamique pour un produit périssable.
    - sku : dict avec infos produit (inclut 'purchased_at')
    - now : datetime actuel
    - competitor_snapshot : dict {stall: prix}
    - unit_cost : coût unitaire du produit
    - shelf_life_hours : durée de conservation en heures
    - margin_floor : marge minimale (ex: 1.1 = 10%)
    """

    # Âge du produit en heures
    age_hours = (now - sku["purchased_at"]).total_seconds() / 3600

    # Fraîcheur : formule de décroissance (exponentielle/logistique)
    freshness_factor = max(0, 1 - (age_hours / shelf_life_hours)**1.5)

    # Prix moyen des concurrents
    competitor_mean = sum(competitor_snapshot.values()) / len(competitor_snapshot)

    # Prix dynamique basé sur concurrence et fraîcheur
    price = competitor_mean * freshness_factor

    # Contraintes : prix ≥ coût × marge minimale
    min_price = unit_cost * margin_floor
    if price < min_price:
        price = min_price

    return round(price, 2)


# --- CLI ---
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--sku", required=True)
    parser.add_argument("--now", required=True)
    args = parser.parse_args()

    # Exemple de données (à remplacer par lecture CSV)
    sku = {"purchased_at": datetime(2026, 4, 20, 9, 15)}
    competitor_snapshot = {"stall1": 500, "stall2": 520}
    unit_cost = 400
    shelf_life_hours = 72

    now = datetime.fromisoformat(args.now)
    price = suggest_price(sku, now, competitor_snapshot, unit_cost, shelf_life_hours)

    print(f"Suggested price for {args.sku} at {args.now}: {price} XAF")


import pandas as pd

# Charger stock.csv
stock_df = pd.read_csv("stock.csv", parse_dates=["purchased_at"])

# Exemple : récupérer un produit par son sku_id
sku_id = "yvan123"
sku_row = stock_df[stock_df["sku_id"] == sku_id].iloc[0]

sku = {
    "purchased_at": sku_row["purchased_at"],
    "product": sku_row["product"]
}
unit_cost = sku_row["unit_cost_xaf"]
shelf_life_hours = sku_row["shelf_life_hours"]



# Charger competitor_prices.csv
competitor_df = pd.read_csv("competitor_prices.csv", parse_dates=["timestamp"])

# Snapshot des concurrents à l’heure donnée
now = pd.Timestamp("2026-04-20 09:15")
snapshot = competitor_df[
    (competitor_df["timestamp"] == now) & (competitor_df["product"] == sku["product"])
]

competitor_snapshot = dict(zip(snapshot["stall"], snapshot["price_xaf"]))


# appel de suggest_price()
price = suggest_price(sku, now.to_pydatetime(), competitor_snapshot, unit_cost, shelf_life_hours)
print(f"Suggested price for {sku_id} at {now}: {price} XAF")