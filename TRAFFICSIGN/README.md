# GTSRB Traffic Sign Detection - CORE Module

This is a streamlined core module for German Traffic Sign Recognition using TensorFlow Lite. It provides simple Python scripts for detecting traffic signs and outputting results to JSON format.

## 📁 Directory Structure

```
CORE/
├── traffic_sign_detector.py    # Main detection class
├── single_detect.py           # Single image detection script
├── batch_detect.py           # Batch processing script
├── requirements.txt          # Python dependencies
├── models/                   # Model files
│   └── gtsrb_model.lite     # TensorFlow Lite model
├── test_images/             # Sample test images
│   ├── 00000.png
│   ├── 00001.png
│   └── ...
└── output/                  # Detection results
    └── detection_results.json
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Single Image Detection
```bash
python single_detect.py test_images/00000.png
```

With JSON output:
```bash
python single_detect.py test_images/00000.png -o output/single_result.json
```

### 3. Batch Processing
```bash
python batch_detect.py test_images/
```

With custom output file:
```bash
python batch_detect.py test_images/ -o output/my_results.json
```

### 4. Using the Detection Class Directly
```python
from traffic_sign_detector import TrafficSignDetector

# Initialize detector
detector = TrafficSignDetector()

# Detect single image
result = detector.detect_sign('test_images/00000.png')
print(result)

# Batch detection
results = detector.detect_batch(['image1.jpg', 'image2.jpg'])

# Save to JSON
detector.save_results_to_json(results, 'output/results.json')
```

## 🎯 Features

- **Simple API**: Easy-to-use Python classes and functions
- **JSON Output**: Structured results with confidence scores and metadata
- **Batch Processing**: Process multiple images efficiently
- **Configurable**: Adjustable confidence thresholds
- **Detailed Results**: Top predictions, inference times, and model info
- **Error Handling**: Robust error handling and logging

## 📊 Output Format

The detection results are saved in JSON format with the following structure:

```json
{
  "detection_summary": {
    "total_images": 5,
    "successful_detections": 4,
    "failed_detections": 1,
    "success_rate": 80.0,
    "average_inference_time_ms": 45.32,
    "detection_timestamp": "2025-06-26T10:30:00"
  },
  "detections": [
    {
      "image_path": "test_images/00000.png",
      "timestamp": "2025-06-26T10:30:00",
      "inference_time_ms": 42.5,
      "detected": true,
      "primary_detection": {
        "class_id": 14,
        "label": "Stop",
        "confidence": 0.9876
      },
      "top_predictions": [
        {
          "class_id": 14,
          "label": "Stop", 
          "confidence": 0.9876
        },
        {
          "class_id": 13,
          "label": "Yield",
          "confidence": 0.0123
        }
      ],
      "model_info": {
        "model_path": "models/gtsrb_model.lite",
        "confidence_threshold": 0.3,
        "input_shape": [1, 224, 224, 3],
        "total_classes": 43
      }
    }
  ]
}
```

## 🏷️ Traffic Sign Classes

The model can detect 43 different German traffic sign classes:

- **Speed Limits**: 20, 30, 50, 60, 70, 80, 100, 120 km/h
- **Warning Signs**: Dangerous curves, road work, pedestrians, etc.
- **Mandatory Signs**: Turn directions, keep right/left, etc.
- **Prohibition Signs**: No overtaking, no entry, etc.
- **Priority Signs**: Right-of-way, yield, stop, etc.

## ⚙️ Configuration Options

### Command Line Arguments

**Single Image Detection:**
- `image_path`: Path to the image file (required)
- `-o, --output`: Output JSON file path
- `-m, --model`: Path to TensorFlow Lite model
- `-c, --confidence`: Confidence threshold (default: 0.3)

**Batch Processing:**
- `input_dir`: Directory containing images (required)
- `-o, --output`: Output JSON file path (default: output/batch_results.json)
- `-m, --model`: Path to TensorFlow Lite model
- `-c, --confidence`: Confidence threshold (default: 0.3)

### TrafficSignDetector Class

```python
detector = TrafficSignDetector(
    model_path='models/gtsrb_model.lite',  # Path to model
    confidence_threshold=0.3               # Confidence threshold
)
```

## 🔧 Requirements

- Python 3.7+
- TensorFlow 2.10+
- NumPy 1.21+
- Pillow 8.3+

## 📝 Usage Examples

### Example 1: Quick Detection
```bash
cd CORE
python single_detect.py test_images/00000.png
```

### Example 2: Batch with Custom Threshold
```bash
python batch_detect.py test_images/ -c 0.5 -o output/high_confidence.json
```

### Example 3: Custom Model
```bash
python single_detect.py image.jpg -m /path/to/custom_model.lite
```

## 🐛 Troubleshooting

**Model not found error:**
- Ensure `gtsrb_model.lite` is in the `models/` directory
- Check file permissions

**Import errors:**
- Install required packages: `pip install -r requirements.txt`
- Ensure TensorFlow is properly installed

**No detections:**
- Try lowering the confidence threshold with `-c 0.1`
- Check if the image contains traffic signs
- Verify image format (PNG, JPG, etc.)

## 📈 Performance

- **Inference Speed**: ~20-50ms per image (CPU)
- **Memory Usage**: ~100MB (model loaded)
- **Accuracy**: High accuracy on German traffic signs
- **Supported Formats**: PNG, JPG, JPEG, BMP, TIFF
