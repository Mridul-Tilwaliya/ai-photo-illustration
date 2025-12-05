import os
import base64
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import replicate

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Photo Illustration API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
# Using a popular InstantID model on Replicate
# This model ID might need updating if a newer/better version is available
MODEL_VERSION = "zsxkib/instant-id:c98b2e7a196828d00955767813b81fc05c5c9b294c670c6d147d545fed4ceecf"

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Photo Illustration API"}

@app.post("/generate")
async def generate_illustration(
    file: UploadFile = File(...),
    prompt: str = Form("a child in a stylized illustration style"),
    negative_prompt: str = Form("(lowres, low quality, worst quality:1.2), (text:1.2), watermark, (frame:1.2), deformed, ugly, deformed eyes, blur, out of focus, blurring, textured skin, hairs, monochrome, grain, grainy, lo-fi, how old, realistic, shallow depth of field, glitch, corrupted, bad anatomy, extra legs, extra arms, extra fingers, poorly drawn hands, poorly drawn feet, disfigured, out of frame, tiling, bad art, deformed, mutated, blurry, fuzzy, misshaped, mutant, gross, disgusting, ugly"),
    style_strength: float = Form(0.8),
    identity_strength: float = Form(0.8),
):
    """
    Receives a user photo and uses Replicate to generate a personalized illustration
    based on a template.
    """
    if not REPLICATE_API_TOKEN:
        raise HTTPException(status_code=500, detail="REPLICATE_API_TOKEN is not set in the backend environment.")

    try:
        # Read the uploaded file
        file_content = await file.read()
        
        # In a real app, we would upload this to S3/Cloud storage and pass the URL.
        # Replicate also accepts base64 data URIs for smaller images.
        base64_image = base64.b64encode(file_content).decode("utf-8")
        data_uri = f"data:{file.content_type};base64,{base64_image}"

        # For the template/pose image, we should ideally have a stored asset.
        # For this prototype, we'll assume there's a default template or we allow uploading one.
        # For now, I'll use a placeholder or allow passing a template URL if needed.
        # Since the assignment implies a "provided template", I'll assume we have a fixed one.
        # TODO: Replace this with the actual path or URL of the template image provided by the user.
        # I'll create a utility to load it or use a public URL for testing.
        
        # Construct the input for the model
        # Note: The exact parameters depend on the specific InstantID model version on Replicate.
        output = replicate.run(
            MODEL_VERSION,
            input={
                "face_image": data_uri,
                # "pose_image": ... (If we want to match the pose of a template)
                # "style_image": ... (If we want to match the style)
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "ip_adapter_scale": style_strength, # Often maps to style strength
                "controlnet_conditioning_scale": 0.8,
                "identity_net_strength_ratio": identity_strength,
                "num_inference_steps": 30,
                "guidance_scale": 5,
            }
        )
        
        # The output is usually a list of URLs
        return {"output_urls": output}

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

