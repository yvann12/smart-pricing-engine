# 📝 Process Log – Dynamic Pricing Challenge

## 9:00 AM – Kickoff
- Review of the brief and definition of deliverables.

- Creation of the `pricer.py` module with the `suggest_price()` function.

- Justification of the freshness decay formula (power of 1.5).

- CLI test: `python pricer.py --sku TOM123 --now 2026-04-20T09:15`.


## 9:45 AM – Data Generation
- Writing `generate_data.py` to produce `stock.csv`, `competitor_prices.csv`, and `sales_history.csv`.

- Verification of the CSV files with Pandas (`.head()`).

- Setting up the data structures for the simulation.


## 11:00 AM – Simulation
- Creation of the notebook `simulation.ipynb`.

- 7-day simulation loop (30-minute granularity).

- Addition of three strategies: dynamic, naive baseline, cheapest competitor.

- Management of remaining stock, logging of stockouts and waste.


## 12:30 PM – Visualizations & Artifacts
- Addition of graphs: profit, waste, margin, stockouts.

- Automatic generation of `sms_pricesheet.md` (mobile-readable business artifact).

- Writing of `process_log.md` (timeline + tool usage).

- Preparation for the Live Defense (GitHub repo ready, file walkthrough).

---



## Notes on LLM/Tool Usage
- Copilot used to:

- Generate the freshness decline formula.

- Propose the notebook and visualization framework. - Correct errors (`NameError`, `File Save Error`).

- Generate the `sms_pricesheet.md` format.

- Tools used: VS Code, Jupyter, Pandas, Matplotlib, GitHub.