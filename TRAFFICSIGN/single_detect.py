#!/usr/bin/env python3
"""
Single Image Traffic Sign Detection
===================================

Simple script to detect traffic signs in a single image.
"""

import argparse
import json
import os
from traffic_sign_detector import TrafficSignDetector

def detect_single_image(image_path, output_file=None, model_path=None, confidence=0.3):
    """
    Detect traffic sign in a single image
    
    Args:
        image_path: Path to the image file
        output_file: Output JSON file path (optional)
        model_path: Path to TensorFlow Lite model (optional)
        confidence: Confidence threshold (default: 0.3)
    """
    
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file does not exist: {image_path}")
        return False
    
    # Initialize detector
    if model_path:
        detector = TrafficSignDetector(model_path=model_path, confidence_threshold=confidence)
    else:
        detector = TrafficSignDetector(confidence_threshold=confidence)
    
    print(f"🔍 Analyzing image: {os.path.basename(image_path)}")
    
    # Run detection
    result = detector.detect_sign(image_path)
    
    # Print results
    print("\n" + "="*50)
    print("DETECTION RESULTS")
    print("="*50)
    
    if result.get('detected', False):
        primary = result['primary_detection']
        print(f"✅ DETECTED: {primary['label']}")
        print(f"🎯 Confidence: {primary['confidence']:.4f}")
        print(f"🏷️  Class ID: {primary['class_id']}")
        print(f"⏱️  Inference Time: {result['inference_time_ms']:.2f}ms")
        
        if len(result['top_predictions']) > 1:
            print(f"\n📋 Top Predictions:")
            for i, pred in enumerate(result['top_predictions'][:3], 1):
                print(f"  {i}. {pred['label']} ({pred['confidence']:.4f})")
    else:
        print("❌ NO TRAFFIC SIGN DETECTED")
        if 'error' in result:
            print(f"💥 Error: {result['error']}")
        else:
            print(f"🎯 Maximum confidence was below threshold ({confidence})")
    
    print("="*50)
    
    # Save to JSON if requested
    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"💾 Results saved to: {output_file}")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Detect traffic signs in a single image')
    parser.add_argument('image_path', help='Path to the image file')
    parser.add_argument('-o', '--output', help='Output JSON file path')
    parser.add_argument('-m', '--model', help='Path to TensorFlow Lite model')
    parser.add_argument('-c', '--confidence', type=float, default=0.3,
                       help='Confidence threshold (default: 0.3)')
    
    args = parser.parse_args()
    
    print("🚀 GTSRB Traffic Sign Detection - Single Image")
    print(f"📸 Image: {args.image_path}")
    print(f"🎯 Confidence threshold: {args.confidence}")
    
    if args.model:
        print(f"🤖 Model: {args.model}")
    
    if args.output:
        print(f"📄 Output: {args.output}")
    
    print("-" * 50)
    
    success = detect_single_image(args.image_path, args.output, args.model, args.confidence)
    
    if not success:
        print(f"\n❌ Detection failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
