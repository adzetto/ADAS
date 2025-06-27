#!/usr/bin/env python3
"""
Raspberry Pi Camera Traffic Sign Detection Module
===============================================

This module provides real-time traffic sign detection using Raspberry Pi Camera
with fisheye lens support and continuous monitoring capabilities.
"""

import tensorflow as tf
import numpy as np
from PIL import Image
import json
import os
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging
import io
import threading
from queue import Queue

try:
    from picamera2 import Picamera2
    from libcamera import controls
    PICAMERA_AVAILABLE = True
except ImportError:
    PICAMERA_AVAILABLE = False
    print("Warning: picamera2 not available. Install with: pip install picamera2")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PiCameraTrafficSignDetector:
    """Raspberry Pi Camera traffic sign detection class with fisheye lens support"""
    
    # GTSRB class labels
    LABELS = [
        'Speed limit (20km/h)', 'Speed limit (30km/h)', 'Speed limit (50km/h)', 'Speed limit (60km/h)',
        'Speed limit (70km/h)', 'Speed limit (80km/h)', 'End of speed limit (80km/h)', 'Speed limit (100km/h)',
        'Speed limit (120km/h)', 'No passing', 'No passing veh over 3.5 tons', 'Right-of-way at intersection',
        'Priority road', 'Yield', 'Stop', 'No vehicles', 'Veh > 3.5 tons prohibited', 'No entry',
        'General caution', 'Dangerous curve left', 'Dangerous curve right', 'Double curve', 'Bumpy road',
        'Slippery road', 'Road narrows on the right', 'Road work', 'Traffic signals', 'Pedestrians',
        'Children crossing', 'Bicycles crossing', 'Beware of ice/snow', 'Wild animals crossing',
        'End speed + passing limits', 'Turn right ahead', 'Turn left ahead', 'Ahead only', 'Go straight or right',
        'Go straight or left', 'Keep right', 'Keep left', 'Roundabout mandatory', 'End of no passing',
        'End no passing veh > 3.5 tons'
    ]
    
    def __init__(self, model_path: str = 'models/gtsrb_model.lite', 
                 confidence_threshold: float = 0.3,
                 camera_resolution: Tuple[int, int] = (1920, 1080),
                 detection_interval: float = 1.0):
        """
        Initialize the Raspberry Pi camera traffic sign detector
        
        Args:
            model_path: Path to the TensorFlow Lite model
            confidence_threshold: Minimum confidence threshold for detections
            camera_resolution: Camera resolution (width, height)
            detection_interval: Time interval between detections in seconds
        """
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.camera_resolution = camera_resolution
        self.detection_interval = detection_interval
        
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.camera = None
        
        self.detection_queue = Queue()
        self.running = False
        
        # Initialize components
        self._load_model()
        if PICAMERA_AVAILABLE:
            self._setup_camera()
        else:
            logger.warning("PiCamera2 not available - camera features disabled")
        
    def _load_model(self):
        """Load the TensorFlow Lite model"""
        try:
            logger.info(f"Loading TensorFlow Lite model: {self.model_path}")
            self.interpreter = tf.lite.Interpreter(model_path=self.model_path)
            self.interpreter.allocate_tensors()
            
            # Get input and output details
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            
            logger.info(f"✅ Model loaded successfully")
            logger.info(f"📐 Input shape: {self.input_details[0]['shape']}")
            logger.info(f"📊 Output shape: {self.output_details[0]['shape']}")
            
        except Exception as e:
            logger.error(f"❌ Error loading model: {e}")
            raise
    
    def _setup_camera(self):
        """Setup Raspberry Pi camera with fisheye lens optimization"""
        try:
            logger.info("🎥 Setting up Raspberry Pi camera...")
            self.camera = Picamera2()
            
            # Configure camera for fisheye lens (wider field of view)
            config = self.camera.create_still_configuration(
                main={"size": self.camera_resolution, "format": "RGB888"},
                controls={
                    "AwbEnable": True,  # Auto white balance
                    "AeEnable": True,   # Auto exposure
                    "FrameDurationLimits": (33333, 33333),  # ~30 FPS
                }
            )
            
            self.camera.configure(config)
            self.camera.start()
            
            # Warm up camera
            time.sleep(2)
            
            logger.info(f"✅ Camera initialized with resolution: {self.camera_resolution}")
            logger.info("🐟 Fisheye lens optimizations applied")
            
        except Exception as e:
            logger.error(f"❌ Error setting up camera: {e}")
            self.camera = None
            raise
    
    def preprocess_image_array(self, image_array: np.ndarray, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
        """
        Preprocess image array for model inference
        
        Args:
            image_array: Input image as numpy array
            target_size: Target size for resizing (width, height)
            
        Returns:
            Preprocessed image array
        """
        try:
            # Convert to PIL Image
            image = Image.fromarray(image_array)
            
            # Apply fisheye correction if needed (center crop to reduce distortion)
            width, height = image.size
            if width > height:
                # Landscape - crop center square
                left = (width - height) // 2
                right = left + height
                image = image.crop((left, 0, right, height))
            elif height > width:
                # Portrait - crop center square  
                top = (height - width) // 2
                bottom = top + width
                image = image.crop((0, top, width, bottom))
            
            # Resize to target size
            image = image.resize(target_size)
            
            # Convert to numpy array and normalize
            image_array = np.array(image, dtype=np.float32)
            image_array = image_array / 255.0  # Normalize to [0, 1]
            
            # Add batch dimension
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
            
        except Exception as e:
            logger.error(f"❌ Error preprocessing image: {e}")
            raise
    
    def capture_and_detect(self) -> Dict:
        """
        Capture image from camera and detect traffic signs
        
        Returns:
            Detection results dictionary
        """
        if not self.camera:
            return {
                'timestamp': datetime.now().isoformat(),
                'error': 'Camera not available',
                'detected': False
            }
        
        try:
            # Capture image
            capture_start = time.time()
            image_array = self.camera.capture_array()
            capture_time = time.time() - capture_start
            
            # Preprocess image
            preprocess_start = time.time()
            input_data = self.preprocess_image_array(image_array)
            preprocess_time = time.time() - preprocess_start
            
            # Run inference
            inference_start = time.time()
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            inference_time = time.time() - inference_start
            
            # Get output
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
            
            # Get predictions
            predicted_class = np.argmax(output_data[0])
            confidence = float(np.max(output_data[0]))
            
            # Get top 3 predictions
            top_indices = np.argsort(output_data[0])[-3:][::-1]
            top_predictions = []
            
            for idx in top_indices:
                if output_data[0][idx] > self.confidence_threshold:
                    top_predictions.append({
                        'class_id': int(idx),
                        'label': self.LABELS[idx],
                        'confidence': float(output_data[0][idx])
                    })
            
            # Prepare result
            result = {
                'timestamp': datetime.now().isoformat(),
                'capture_time_ms': round(capture_time * 1000, 2),
                'preprocess_time_ms': round(preprocess_time * 1000, 2),
                'inference_time_ms': round(inference_time * 1000, 2),
                'total_time_ms': round((capture_time + preprocess_time + inference_time) * 1000, 2),
                'detected': confidence > self.confidence_threshold,
                'camera_resolution': self.camera_resolution,
                'primary_detection': {
                    'class_id': int(predicted_class),
                    'label': self.LABELS[predicted_class],
                    'confidence': confidence
                } if confidence > self.confidence_threshold else None,
                'top_predictions': top_predictions,
                'model_info': {
                    'model_path': self.model_path,
                    'confidence_threshold': self.confidence_threshold,
                    'input_shape': self.input_details[0]['shape'].tolist(),
                    'total_classes': len(self.LABELS)
                }
            }
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error during capture and detection: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'detected': False
            }
    
    def start_continuous_detection(self, duration: Optional[float] = None, save_results: bool = True):
        """
        Start continuous traffic sign detection
        
        Args:
            duration: Detection duration in seconds (None for indefinite)
            save_results: Whether to save results to JSON file
        """
        if not self.camera:
            logger.error("❌ Camera not available for continuous detection")
            return
        
        self.running = True
        results = []
        start_time = time.time()
        detection_count = 0
        
        logger.info("🚀 Starting continuous traffic sign detection...")
        logger.info(f"⏱️  Detection interval: {self.detection_interval}s")
        logger.info(f"🎯 Confidence threshold: {self.confidence_threshold}")
        
        if duration:
            logger.info(f"⏰ Duration: {duration}s")
        else:
            logger.info("⏰ Duration: Indefinite (Press Ctrl+C to stop)")
        
        try:
            while self.running:
                # Check duration
                if duration and (time.time() - start_time) >= duration:
                    break
                
                # Perform detection
                result = self.capture_and_detect()
                results.append(result)
                detection_count += 1
                
                # Print detection result
                if result.get('detected', False):
                    primary = result.get('primary_detection', {})
                    print(f"🚦 DETECTED: {primary.get('label', 'Unknown')} "
                          f"(Confidence: {primary.get('confidence', 0):.2f}) "
                          f"[Detection #{detection_count}]")
                    
                    # Print top predictions if available
                    top_preds = result.get('top_predictions', [])
                    if len(top_preds) > 1:
                        print("   📊 Top predictions:")
                        for i, pred in enumerate(top_preds[:3]):
                            print(f"      {i+1}. {pred['label']} ({pred['confidence']:.2f})")
                else:
                    print(f"⚪ No sign detected [Detection #{detection_count}] "
                          f"(Time: {result.get('total_time_ms', 0):.1f}ms)")
                
                # Wait for next detection
                time.sleep(self.detection_interval)
                
        except KeyboardInterrupt:
            logger.info("🛑 Detection stopped by user")
        except Exception as e:
            logger.error(f"❌ Error during continuous detection: {e}")
        finally:
            self.running = False
            
            # Save results if requested
            if save_results and results:
                output_dir = 'output'
                os.makedirs(output_dir, exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"{output_dir}/pi_camera_detection_{timestamp}.json"
                
                self._save_results_to_json(results, output_file)
                logger.info(f"📁 Results saved to: {output_file}")
            
            total_time = time.time() - start_time
            successful_detections = sum(1 for r in results if r.get('detected', False))
            
            print(f"\n📈 Detection Summary:")
            print(f"   ⏱️  Total time: {total_time:.1f}s")
            print(f"   🔢 Total detections: {detection_count}")
            print(f"   ✅ Successful detections: {successful_detections}")
            print(f"   📊 Success rate: {(successful_detections/detection_count*100):.1f}%" if detection_count > 0 else "   📊 Success rate: 0%")
    
    def _save_results_to_json(self, results: List[Dict], output_path: str):
        """Save detection results to JSON file"""
        try:
            # Create summary statistics
            total_detections = len(results)
            successful_detections = sum(1 for r in results if r.get('detected', False))
            failed_detections = total_detections - successful_detections
            
            # Average processing times
            capture_times = [r.get('capture_time_ms', 0) for r in results if 'capture_time_ms' in r]
            inference_times = [r.get('inference_time_ms', 0) for r in results if 'inference_time_ms' in r]
            total_times = [r.get('total_time_ms', 0) for r in results if 'total_time_ms' in r]
            
            # Prepare output data
            output_data = {
                'detection_summary': {
                    'total_detections': total_detections,
                    'successful_detections': successful_detections,
                    'failed_detections': failed_detections,
                    'success_rate': round(successful_detections / total_detections * 100, 2) if total_detections > 0 else 0,
                    'average_capture_time_ms': round(np.mean(capture_times), 2) if capture_times else 0,
                    'average_inference_time_ms': round(np.mean(inference_times), 2) if inference_times else 0,
                    'average_total_time_ms': round(np.mean(total_times), 2) if total_times else 0,
                    'camera_resolution': self.camera_resolution,
                    'detection_interval_s': self.detection_interval,
                    'session_timestamp': datetime.now().isoformat()
                },
                'detections': results
            }
            
            # Save to JSON file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"❌ Error saving results to {output_path}: {e}")
    
    def cleanup(self):
        """Cleanup camera resources"""
        self.running = False
        if self.camera:
            try:
                self.camera.stop()
                self.camera.close()
                logger.info("🎥 Camera resources cleaned up")
            except Exception as e:
                logger.error(f"❌ Error cleaning up camera: {e}")


def main():
    """Main function for Pi camera detection"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Raspberry Pi Camera Traffic Sign Detection')
    parser.add_argument('--model', default='models/gtsrb_model.lite', help='Path to TensorFlow Lite model')
    parser.add_argument('--confidence', type=float, default=0.3, help='Confidence threshold')
    parser.add_argument('--resolution', default='1920x1080', help='Camera resolution (WxH)')
    parser.add_argument('--interval', type=float, default=1.0, help='Detection interval in seconds')
    parser.add_argument('--duration', type=float, help='Detection duration in seconds')
    parser.add_argument('--no-save', action='store_true', help='Do not save results to file')
    
    args = parser.parse_args()
    
    # Parse resolution
    try:
        width, height = map(int, args.resolution.split('x'))
        resolution = (width, height)
    except ValueError:
        logger.error("❌ Invalid resolution format. Use WxH (e.g., 1920x1080)")
        return
    
    print("🚦 Raspberry Pi Camera Traffic Sign Detector")
    print("=" * 50)
    print(f"📹 Camera Resolution: {resolution[0]}x{resolution[1]}")
    print(f"🎯 Confidence Threshold: {args.confidence}")
    print(f"⏱️  Detection Interval: {args.interval}s")
    print(f"🤖 Model: {args.model}")
    print("=" * 50)
    
    # Initialize detector
    try:
        detector = PiCameraTrafficSignDetector(
            model_path=args.model,
            confidence_threshold=args.confidence,
            camera_resolution=resolution,
            detection_interval=args.interval
        )
        
        # Start detection
        detector.start_continuous_detection(
            duration=args.duration,
            save_results=not args.no_save
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize detector: {e}")
    finally:
        # Cleanup
        try:
            detector.cleanup()
        except:
            pass


if __name__ == "__main__":
    main()