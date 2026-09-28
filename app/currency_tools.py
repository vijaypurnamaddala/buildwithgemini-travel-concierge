import json
import urllib.request


def convert_currency(
    amount: float, from_currency: str = "USD", to_currency: str = "EUR"
) -> dict:
    """Converts money between different international currencies using real-time foreign exchange rates.

    Args:
        amount: The amount of money to convert (e.g. 100.0).
        from_currency: 3-letter currency code to convert from (e.g. 'USD', 'EUR', 'GBP', 'JPY', 'CAD').
        to_currency: 3-letter currency code to convert to (e.g. 'EUR', 'JPY', 'GBP', 'USD', 'AUD').

    Returns:
        A dictionary containing the original amount, converted amount, rate, base currency, target currency, and date.
    """
    base = from_currency.upper().strip()
    target = to_currency.upper().strip()

    if base == target:
        return {
            "amount": float(amount),
            "converted_amount": float(amount),
            "rate": 1.0,
            "base": base,
            "target": target,
        }

    url = f"https://api.frankfurter.app/latest?amount={amount}&from={base}&to={target}"
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "TravelConcierge/1.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            converted_val = data.get("rates", {}).get(target)
            if converted_val is None:
                return {"error": f"Currency code '{target}' not supported."}
            return {
                "amount": float(amount),
                "converted_amount": float(converted_val),
                "rate": round(float(converted_val) / float(amount), 4) if amount > 0 else 0.0,
                "base": base,
                "target": target,
                "date": data.get("date"),
            }
    except Exception as e:
        return {"error": f"Failed to fetch currency conversion rates: {e}"}
