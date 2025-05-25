"""
Relay Tracker — отслеживает географию ретрансляции Bitcoin-транзакции.
"""

import sys
import requests

def get_relay_data(txid):
    url = f"https://oxt.me/tx/{txid}.json"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Не удалось получить данные от oxt.me")
    return response.json()

def analyze_relay(data):
    nodes = data.get("relayed_by", [])
    countries = {}
    for node in nodes:
        location = node.get("location", {})
        country = location.get("country_name", "Unknown")
        countries[country] = countries.get(country, 0) + 1
    return countries

def main(txid):
    print(f"🌐 Анализ ретрансляции транзакции {txid}...")
    try:
        data = get_relay_data(txid)
        countries = analyze_relay(data)
    except Exception as e:
        print("❌ Ошибка:", e)
        return

    print(f"🌍 Транзакция ретранслировалась из следующих стран:")
    for country, count in countries.items():
        print(f" - {country}: {count} раз")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python relay_tracker.py <txid>")
        sys.exit(1)
    main(sys.argv[1])
