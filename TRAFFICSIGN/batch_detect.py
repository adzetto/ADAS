#!/usr/bin/env python3
"""
Batch Traffic Sign Detection Script
==================================

Simple script to process multiple images and generate JSON results.
"""

import os
import sys
import argparse
from traffic_sign_detector import TrafficSignDetector

def process_images(input_dir, output_file, model_path=None, confidence=0.3):
    """
    Process all images in a directory and save results to JSON
    
    Args:
        input_dir: Directory containing images to process
        output_file: Output JSON file path
        model_path: Path to TensorFlow Lite model (optional)
        confidence: Confidence threshold (default: 0.3)
    """
    
    # Initialize detector
    if model_path:
        detector = TrafficSignDetector(model_path=model_path, confidence_threshold=confidence)
    else:
        detector = TrafficSignDetector(confidence_threshold=confidence)
    
    # Get all image files
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    image_paths = []
    
    if not os.path.exists(input_dir):
        print(f"❌ Error: Input directory does not exist: {input_dir}")
        return False
    
    for file in os.listdir(input_dir):
        if file.lower().endswith(image_extensions):
            image_paths.append(os.path.join(input_dir, file))
    
    if not image_paths:
        print(f"❌ Error: No image files found in {input_dir}")
        return False
    
    print(f"📸 Found {len(image_paths)} images to process")
    
    # Process images
    results = detector.detect_batch(image_paths)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Save results
    detector.save_results_to_json(results, output_file)
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Batch process traffic sign detection')
    parser.add_argument('input_dir', help='Directory containing images to process')
    parser.add_argument('-o', '--output', default='output/batch_results.json',
                       help='Output JSON file path (default: output/batch_results.json)')
    parser.add_argument('-m', '--model', help='Path to TensorFlow Lite model')
    parser.add_argument('-c', '--confidence', type=float, default=0.3,
                       help='Confidence threshold (default: 0.3)')
    
    args = parser.parse_args()
    
    print("🚀 GTSRB Traffic Sign Detection - Batch Processing")
    print(f"📁 Input directory: {args.input_dir}")
    print(f"📄 Output file: {args.output}")
    print(f"🎯 Confidence threshold: {args.confidence}")
    
    if args.model:
        print(f"🤖 Model: {args.model}")
    
    print("-" * 50)
    
    success = process_images(args.input_dir, args.output, args.model, args.confidence)
    
    if success:
        print(f"\n✅ Batch processing completed successfully!")
        print(f"📊 Results saved to: {args.output}")
    else:
        print(f"\n❌ Batch processing failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
