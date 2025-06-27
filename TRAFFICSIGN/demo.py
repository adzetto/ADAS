#!/usr/bin/env python3
"""
GTSRB CORE Module Demo
=====================

This script demonstrates the traffic sign detection capabilities.
"""

import os
import sys

def run_demo():
    """Run a complete demonstration of the CORE module"""
    
    print("🚀 GTSRB Traffic Sign Detection - CORE Module Demo")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("models/gtsrb_model.lite"):
        print("❌ Please run this script from the CORE directory")
        print("   cd CORE && python demo.py")
        return False
    
    print("✅ CORE module files detected")
    print("📁 Model: models/gtsrb_model.lite")
    print("📸 Test images: test_images/")
    print()
    
    # Demo 1: Single image detection
    print("🎯 DEMO 1: Single Image Detection")
    print("-" * 40)
    
    test_image = "test_images/00000.png"
    if os.path.exists(test_image):
        print(f"🔍 Analyzing: {test_image}")
        
        try:
            from traffic_sign_detector import TrafficSignDetector
            
            detector = TrafficSignDetector()
            result = detector.detect_sign(test_image)
            
            if result.get('detected', False):
                primary = result['primary_detection']
                print(f"✅ DETECTED: {primary['label']}")
                print(f"🎯 Confidence: {primary['confidence']:.4f}")
                print(f"⏱️  Time: {result['inference_time_ms']:.1f}ms")
            else:
                print("❌ No traffic sign detected")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    print()
    
    # Demo 2: Batch processing
    print("📚 DEMO 2: Batch Processing")
    print("-" * 40)
    
    try:
        # Get all test images
        image_files = [f for f in os.listdir("test_images") 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        print(f"📸 Processing {len(image_files)} images...")
        
        image_paths = [os.path.join("test_images", f) for f in image_files]
        results = detector.detect_batch(image_paths)
        
        # Count successful detections
        successful = sum(1 for r in results if r.get('detected', False))
        
        print(f"✅ Results: {successful}/{len(results)} images with detections")
        
        # Show detected signs
        for result in results:
            if result.get('detected', False):
                primary = result['primary_detection']
                filename = os.path.basename(result['image_path'])
                print(f"   📋 {filename}: {primary['label']} ({primary['confidence']:.3f})")
        
    except Exception as e:
        print(f"❌ Batch processing error: {e}")
        return False
    
    print()
    
    # Demo 3: JSON output
    print("💾 DEMO 3: JSON Output")
    print("-" * 40)
    
    try:
        os.makedirs("output", exist_ok=True)
        output_file = "output/demo_results.json"
        
        detector.save_results_to_json(results, output_file)
        
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"✅ JSON saved: {output_file} ({file_size} bytes)")
            print(f"📊 Contains results for {len(results)} images")
        else:
            print("❌ Failed to save JSON file")
            return False
            
    except Exception as e:
        print(f"❌ JSON output error: {e}")
        return False
    
    print()
    print("🎉 Demo completed successfully!")
    print()
    print("📋 Quick Commands:")
    print("   python single_detect.py test_images/00000.png")
    print("   python batch_detect.py test_images/")
    print("   python test_core.py")
    print()
    print("📁 Check the output/ directory for JSON results")
    
    return True

def main():
    """Main demo function"""
    try:
        success = run_demo()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
