import json
import os
import urllib.parse
import urllib.request


def _get_api_key() -> str:
    key = os.environ.get("GOOGLE_MAPS_API_KEY", "").strip()
    if not key:
        raise ValueError("GOOGLE_MAPS_API_KEY environment variable is not set in .env")
    return key


def geocode_address(address: str) -> dict:
    """Converts a street address or location name into geographic coordinates (latitude and longitude).

    Args:
        address: The address or place name to geocode (e.g. '1600 Amphitheatre Pkwy, Mountain View, CA' or 'Eiffel Tower, Paris').

    Returns:
        A dictionary containing formatted_address, latitude, longitude, and place_id.
    """
    try:
        api_key = _get_api_key()
    except ValueError as e:
        return {"error": str(e)}

    encoded_address = urllib.parse.quote(address)
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={encoded_address}&key={api_key}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "TravelConcierge/1.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            if data.get("status") == "OK" and data.get("results"):
                result = data["results"][0]
                geometry = result.get("geometry", {}).get("location", {})
                return {
                    "formatted_address": result.get("formatted_address"),
                    "latitude": geometry.get("lat"),
                    "longitude": geometry.get("lng"),
                    "place_id": result.get("place_id"),
                }
            return {"error": f"Geocoding failed with status: {data.get('status')}"}
    except Exception as e:
        return {"error": f"Failed to perform geocoding request: {e}"}


def search_nearby_places(
    latitude: float,
    longitude: float,
    place_type: str = "tourist_attraction",
    radius_meters: float = 1000.0,
) -> list[dict]:
    """Finds nearby places of a given type around a latitude and longitude coordinate using Places API (New).

    Args:
        latitude: Latitude of the center location.
        longitude: Longitude of the center location.
        place_type: Type of place to search for (e.g. 'restaurant', 'tourist_attraction', 'museum', 'cafe', 'park').
        radius_meters: Radius in meters around the center to search (default: 1000.0).

    Returns:
        A list of dictionaries containing name, address, and location for each nearby place.
    """
    try:
        api_key = _get_api_key()
    except ValueError as e:
        return [{"error": str(e)}]

    url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location",
    }
    payload = {
        "includedTypes": [place_type.strip().lower()],
        "maxResultCount": 10,
        "locationRestriction": {
            "circle": {
                "center": {"latitude": latitude, "longitude": longitude},
                "radius": float(radius_meters),
            }
        },
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            places = data.get("places", [])
            results = []
            for place in places:
                display_name = place.get("displayName", {}).get("text", "")
                results.append({
                    "name": display_name,
                    "address": place.get("formattedAddress"),
                    "location": place.get("location"),
                })
            return results
    except Exception as e:
        return [{"error": f"Failed to search nearby places: {e}"}]
