import uuid
from google import genai
from google.genai import types
from google.cloud import storage
from google.adk.tools import ToolContext

# IMPORTANT: Hardcode project ID and bucket name as strings
PROJECT_ID = "qwiklabs-gcp-03-4a5379d43351"
BUCKET_NAME = "travel-concierge-media-qwiklabs-gcp-03-4a5379d43351"


async def generate_destination_image(
    prompt: str,
    destination_name: str = "destination",
    tool_context: ToolContext = None,
) -> dict:
    """Generates a high-quality visual preview image for a travel destination or landmark.

    Args:
        prompt: Detailed description of the image to generate (e.g. 'A scenic sunset over Golden Gate Park in San Francisco').
        destination_name: Name of the destination or venue (e.g. 'Golden Gate Park').

    Returns:
        A dictionary containing the destination_name, public_url, and artifact_name.
    """
    # 1. Initialize GenAI client with Vertex AI in global region
    client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")

    # 2. Call gemini-3.1-flash-lite-image model
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-image",
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"]
        ),
    )

    image_bytes = None
    mime_type = "image/jpeg"

    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                image_bytes = part.inline_data.data
                mime_type = part.inline_data.mime_type or "image/jpeg"
                break

    if not image_bytes:
        return {"error": "Failed to generate image from prompt."}

    # Generate unique filename for artifact and GCS object
    clean_name = "".join(c for c in destination_name.lower().replace(" ", "-") if c.isalnum() or c == "-")
    ext = "png" if "png" in mime_type else "jpg"
    filename = f"{clean_name}-{uuid.uuid4().hex[:8]}.{ext}"

    # (1) Save artifact to ToolContext for Playground Artifacts panel
    if tool_context is not None:
        artifact_part = types.Part(
            inline_data=types.Blob(data=image_bytes, mime_type=mime_type)
        )
        await tool_context.save_artifact(filename, artifact_part)

    # (2) Upload image bytes to public Cloud Storage bucket
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_string(image_bytes, content_type=mime_type)

    public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"

    return {
        "destination_name": destination_name,
        "public_url": public_url,
        "artifact_name": filename,
    }
