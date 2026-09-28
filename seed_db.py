import os
from google.cloud import firestore

# IMPORTANT: Hardcode project ID to avoid project number resolution issues on Agent Platform
PROJECT_ID = "qwiklabs-gcp-03-4a5379d43351"

DESTINATIONS = [
    {
        "id": "sf-golden-gate-park",
        "name": "Golden Gate Park",
        "city": "San Francisco",
        "category": "Park & Nature",
        "description": "A massive urban park featuring gardens, lakes, museums, and scenic trails.",
        "rating": 4.8,
        "tags": ["outdoors", "scenic", "family-friendly"],
    },
    {
        "id": "sf-ferry-building",
        "name": "Ferry Building Marketplace",
        "city": "San Francisco",
        "category": "Dining & Shopping",
        "description": "Historic landmark along the waterfront featuring artisan food vendors and farmers markets.",
        "rating": 4.6,
        "tags": ["foodie", "waterfront", "shopping"],
    },
    {
        "id": "ny-central-park",
        "name": "Central Park",
        "city": "New York",
        "category": "Park & Nature",
        "description": "Iconic Manhattan park with walking paths, boat rentals, and historical monuments.",
        "rating": 4.9,
        "tags": ["outdoors", "iconic", "walking"],
    },
    {
        "id": "ny-high-line",
        "name": "The High Line",
        "city": "New York",
        "category": "Landmark",
        "description": "An elevated linear park and greenway built on a historic freight rail line.",
        "rating": 4.7,
        "tags": ["art", "scenic", "architecture"],
    },
    {
        "id": "tokyo-sensoji",
        "name": "Senso-ji Temple",
        "city": "Tokyo",
        "category": "Historical & Culture",
        "description": "Tokyo's oldest Buddhist temple located in Asakusa with vibrant market streets.",
        "rating": 4.8,
        "tags": ["culture", "historic", "temple"],
    },
    {
        "id": "paris-louvre",
        "name": "Louvre Museum",
        "city": "Paris",
        "category": "Museum",
        "description": "The world's largest art museum, home to the Mona Lisa and iconic glass pyramid.",
        "rating": 4.9,
        "tags": ["art", "museum", "historic"],
    },
]

def seed_firestore():
    print(f"Connecting to Firestore for project: {PROJECT_ID}")
    db = firestore.Client(project=PROJECT_ID)
    collection_ref = db.collection("destinations")

    for dest in DESTINATIONS:
        doc_id = dest["id"]
        collection_ref.document(doc_id).set(dest)
        print(f"Seeded destination: {dest['name']} ({dest['city']})")

    print(f"Successfully seeded {len(DESTINATIONS)} destinations into Firestore.")

if __name__ == "__main__":
    seed_firestore()
