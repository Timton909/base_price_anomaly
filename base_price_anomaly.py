import requests, time

def price_anomaly():
    print("Base — Price Anomaly Detector (price moves too far for available liquidity)")
    seen = set()

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/pairs/base")
            for pair in r.json().get("pairs", []):
                addr = pair["pairAddress"]
                if addr in seen: continue

                liq = pair["liquidity"]["usd"]
                price_change_5m = pair.get("priceChange", {}).get("m5", 0) or 0

                # If < $50k liq but > 100% in 5 min = anomaly (bot manipulation or thin orderbook)
                if liq < 50_000 and abs(price_change_5m) > 100:
                    seen.add(addr)
                    token = pair["baseToken"]["symbol"]
                    print(f"PRICE ANOMALY DETECTED\n"
                          f"{token} {price_change_5m:+.1f}% in 5 min\n"
                          f"Liquidity only ${liq:,.0f}\n"
                          f"https://dexscreener.com/base/{addr}\n"
                          f"→ Impossible move — fake volume or sniper games\n"
                          f"→ Either moonshot or instant rug incoming\n"
                          f"{'ANOMALY'*20}")

                # Or massive liq but tiny move = hidden wall
                if liq > 500_000 and abs(price_change_5m) < 5:
                    seen.add(addr)
                    token = pair["baseToken"]["symbol"]
                    print(f"HIDDEN WALL ANOMALY\n"
                          f"{token} only {price_change_5m:+.1f}% on ${liq:,.0f} liq\n"
                          f"https://dexscreener.com/base/{addr}\n"
                          f"→ Whales are absorbing everything — breakout imminent\n"
                          f"{'WALL'*25}")

        except:
            pass
        time.sleep(5.2)

if __name__ == "__main__":
    price_anomaly()
