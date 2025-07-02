# Claude Code Project Memory

## Project Overview
This is an **Image Classifier Learning App** designed to teach model inferencing concepts through hands-on practice. The app provides a simple web interface where users can upload images and see AI predictions in real-time.

## Architecture
- **Backend**: FastAPI with Python
- **Frontend**: Embedded HTML/CSS/JavaScript (single-page app)
- **ML Model**: MobileNet v2 via Hugging Face Transformers
- **Image Processing**: PIL (Python Imaging Library)
- **Deployment**: Docker containerized with docker-compose

## Key Learning Concepts Demonstrated
1. **Model Loading**: Pre-trained model initialization at startup
2. **Image Preprocessing**: Format conversion, RGB handling
3. **Model Inference**: Single-line prediction calls
4. **Result Processing**: Confidence scores, top-N predictions
5. **Performance Monitoring**: Processing time measurement
6. **Error Handling**: Graceful handling of invalid uploads

## File Structure
```
model-inferencing/
├── main.py              # Main FastAPI application with embedded frontend
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker container configuration
├── docker-compose.yml  # Docker Compose setup for easy deployment
├── .dockerignore       # Docker build exclusions
├── static/             # Directory for static files (currently empty)
├── README.md           # User documentation and setup instructions
└── CLAUDE.md           # This file - project memory for Claude Code
```

## Key Code Locations
- **Model Loading**: `main.py:23` - Startup event that loads MobileNet
- **Image Processing**: `main.py:67` - PIL image preprocessing pipeline
- **Inference Call**: `main.py:72` - The actual model prediction
- **Frontend**: `main.py:31-119` - Embedded HTML interface
- **API Endpoint**: `main.py:121` - `/predict` endpoint for image classification

## Dependencies
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `transformers` - Hugging Face model library
- `torch` + `torchvision` - PyTorch backend
- `pillow` - Image processing
- `python-multipart` - File upload handling

## How to Run

### Option 1: Using Docker (Recommended)
```bash
docker-compose up --build
```

### Option 2: Local Python Installation
```bash
pip install -r requirements.txt
python main.py
```

Then visit `http://localhost:8000`

## Testing Commands

### Docker Testing
- Build and test: `docker-compose up --build`
- Manual Docker build: `docker build -t image-classifier . && docker run -p 8000:8000 image-classifier`

### Local Testing
- Basic import test: `python -c "from main import app; print('✅ App imports successfully!')"`
- Full server test: `python main.py` (then test uploads via browser)

## Educational Value
This project teaches:
- **Beginner Level**: What is model inference? How do confidence scores work?
- **Intermediate Level**: Image preprocessing, API design, model loading patterns
- **Advanced Level**: Performance optimization, error handling, model comparison

## Future Enhancements (Optional)
- [ ] Compare multiple models (MobileNet vs ResNet)
- [ ] Batch processing for multiple images
- [ ] GPU acceleration support
- [ ] Custom model training pipeline
- [ ] Model performance benchmarking

## Notes for Claude Code
- The app uses MobileNet v2 for fast CPU inference
- All frontend code is embedded in main.py for simplicity
- Error handling covers common edge cases (non-images, corrupted files)
- Processing time is measured and displayed for educational purposes
- The model downloads automatically on first run (~14MB)

## Docker Benefits
- **Consistent Environment**: Same runtime across all systems
- **Easy Deployment**: Single command setup
- **Dependency Isolation**: No local Python environment conflicts
- **Model Caching**: Hugging Face models cached in Docker volume
- **Health Checks**: Built-in container health monitoring

## Troubleshooting

### Docker Issues
- If Docker build fails: Ensure Docker is running and has sufficient memory
- If container won't start: Check port 8000 isn't already in use
- If models won't download: Check internet connection and firewall settings

### General Issues
- If model download fails: Check internet connection, Hugging Face may be rate-limiting
- If imports fail: Ensure all dependencies are installed with correct versions
- If server won't start: Check port 8000 isn't already in use
- If predictions are slow: This is normal on CPU, ~100-500ms expected