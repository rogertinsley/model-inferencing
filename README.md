# 🖼️ Image Classifier Learning App

A simple web application to learn model inferencing concepts using image classification.

## 🎯 What You'll Learn

- **Model Loading**: How to load pre-trained models using Hugging Face
- **Image Preprocessing**: Converting images to the right format for inference
- **Model Inference**: Running predictions on real data
- **Result Processing**: Interpreting model outputs and confidence scores
- **Performance Monitoring**: Tracking inference time and model performance

## 🚀 Quick Start

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
   - Upload an image and see the AI predictions!

## 🧠 How It Works

### The Model
- Uses **MobileNet v2** - a lightweight, efficient model perfect for learning
- Pre-trained on ImageNet dataset (1000+ categories)
- Runs inference on CPU (no GPU required)

### The Process
1. **Upload**: User uploads an image through the web interface
2. **Preprocess**: Image is converted to RGB and prepared for the model
3. **Inference**: MobileNet processes the image and returns predictions
4. **Display**: Top 3 predictions shown with confidence scores and timing

### Key Learning Points
- **main.py:23**: Model loading happens at startup for efficiency
- **main.py:67**: Image preprocessing handles different formats
- **main.py:72**: The actual inference call is just one line!
- **main.py:74**: Processing time measurement for performance analysis

## 🔍 Try These Experiments

1. **Different Images**: Try photos of animals, objects, food, vehicles
2. **Edge Cases**: What happens with abstract art? Blurry images?
3. **Confidence Analysis**: Notice how confidence varies with image clarity
4. **Performance**: Watch how processing time changes with image size

## 📚 Next Steps to Explore

- Modify the model to use ResNet instead of MobileNet
- Add batch processing for multiple images
- Implement custom image preprocessing
- Add GPU acceleration with CUDA
- Try different types of models (object detection, image captioning)

## 🛠️ Code Structure

```
model-inferencing/
├── main.py           # FastAPI backend + HTML frontend
├── requirements.txt  # Python dependencies
└── README.md        # This file
```

## 🤔 Understanding the Results

- **Labels**: The model was trained on ImageNet categories
- **Confidence**: Higher percentages mean the model is more certain
- **Top-3**: Shows the 3 most likely predictions
- **Processing Time**: How long inference took (usually 100-500ms on CPU)

Happy learning! 🎉