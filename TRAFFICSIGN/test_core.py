#!/usr/bin/env python3
"""
Test script for GTSRB CORE module
"""

import os
import sys

def test_core_module():
    """Test the CORE module functionality"""
    
    print("🧪 Testing GTSRB CORE Module")
    print("=" * 40)
    
    # Check if model exists
    model_path = "models/gtsrb_model.lite"
    if os.path.exists(model_path):
        print(f"✅ Model found: {model_path}")
    else:
        print(f"❌ Model not found: {model_path}")
        return False
    
    # Check if test images exist
    test_images_dir = "test_images"
    if os.path.exists(test_images_dir):
        image_files = [f for f in os.listdir(test_images_dir) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        print(f"✅ Test images found: {len(image_files)} files")
        
        if image_files:
            test_image = os.path.join(test_images_dir, image_files[0])
            print(f"📸 Test image: {test_image}")
        else:
            print("❌ No image files found in test_images/")
            return False
    else:
        print(f"❌ Test images directory not found: {test_images_dir}")
        return False
    
    # Test imports
    try:
        print("\n🔍 Testing imports...")
        from traffic_sign_detector import TrafficSignDetector
        print("✅ TrafficSignDetector imported successfully")
        
        # Test detector initialization
        print("\n🤖 Testing detector initialization...")
        detector = TrafficSignDetector(model_path=model_path, confidence_threshold=0.3)
        print("✅ Detector initialized successfully")
        
        # Test single detection
        print(f"\n🎯 Testing detection on: {os.path.basename(test_image)}")
        result = detector.detect_sign(test_image)
        
        if result.get('detected', False):
            primary = result['primary_detection']
            print(f"✅ Detection successful!")
            print(f"   🏷️  Label: {primary['label']}")
            print(f"   🎯 Confidence: {primary['confidence']:.4f}")
            print(f"   ⏱️  Inference time: {result['inference_time_ms']:.2f}ms")
        else:
            print("⚠️  No traffic sign detected (this may be normal)")
        
        # Test JSON output
        print("\n💾 Testing JSON output...")
        os.makedirs("output", exist_ok=True)
        output_file = "output/test_results.json"
        detector.save_results_to_json([result], output_file)
        
        if os.path.exists(output_file):
            print(f"✅ JSON output created: {output_file}")
        else:
            print(f"❌ JSON output failed: {output_file}")
            return False
        
        print("\n🎉 All tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Please install required packages: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

def main():
    """Main test function"""
    success = test_core_module()
    
    if success:
        print("\n✅ CORE module is working correctly!")
        print("\n📋 Next steps:")
        print("   • Run: python single_detect.py test_images/00000.png")
        print("   • Run: python batch_detect.py test_images/")
        print("   • Check output/ directory for JSON results")
        return 0
    else:
        print("\n❌ CORE module test failed!")
        print("\n🔧 Troubleshooting:")
        print("   • Install dependencies: pip install -r requirements.txt")
        print("   • Ensure model file exists in models/")
        print("   • Check test images in test_images/")
        return 1

if __name__ == "__main__":
    sys.exit(main())
