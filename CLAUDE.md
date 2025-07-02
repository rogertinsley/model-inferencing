# Claude Code Project Memory

## Project Overview
This is an **AI Model Comparison Learning App** designed to teach model inferencing concepts through hands-on comparison of different CNN architectures. The app provides an interactive web interface where users can compare MobileNet v2 vs ResNet-50 performance, understand speed vs accuracy trade-offs, and learn when to choose different model architectures.

## Architecture
- **Backend**: FastAPI with Python
- **Frontend**: Enhanced HTML/CSS/JavaScript with interactive model selection
- **ML Models**: Dual model support (MobileNet v2 + ResNet-50) via Hugging Face Transformers
- **Image Processing**: PIL (Python Imaging Library)
- **Performance Monitoring**: psutil for memory tracking
- **Deployment**: Docker containerized with docker-compose

## Key Learning Concepts Demonstrated
1. **Model Architecture Comparison**: MobileNet v2 vs ResNet-50 design differences
2. **Speed vs Accuracy Trade-offs**: Real performance implications of architecture choices
3. **Resource Usage Analysis**: Memory consumption and computational requirements
4. **Model Selection Strategy**: When to prioritize efficiency vs accuracy
5. **Performance Monitoring**: Processing time and memory usage measurement
6. **Interactive Learning**: Side-by-side model comparison with visual feedback
7. **Error Handling**: Graceful handling of invalid uploads and model failures

## File Structure
```
model-inferencing/
├── main.py              # FastAPI application with dual model support + enhanced UI
├── requirements.txt     # Python dependencies (includes psutil)
├── Dockerfile          # Docker container configuration
├── docker-compose.yml  # Docker Compose setup for easy deployment
├── .dockerignore       # Docker build exclusions
├── static/             # Directory for static files (currently empty)
├── README.md           # Comprehensive user documentation with model comparison info
└── CLAUDE.md           # This file - project memory for Claude Code
```

## Key Code Locations
- **Model Loading**: `main.py:46-59` - Startup event that loads both MobileNet and ResNet
- **Model Information**: `main.py:24-42` - Model specifications and metadata
- **Memory Monitoring**: `main.py:60-62` - psutil integration for resource tracking
- **Single Model Prediction**: `main.py:375-405` - Enhanced `/predict` endpoint with model selection
- **Model Comparison**: `main.py:407-446` - `/compare` endpoint for side-by-side analysis
- **Enhanced Frontend**: `main.py:64-374` - Interactive UI with model selection and comparison
- **Model Info API**: `main.py:448-452` - `/models` endpoint for model metadata

## Dependencies
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `transformers` - Hugging Face model library
- `torch` + `torchvision` - PyTorch backend
- `pillow` - Image processing
- `python-multipart` - File upload handling
- `psutil` - System performance monitoring

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
- Manual Docker build: `docker build -t ai-model-comparison . && docker run -p 8000:8000 ai-model-comparison`

### Local Testing
- Basic import test: `python -c "from main import app; print('✅ Enhanced app imports successfully!')"`
- Full server test: `python main.py` (then test model selection and comparison via browser)
- API endpoints test: Test `/predict`, `/compare`, and `/models` endpoints

## Educational Value
This project teaches:
- **Beginner Level**: Model architecture differences, speed vs accuracy concepts
- **Intermediate Level**: Performance profiling, resource usage analysis, model selection
- **Advanced Level**: Architecture trade-offs, optimization strategies, comparative analysis
- **Practical Skills**: When to choose MobileNet vs ResNet in real applications

## Future Enhancements (Optional)
- [x] Compare multiple models (MobileNet vs ResNet) - **COMPLETED**
- [ ] Add more architectures (EfficientNet, Vision Transformer)
- [ ] Batch processing for multiple images
- [ ] GPU acceleration support
- [ ] Custom model training pipeline
- [ ] Advanced metrics (FLOPs, detailed timing breakdown)
- [ ] Export comparison reports

## Notes for Claude Code
- The app loads both MobileNet v2 (14MB) and ResNet-50 (98MB) on startup
- Enhanced frontend with interactive model selection and comparison modes
- Real-time performance monitoring with memory usage tracking
- Educational tooltips explain architecture differences
- Side-by-side comparison mode shows speed vs accuracy trade-offs
- Model downloads automatically on first run (~112MB total)
- Graceful handling of model loading failures and memory constraints

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
- If model downloads fail: Check internet connection, Hugging Face may be rate-limiting
- If imports fail: Ensure all dependencies including psutil are installed
- If server won't start: Check port 8000 isn't already in use
- If memory usage is high: Normal with dual models loaded (~500MB+ RAM expected)
- If predictions are slow: MobileNet ~100-300ms, ResNet ~500-2000ms on CPU
- If comparison fails: Ensure sufficient memory for running both models