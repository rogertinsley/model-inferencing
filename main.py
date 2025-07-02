from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from PIL import Image
import io
import time
import psutil
import os
from transformers import pipeline
import torch

app = FastAPI(title="Image Classifier Learning App", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Global variables to store models
models = {}
model_info = {
    "mobilenet": {
        "name": "MobileNet v2",
        "model_id": "google/mobilenet_v2_1.0_224",
        "size": "14 MB",
        "parameters": "3.4M",
        "accuracy": "71.8%",
        "description": "Lightweight model optimized for mobile devices",
        "best_for": "Real-time applications, mobile deployment"
    },
    "resnet": {
        "name": "ResNet-50",
        "model_id": "microsoft/resnet-50",
        "size": "98 MB",
        "parameters": "25.6M",
        "accuracy": "76.0%",
        "description": "Deep residual network for high accuracy",
        "best_for": "High accuracy requirements, cloud deployment"
    }
}

@app.on_event("startup")
async def load_models():
    global models
    print("Loading image classification models...")
    
    # Load MobileNet first (faster)
    print("Loading MobileNet v2...")
    models["mobilenet"] = pipeline("image-classification", model=model_info["mobilenet"]["model_id"])
    print("MobileNet v2 loaded successfully!")
    
    # Load ResNet (slower, larger)
    print("Loading ResNet-50...")
    models["resnet"] = pipeline("image-classification", model=model_info["resnet"]["model_id"])
    print("ResNet-50 loaded successfully!")
    
    print("All models loaded successfully!")

def get_memory_usage():
    """Get current memory usage in MB"""
    process = psutil.Process(os.getpid())
    return round(process.memory_info().rss / 1024 / 1024, 1)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Model Comparison Learning App</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
            .container { text-align: center; }
            .header { background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            .model-selector { background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            .model-card { display: inline-block; margin: 10px; padding: 15px; border: 2px solid #ddd; border-radius: 8px; background: #f9f9f9; min-width: 250px; vertical-align: top; }
            .model-card.selected { border-color: #4CAF50; background: #e8f5e8; }
            .model-card h3 { margin-top: 0; color: #333; }
            .model-stats { font-size: 0.9em; color: #666; text-align: left; }
            .upload-area { background: white; border: 2px dashed #ccc; padding: 20px; margin: 20px 0; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            .action-buttons { margin: 20px 0; }
            .btn { padding: 12px 24px; margin: 5px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; font-weight: bold; }
            .btn-primary { background: #4CAF50; color: white; }
            .btn-secondary { background: #2196F3; color: white; }
            .btn:hover { opacity: 0.9; }
            .btn:disabled { opacity: 0.5; cursor: not-allowed; }
            .results { margin-top: 20px; }
            .result-section { background: white; margin: 20px 0; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            .comparison-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }
            .model-result { background: #f9f9f9; padding: 15px; border-radius: 8px; }
            .prediction { margin: 10px 0; padding: 10px; background: #e8f4f8; border-radius: 5px; border-left: 4px solid #2196F3; }
            .confidence-bar { background: #ddd; height: 20px; border-radius: 10px; margin: 5px 0; overflow: hidden; }
            .confidence-fill { background: linear-gradient(90deg, #4CAF50, #8BC34A); height: 100%; border-radius: 10px; }
            .metrics { display: flex; justify-content: space-around; margin: 15px 0; }
            .metric { text-align: center; }
            .metric-value { font-size: 1.2em; font-weight: bold; color: #4CAF50; }
            .metric-label { font-size: 0.9em; color: #666; }
            img { max-width: 300px; max-height: 300px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            .tooltip { position: relative; display: inline-block; cursor: help; }
            .tooltip .tooltiptext { visibility: hidden; width: 300px; background-color: #333; color: #fff; text-align: center; border-radius: 6px; padding: 10px; position: absolute; z-index: 1; bottom: 125%; left: 50%; margin-left: -150px; opacity: 0; transition: opacity 0.3s; font-size: 0.9em; }
            .tooltip:hover .tooltiptext { visibility: visible; opacity: 1; }
            .comparison-summary { background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 15px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 AI Model Comparison Learning App</h1>
                <p>Compare MobileNet vs ResNet architectures and understand the speed vs accuracy trade-offs!</p>
            </div>
            
            <div class="model-selector">
                <h2>🎯 Choose Your Learning Mode</h2>
                <div class="model-card tooltip" data-model="mobilenet">
                    <h3>📱 MobileNet v2</h3>
                    <div class="model-stats">
                        <div><strong>Size:</strong> 14 MB</div>
                        <div><strong>Parameters:</strong> 3.4M</div>
                        <div><strong>Accuracy:</strong> 71.8%</div>
                        <div><strong>Best for:</strong> Real-time apps</div>
                    </div>
                    <span class="tooltiptext">MobileNet v2 uses depthwise separable convolutions to achieve high efficiency with low computational cost. Perfect for mobile devices and real-time applications.</span>
                </div>
                
                <div class="model-card tooltip" data-model="resnet">
                    <h3>🏗️ ResNet-50</h3>
                    <div class="model-stats">
                        <div><strong>Size:</strong> 98 MB</div>
                        <div><strong>Parameters:</strong> 25.6M</div>
                        <div><strong>Accuracy:</strong> 76.0%</div>
                        <div><strong>Best for:</strong> High accuracy</div>
                    </div>
                    <span class="tooltiptext">ResNet-50 uses residual connections to train very deep networks effectively. Higher accuracy but requires more computational resources.</span>
                </div>
                
                <div class="model-card tooltip" data-model="compare">
                    <h3>⚔️ Compare Both</h3>
                    <div class="model-stats">
                        <div><strong>Mode:</strong> Side-by-side</div>
                        <div><strong>Shows:</strong> Speed vs Accuracy</div>
                        <div><strong>Learn:</strong> Trade-offs</div>
                        <div><strong>Best for:</strong> Understanding</div>
                    </div>
                    <span class="tooltiptext">Run the same image through both models to see the differences in predictions, timing, and resource usage. Perfect for learning!</span>
                </div>
            </div>
            
            <form id="uploadForm" enctype="multipart/form-data">
                <div class="upload-area">
                    <h3>📸 Upload an Image</h3>
                    <input type="file" id="imageFile" name="file" accept="image/*" required>
                    <div class="action-buttons">
                        <button type="button" class="btn btn-primary" id="classifyBtn" disabled>🔍 Classify with Selected Model</button>
                        <button type="button" class="btn btn-secondary" id="compareBtn" disabled>⚔️ Compare Both Models</button>
                    </div>
                </div>
            </form>
            
            <div id="results" class="results"></div>
        </div>

        <script>
            let selectedModel = null;
            let currentFile = null;
            
            // Model selection
            document.querySelectorAll('.model-card').forEach(card => {
                card.addEventListener('click', () => {
                    document.querySelectorAll('.model-card').forEach(c => c.classList.remove('selected'));
                    card.classList.add('selected');
                    selectedModel = card.dataset.model;
                    updateButtons();
                });
            });
            
            // File selection
            document.getElementById('imageFile').addEventListener('change', (e) => {
                currentFile = e.target.files[0];
                updateButtons();
            });
            
            function updateButtons() {
                const classifyBtn = document.getElementById('classifyBtn');
                const compareBtn = document.getElementById('compareBtn');
                
                classifyBtn.disabled = !currentFile || !selectedModel || selectedModel === 'compare';
                compareBtn.disabled = !currentFile;
            }
            
            // Classify with single model
            document.getElementById('classifyBtn').addEventListener('click', async () => {
                if (!currentFile || !selectedModel) return;
                
                const formData = new FormData();
                formData.append('file', currentFile);
                formData.append('model_type', selectedModel);
                
                document.getElementById('results').innerHTML = '<div class="result-section"><p>🤔 Analyzing image with ' + (selectedModel === 'mobilenet' ? 'MobileNet v2' : 'ResNet-50') + '...</p></div>';
                
                try {
                    const response = await fetch('/predict', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        displaySingleResult(result);
                    } else {
                        throw new Error(result.detail || 'Prediction failed');
                    }
                } catch (error) {
                    document.getElementById('results').innerHTML = `<div class="result-section"><p style="color: red;">Error: ${error.message}</p></div>`;
                }
            });
            
            // Compare both models
            document.getElementById('compareBtn').addEventListener('click', async () => {
                if (!currentFile) return;
                
                const formData = new FormData();
                formData.append('file', currentFile);
                
                document.getElementById('results').innerHTML = '<div class="result-section"><p>⚔️ Running comparison between MobileNet v2 and ResNet-50...</p></div>';
                
                try {
                    const response = await fetch('/compare', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        displayComparison(result);
                    } else {
                        throw new Error(result.detail || 'Comparison failed');
                    }
                } catch (error) {
                    document.getElementById('results').innerHTML = `<div class="result-section"><p style="color: red;">Error: ${error.message}</p></div>`;
                }
            });
            
            function displaySingleResult(result) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    let html = `
                        <div class="result-section">
                            <h3>📸 Uploaded Image</h3>
                            <img src="${e.target.result}" alt="Uploaded image">
                        </div>
                        
                        <div class="result-section">
                            <h3>🎯 ${result.model_info.name} Results</h3>
                            <div class="metrics">
                                <div class="metric">
                                    <div class="metric-value">${result.processing_time}ms</div>
                                    <div class="metric-label">Processing Time</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-value">${result.memory_usage.used}MB</div>
                                    <div class="metric-label">Memory Used</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-value">${result.model_info.accuracy}</div>
                                    <div class="metric-label">Model Accuracy</div>
                                </div>
                            </div>
                            
                            <h4>Top 3 Predictions:</h4>
                    `;
                    
                    result.predictions.slice(0, 3).forEach((pred, index) => {
                        const confidence = (pred.score * 100).toFixed(1);
                        html += `
                            <div class="prediction">
                                <strong>#${index + 1}: ${pred.label}</strong>
                                <div class="confidence-bar">
                                    <div class="confidence-fill" style="width: ${confidence}%"></div>
                                </div>
                                <small>${confidence}% confidence</small>
                            </div>
                        `;
                    });
                    
                    html += `</div>`;
                    document.getElementById('results').innerHTML = html;
                };
                reader.readAsDataURL(currentFile);
            }
            
            function displayComparison(result) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    let html = `
                        <div class="result-section">
                            <h3>📸 Uploaded Image</h3>
                            <img src="${e.target.result}" alt="Uploaded image">
                        </div>
                        
                        <div class="comparison-summary">
                            <h3>📊 Comparison Summary</h3>
                            <p><strong>Speed:</strong> ResNet-50 took ${result.comparison.speed_ratio}x longer than MobileNet v2</p>
                            <p><strong>Accuracy:</strong> ResNet-50 has ${result.comparison.accuracy_difference} higher ImageNet accuracy</p>
                        </div>
                        
                        <div class="comparison-grid">
                            <div class="model-result">
                                <h3>📱 MobileNet v2</h3>
                                <div class="metrics">
                                    <div class="metric">
                                        <div class="metric-value">${result.results.mobilenet.processing_time}ms</div>
                                        <div class="metric-label">Processing Time</div>
                                    </div>
                                    <div class="metric">
                                        <div class="metric-value">${result.results.mobilenet.memory_usage.used}MB</div>
                                        <div class="metric-label">Memory Used</div>
                                    </div>
                                </div>
                                <h4>Top 3 Predictions:</h4>
                    `;
                    
                    result.results.mobilenet.predictions.slice(0, 3).forEach((pred, index) => {
                        const confidence = (pred.score * 100).toFixed(1);
                        html += `
                            <div class="prediction">
                                <strong>#${index + 1}: ${pred.label}</strong>
                                <div class="confidence-bar">
                                    <div class="confidence-fill" style="width: ${confidence}%"></div>
                                </div>
                                <small>${confidence}% confidence</small>
                            </div>
                        `;
                    });
                    
                    html += `
                            </div>
                            <div class="model-result">
                                <h3>🏗️ ResNet-50</h3>
                                <div class="metrics">
                                    <div class="metric">
                                        <div class="metric-value">${result.results.resnet.processing_time}ms</div>
                                        <div class="metric-label">Processing Time</div>
                                    </div>
                                    <div class="metric">
                                        <div class="metric-value">${result.results.resnet.memory_usage.used}MB</div>
                                        <div class="metric-label">Memory Used</div>
                                    </div>
                                </div>
                                <h4>Top 3 Predictions:</h4>
                    `;
                    
                    result.results.resnet.predictions.slice(0, 3).forEach((pred, index) => {
                        const confidence = (pred.score * 100).toFixed(1);
                        html += `
                            <div class="prediction">
                                <strong>#${index + 1}: ${pred.label}</strong>
                                <div class="confidence-bar">
                                    <div class="confidence-fill" style="width: ${confidence}%"></div>
                                </div>
                                <small>${confidence}% confidence</small>
                            </div>
                        `;
                    });
                    
                    html += `</div></div>`;
                    document.getElementById('results').innerHTML = html;
                };
                reader.readAsDataURL(currentFile);
            }
        </script>
    </body>
    </html>
    """

@app.post("/predict")
async def predict_image(file: UploadFile = File(...), model_type: str = Form("mobilenet")):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    if model_type not in models:
        raise HTTPException(status_code=400, detail=f"Model {model_type} not available")
    
    try:
        # Read and process the image
        start_time = time.time()
        memory_before = get_memory_usage()
        
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary (handles PNG with transparency, etc.)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Run inference with selected model
        predictions = models[model_type](image)
        
        processing_time = int((time.time() - start_time) * 1000)
        memory_after = get_memory_usage()
        memory_used = memory_after - memory_before
        
        return {
            "predictions": predictions,
            "processing_time": processing_time,
            "memory_usage": {
                "before": memory_before,
                "after": memory_after,
                "used": memory_used
            },
            "image_size": image.size,
            "model_info": model_info[model_type],
            "model_type": model_type
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/compare")
async def compare_models(file: UploadFile = File(...)):
    """Compare predictions from both models"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and process the image once
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        results = {}
        
        # Test both models
        for model_name in ["mobilenet", "resnet"]:
            start_time = time.time()
            memory_before = get_memory_usage()
            
            predictions = models[model_name](image)
            
            processing_time = int((time.time() - start_time) * 1000)
            memory_after = get_memory_usage()
            
            results[model_name] = {
                "predictions": predictions,
                "processing_time": processing_time,
                "memory_usage": {
                    "before": memory_before,
                    "after": memory_after,
                    "used": memory_after - memory_before
                },
                "model_info": model_info[model_name]
            }
        
        return {
            "image_size": image.size,
            "results": results,
            "comparison": {
                "speed_ratio": round(results["resnet"]["processing_time"] / results["mobilenet"]["processing_time"], 1),
                "accuracy_difference": f"+{float(model_info['resnet']['accuracy'][:-1]) - float(model_info['mobilenet']['accuracy'][:-1]):.1f}%"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing models: {str(e)}")

@app.get("/models")
async def get_model_info():
    """Get information about available models"""
    return {
        "available_models": model_info,
        "current_memory": get_memory_usage()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)