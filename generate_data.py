import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Produits et spécifications
products = {
    "tomato": {"shelf_life": 72, "cost_range": (300, 500)},
    "milk": {"shelf_life": 24, "cost_range": (400, 600)},
    "tilapia": {"shelf_life": 18, "cost_range": (800, 1200)},
    "banana": {"shelf_life": 120, "cost_range": (200, 400)},
}

# --- Génération stock.csv ---
stock_data = []
for i, (prod, specs) in enumerate(products.items(), start=1):
    unit_cost = np.random.randint(*specs["cost_range"])
    stock_data.append({
        "sku_id": f"{prod[:3].upper()}{i:03d}",
        "product": prod,
        "purchased_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "quantity": np.random.randint(20, 100),
        "unit_cost_xaf": unit_cost,
        "shelf_life_hours": specs["shelf_life"],
        "supplier": f"Supplier_{i}"
    })
pd.DataFrame(stock_data).to_csv("stock.csv", index=False)

# --- Génération competitor_prices.csv ---
timestamps = [datetime.now() + timedelta(minutes=30*i) for i in range(48*2)]
competitor_data = []
for ts in timestamps:
    for stall in range(1, 13):
        for prod, specs in products.items():
            daily_mean = np.mean(specs["cost_range"]) * 1.2
            # Oscillation ±15% avec prime du matin
            price = daily_mean * (1 + 0.15*np.sin(2*np.pi*ts.hour/24))
            competitor_data.append({
                "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
                "stall": stall,
                "product": prod,
                "price_xaf": round(price, 2)
            })
pd.DataFrame(competitor_data).to_csv("competitor_prices.csv", index=False)

# --- Génération sales_history.csv ---
sales_data = []
for prod, specs in products.items():
    Q0 = 100
    alpha = 0.5
    p_ref = np.mean(specs["cost_range"])
    for age in range(specs["shelf_life"]):
        freshness_factor = max(0, 1 - (age/specs["shelf_life"])**1.5)
        for price in np.linspace(specs["cost_range"][0], specs["cost_range"][1], 5):
            quantity = Q0 * np.exp(-alpha*(price - p_ref)/p_ref) * freshness_factor
            sales_data.append({
                "product": prod,
                "age_hours": age,
                "price_xaf": round(price, 2),
                "quantity_sold": int(quantity)
            })
pd.DataFrame(sales_data).to_csv("sales_history.csv", index=False)

print("✅ Fichiers générés : stock.csv, competitor_prices.csv, sales_history.csv")
