# 🤖 AI Model Comparison Learning App

A comprehensive web application designed to teach AI model inferencing concepts through hands-on comparison of MobileNet vs ResNet architectures.

## 🎯 What You'll Learn

### Core Concepts
- **Model Architecture Differences**: Understanding MobileNet vs ResNet design philosophies
- **Speed vs Accuracy Trade-offs**: Real-world performance implications
- **Resource Usage**: Memory consumption and computational requirements
- **Model Selection**: When to choose efficiency vs accuracy

### Technical Skills
- **Model Loading**: Loading multiple pre-trained models simultaneously
- **Image Preprocessing**: Preparing images for different model architectures
- **Performance Monitoring**: Measuring inference time and memory usage
- **Comparative Analysis**: Side-by-side model evaluation

## 🚀 Quick Start

### Option 1: Using Docker (Recommended)

1. **Build and Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Open Your Browser**
   - Go to `http://localhost:8000`
   - Experience the interactive model comparison interface!

### Option 2: Local Python Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python main.py
   ```

3. **Open Your Browser**
   - Go to `http://localhost:8000`
   - Start comparing AI models!

## 🧠 How It Works

### The Models

#### 📱 MobileNet v2
- **Size**: 14 MB
- **Parameters**: 3.4 million
- **Accuracy**: 71.8% ImageNet top-1
- **Strength**: Ultra-fast inference (100-300ms)
- **Best for**: Mobile apps, real-time processing, edge devices

#### 🏗️ ResNet-50
- **Size**: 98 MB  
- **Parameters**: 25.6 million
- **Accuracy**: 76.0% ImageNet top-1
- **Strength**: High accuracy, rich feature extraction
- **Best for**: Cloud applications, accuracy-critical tasks

### The Learning Experience

1. **Model Selection**: Choose individual models or side-by-side comparison
2. **Upload & Analyze**: Process images through selected architectures
3. **Compare Results**: See predictions, timing, and resource usage
4. **Understand Trade-offs**: Learn when to prioritize speed vs accuracy

## 🔍 Learning Experiments

### Beginner Level
1. **Single Model Testing**: Start with MobileNet, then try ResNet
2. **Speed Comparison**: Notice the inference time differences
3. **Accuracy Analysis**: Compare prediction confidence scores

### Intermediate Level
1. **Side-by-Side Comparison**: Use the compare mode for same image
2. **Edge Cases**: Test with blurry, abstract, or unusual images
3. **Resource Monitoring**: Observe memory usage patterns

### Advanced Level
1. **Performance Profiling**: Analyze speed vs accuracy ratios
2. **Architecture Understanding**: Relate results to model design choices
3. **Use Case Mapping**: Determine model selection for different scenarios

## 🎮 Interactive Features

### Model Selection Interface
- **Visual Model Cards**: Click to select MobileNet, ResNet, or comparison mode
- **Hover Tooltips**: Learn about each architecture's design principles
- **Performance Stats**: See model specifications at a glance

### Results Dashboard
- **Single Model Mode**: Detailed analysis of chosen architecture
- **Comparison Mode**: Side-by-side results with performance metrics
- **Real-time Metrics**: Processing time, memory usage, accuracy indicators

### Educational Elements
- **Architecture Explanations**: Built-in tooltips explain technical concepts
- **Performance Summaries**: Clear visualization of speed vs accuracy trade-offs
- **Visual Feedback**: Confidence bars and metric displays

## 🐳 Docker Commands

```bash
# Build and run with Docker Compose (easiest)
docker-compose up --build

# Or build and run manually
docker build -t ai-model-comparison .
docker run -p 8000:8000 ai-model-comparison

# Stop the application
docker-compose down
```

## 🛠️ Code Structure

```
model-inferencing/
├── main.py              # FastAPI backend with dual model support
├── requirements.txt     # Python dependencies (includes psutil)
├── Dockerfile          # Docker container configuration
├── docker-compose.yml  # Docker Compose setup
├── .dockerignore       # Docker build exclusions
├── static/             # Static files directory
├── CLAUDE.md           # Project memory for Claude Code
└── README.md           # This comprehensive guide
```

## 📊 API Endpoints

- **`GET /`**: Interactive web interface
- **`POST /predict`**: Single model inference with model selection
- **`POST /compare`**: Side-by-side model comparison
- **`GET /models`**: Model information and current memory usage

## 🤔 Understanding the Results

### Single Model Results
- **Processing Time**: Inference speed in milliseconds
- **Memory Usage**: RAM consumption during processing
- **Top-3 Predictions**: Most likely classifications with confidence
- **Model Info**: Architecture details and specifications

### Comparison Results
- **Speed Ratio**: How much faster/slower models perform
- **Accuracy Difference**: ImageNet accuracy comparison
- **Side-by-Side Predictions**: Different model interpretations
- **Resource Usage**: Memory and timing differences

## 🎓 Educational Outcomes

After using this app, you'll understand:

1. **Why MobileNet is perfect for mobile apps** (speed + efficiency)
2. **When ResNet's extra accuracy is worth the cost** (critical applications)
3. **How to make informed model selection decisions** (use case analysis)
4. **The fundamental trade-offs in AI model design** (speed vs accuracy vs size)

## 🔬 Technical Deep Dive

### MobileNet v2 Architecture
- **Depthwise Separable Convolutions**: Reduces computation by factorizing standard convolutions
- **Inverted Residuals**: Expand-project pattern with linear bottlenecks
- **Efficient Design**: Optimized for mobile and edge device constraints

### ResNet-50 Architecture  
- **Residual Connections**: Skip connections enable training of very deep networks
- **Batch Normalization**: Stabilizes training and improves convergence
- **Deep Feature Learning**: 50 layers capture complex hierarchical patterns

## 🚀 Next Steps

Ready to go deeper? Try these extensions:

- **Add More Models**: Integrate EfficientNet, Vision Transformer (ViT)
- **Batch Processing**: Upload multiple images for bulk comparison
- **Custom Models**: Load your own trained models
- **GPU Acceleration**: Enable CUDA for faster inference
- **Advanced Metrics**: Add FLOPs counting, detailed timing breakdown

Happy learning! 🎉

---

*This app demonstrates that learning AI concepts is most effective through hands-on experimentation and direct comparison.*