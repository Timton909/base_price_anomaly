# Base — Price Anomaly Detector

Catches two impossible situations:

1. Tiny liquidity (<$50k) but >100% price move in 5 min  
   → Fake pumps or sniper manipulation

2. Huge liquidity (>$500k) but <5% move  
   → Whales quietly absorbing sells — wall building

## Run

```bash
python base_price_anomaly.py
