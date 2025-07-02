from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from PIL import Image
import io
import time
from transformers import pipeline
import torch

app = FastAPI(title="Image Classifier Learning App", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Global variable to store the model (we'll initialize it on startup)
classifier = None

@app.on_event("startup")
async def load_model():
    global classifier
    print("Loading image classification model...")
    # Using a lightweight model for faster inference
    classifier = pipeline("image-classification", model="google/mobilenet_v2_1.0_224")
    print("Model loaded successfully!")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Image Classifier Learning App</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .container { text-align: center; }
            .upload-area { border: 2px dashed #ccc; padding: 20px; margin: 20px 0; }
            .results { margin-top: 20px; text-align: left; }
            .prediction { margin: 10px 0; padding: 10px; background: #f5f5f5; border-radius: 5px; }
            img { max-width: 300px; max-height: 300px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🖼️ Image Classifier Learning App</h1>
            <p>Upload an image to see what the AI model thinks it is!</p>
            
            <form id="uploadForm" enctype="multipart/form-data">
                <div class="upload-area">
                    <input type="file" id="imageFile" name="file" accept="image/*" required>
                    <br><br>
                    <button type="submit">Classify Image</button>
                </div>
            </form>
            
            <div id="results" class="results"></div>
        </div>

        <script>
            document.getElementById('uploadForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const fileInput = document.getElementById('imageFile');
                const file = fileInput.files[0];
                
                if (!file) {
                    alert('Please select an image file');
                    return;
                }
                
                const formData = new FormData();
                formData.append('file', file);
                
                document.getElementById('results').innerHTML = '<p>🤔 Analyzing image...</p>';
                
                try {
                    const response = await fetch('/predict', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        displayResults(result, file);
                    } else {
                        throw new Error(result.detail || 'Prediction failed');
                    }
                } catch (error) {
                    document.getElementById('results').innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
                }
            });
            
            function displayResults(result, file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    let html = `
                        <h3>📸 Uploaded Image:</h3>
                        <img src="${e.target.result}" alt="Uploaded image">
                        
                        <h3>🎯 Predictions (Top 3):</h3>
                    `;
                    
                    result.predictions.slice(0, 3).forEach((pred, index) => {
                        const confidence = (pred.score * 100).toFixed(1);
                        html += `
                            <div class="prediction">
                                <strong>#${index + 1}: ${pred.label}</strong>
                                <div style="background: #ddd; height: 20px; border-radius: 10px; margin-top: 5px;">
                                    <div style="background: #4CAF50; height: 100%; width: ${confidence}%; border-radius: 10px;"></div>
                                </div>
                                <small>${confidence}% confidence</small>
                            </div>
                        `;
                    });
                    
                    html += `<p><small>⏱️ Processing time: ${result.processing_time}ms</small></p>`;
                    
                    document.getElementById('results').innerHTML = html;
                };
                reader.readAsDataURL(file);
            }
        </script>
    </body>
    </html>
    """

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and process the image
        start_time = time.time()
        
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary (handles PNG with transparency, etc.)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Run inference
        predictions = classifier(image)
        
        processing_time = int((time.time() - start_time) * 1000)
        
        return {
            "predictions": predictions,
            "processing_time": processing_time,
            "image_size": image.size,
            "model_info": "MobileNet v2 (224x224)"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)