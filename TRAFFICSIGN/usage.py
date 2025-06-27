#!/usr/bin/env python3
"""
GTSRB CORE Module - Usage Guide
==============================

This script shows all available commands and usage examples.
"""

import os
import sys

def show_usage():
    """Display usage information and examples"""
    
    print("🚀 GTSRB Traffic Sign Detection - CORE Module")
    print("=" * 60)
    print()
    
    # Check if we're in the right directory
    if not os.path.exists("models/gtsrb_model.lite"):
        print("❌ Please run this script from the CORE directory")
        print("   cd CORE && python usage.py")
        return
    
    print("📁 CORE Module Structure:")
    print("   CORE/")
    print("   ├── traffic_sign_detector.py  # Main detection class")
    print("   ├── single_detect.py         # Single image detection")
    print("   ├── batch_detect.py          # Batch processing")
    print("   ├── demo.py                  # Interactive demo")
    print("   ├── test_core.py             # Test script")
    print("   ├── models/gtsrb_model.lite  # TensorFlow Lite model")
    print("   ├── test_images/             # Sample images")
    print("   └── output/                  # JSON results")
    print()
    
    print("🔧 Installation:")
    print("   pip install -r requirements.txt")
    print()
    
    print("📋 Available Commands:")
    print()
    
    print("1️⃣  Test the module:")
    print("   python test_core.py")
    print()
    
    print("2️⃣  Run interactive demo:")
    print("   python demo.py")
    print()
    
    print("3️⃣  Detect single image:")
    print("   python single_detect.py test_images/00000.png")
    print("   python single_detect.py image.jpg -o result.json")
    print("   python single_detect.py image.jpg -c 0.5  # confidence threshold")
    print()
    
    print("4️⃣  Batch process directory:")
    print("   python batch_detect.py test_images/")
    print("   python batch_detect.py my_images/ -o my_results.json")
    print("   python batch_detect.py images/ -c 0.4 -o high_conf.json")
    print()
    
    print("5️⃣  Use in Python code:")
    print("   from traffic_sign_detector import TrafficSignDetector")
    print("   detector = TrafficSignDetector()")
    print("   result = detector.detect_sign('image.jpg')")
    print("   print(result)")
    print()
    
    print("📊 JSON Output Format:")
    print("   {")
    print('     "image_path": "test_images/00000.png",')
    print('     "detected": true,')
    print('     "primary_detection": {')
    print('       "class_id": 14,')
    print('       "label": "Stop",')
    print('       "confidence": 0.9876')
    print('     },')
    print('     "top_predictions": [...],')
    print('     "inference_time_ms": 42.5,')
    print('     "model_info": {...}')
    print("   }")
    print()
    
    print("🎯 Command Line Options:")
    print("   -o, --output FILE     Save results to JSON file")
    print("   -c, --confidence NUM  Confidence threshold (default: 0.3)")
    print("   -m, --model FILE      Custom model path")
    print("   -h, --help            Show help message")
    print()
    
    print("🏷️  Supported Traffic Signs (43 classes):")
    print("   • Speed limits: 20, 30, 50, 60, 70, 80, 100, 120 km/h")
    print("   • Warning signs: curves, construction, pedestrians, etc.")
    print("   • Mandatory signs: turn directions, keep right/left")
    print("   • Prohibition signs: no overtaking, no entry, etc.")
    print("   • Priority signs: right-of-way, yield, stop")
    print()
    
    print("🚀 Quick Start:")
    print("   1. cd CORE")
    print("   2. pip install -r requirements.txt")
    print("   3. python demo.py")
    print("   4. python single_detect.py test_images/00000.png")
    print()
    
    print("📝 Examples:")
    print("   # Basic detection")
    print("   python single_detect.py test_images/00000.png")
    print()
    print("   # Save to JSON")
    print("   python single_detect.py image.jpg -o result.json")
    print()
    print("   # Batch process with high confidence")
    print("   python batch_detect.py images/ -c 0.7 -o high_conf.json")
    print()
    print("   # Custom model")
    print("   python single_detect.py image.jpg -m /path/to/model.lite")
    print()
    
    print("✅ Ready to detect traffic signs!")

def main():
    """Main function"""
    try:
        show_usage()
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
