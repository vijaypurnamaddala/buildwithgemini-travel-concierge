from google.cloud import firestore

# IMPORTANT: Hardcode project ID to avoid project number resolution issues on Agent Platform
FIRESTORE_PROJECT_ID = "qwiklabs-gcp-03-4a5379d43351"

def _get_db():
    return firestore.Client(project=FIRESTORE_PROJECT_ID)

def search_destinations(query: str = "", city: str = "") -> list[dict]:
    """Searches for travel destinations and venues in the database.

    Args:
        query: Optional search keyword to filter destinations by name, category, description, or tags.
        city: Optional city name to filter destinations (e.g., 'San Francisco', 'New York', 'Tokyo', 'Paris').

    Returns:
        A list of matching destination dictionaries.
    """
    db = _get_db()
    docs = db.collection("destinations").stream()
    results = []

    q = query.lower().strip()
    c = city.lower().strip()

    for doc in docs:
        data = doc.to_dict()
        doc_city = data.get("city", "").lower()
        
        # Check city filter
        if c and c not in doc_city:
            continue

        # Check query filter across fields
        if q:
            name = data.get("name", "").lower()
            category = data.get("category", "").lower()
            desc = data.get("description", "").lower()
            tags = [t.lower() for t in data.get("tags", [])]

            if not (q in name or q in category or q in desc or any(q in t for t in tags)):
                continue

        results.append(data)

    return results

def add_destination(name: str, city: str, category: str, description: str, rating: float = 4.5, tags: str = "") -> dict:
    """Adds a new destination or venue to the travel catalog in Firestore.

    Args:
        name: Name of the venue or landmark (e.g. 'Eiffel Tower').
        city: City where the destination is located (e.g. 'Paris').
        category: Category such as 'Landmark', 'Museum', 'Park & Nature', 'Dining & Shopping'.
        description: Detailed description of the venue or attraction.
        rating: Rating out of 5.0 (default: 4.5).
        tags: Comma-separated list of tags (e.g. 'historic, view, iconic').

    Returns:
        A dictionary of the added destination object.
    """
    db = _get_db()
    
    # Generate clean document ID
    doc_id = f"{city.lower().replace(' ', '-')}-{name.lower().replace(' ', '-')}"
    doc_id = ''.join(e for e in doc_id if e.isalnum() or e == '-')

    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if isinstance(tags, str) else tags

    dest_data = {
        "id": doc_id,
        "name": name,
        "city": city,
        "category": category,
        "description": description,
        "rating": float(rating),
        "tags": tag_list or ["travel"],
    }

    db.collection("destinations").document(doc_id).set(dest_data)
    return dest_data

def get_destination_details(destination_id: str) -> dict:
    """Gets details for a specific destination by its document ID.

    Args:
        destination_id: Document ID of the destination (e.g., 'sf-golden-gate-park').

    Returns:
        Destination details dictionary or error dictionary if not found.
    """
    db = _get_db()
    doc = db.collection("destinations").document(destination_id).get()
    if doc.exists:
        return doc.to_dict()
    return {"error": f"Destination with ID '{destination_id}' not found."}
