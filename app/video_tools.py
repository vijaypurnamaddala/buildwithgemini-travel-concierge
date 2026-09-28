import base64
import uuid
from google import genai
from google.genai import types
from google.cloud import storage
from google.adk.tools import ToolContext

# IMPORTANT: Hardcode project ID and bucket name as strings
PROJECT_ID = "qwiklabs-gcp-03-4a5379d43351"
BUCKET_NAME = "travel-concierge-media-qwiklabs-gcp-03-4a5379d43351"


async def generate_destination_video(
    prompt: str,
    destination_name: str = "destination",
    tool_context: ToolContext = None,
) -> dict:
    """Generates a short video for a travel destination or item in the travel domain using gemini-omni-flash-preview.

    Args:
        prompt: Detailed description of the video to generate (e.g. 'A short video of a serene waterfall in Kyoto').
        destination_name: Name of the destination, venue, or item (e.g. 'Kyoto Waterfall').

    Returns:
        A dictionary containing destination_name, public_url, and artifact_name.
    """
    # 1. Initialize GenAI client with Vertex AI in global region
    client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")

    # 2. Call gemini-omni-flash-preview model via interactions API
    interaction = client.interactions.create(
        model="gemini-omni-flash-preview",
        input=prompt,
    )

    video_bytes = None
    mime_type = "video/mp4"

    if hasattr(interaction, "output_video") and interaction.output_video:
        data = interaction.output_video.data
        if isinstance(data, str):
            video_bytes = base64.b64decode(data)
        elif isinstance(data, bytes):
            video_bytes = data

    if not video_bytes:
        return {"error": "Failed to generate video from prompt."}

    # Generate unique filename for artifact and GCS object
    clean_name = "".join(c for c in destination_name.lower().replace(" ", "-") if c.isalnum() or c == "-") or "video"
    filename = f"{clean_name}-{uuid.uuid4().hex[:8]}.mp4"

    # (1) Save artifact to ToolContext for Playground Artifacts panel
    if tool_context is not None:
        artifact_part = types.Part(
            inline_data=types.Blob(data=video_bytes, mime_type=mime_type)
        )
        await tool_context.save_artifact(filename, artifact_part)

    # (2) Upload video bytes directly to public Cloud Storage bucket
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_string(video_bytes, content_type=mime_type)

    public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"

    return {
        "destination_name": destination_name,
        "public_url": public_url,
        "artifact_name": filename,
    }
