#!/usr/bin/env python3
"""
GTSRB Traffic Sign Detection Core Module
========================================

This module provides core functionality for detecting German traffic signs
and outputting results to JSON format.
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrafficSignDetector:
    """Core traffic sign detection class"""
    
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
    
    def __init__(self, model_path: str = 'models/gtsrb_model.lite', confidence_threshold: float = 0.3):
        """
        Initialize the traffic sign detector
        
        Args:
            model_path: Path to the TensorFlow Lite model
            confidence_threshold: Minimum confidence threshold for detections
        """
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        
        # Load model
        self._load_model()
        
    def _load_model(self):
        """Load the TensorFlow Lite model"""
        try:
            logger.info(f"Loading TensorFlow Lite model: {self.model_path}")
            self.interpreter = tf.lite.Interpreter(model_path=self.model_path)
            self.interpreter.allocate_tensors()
            
            # Get input and output details
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            
            logger.info(f"Model loaded successfully")
            logger.info(f"Input shape: {self.input_details[0]['shape']}")
            logger.info(f"Output shape: {self.output_details[0]['shape']}")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def preprocess_image(self, image_path: str, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
        """
        Preprocess image for model inference
        
        Args:
            image_path: Path to the image file
            target_size: Target size for resizing (width, height)
            
        Returns:
            Preprocessed image array
        """
        try:
            # Load and convert image
            image = Image.open(image_path).convert('RGB')
            image = image.resize(target_size)
            
            # Convert to numpy array and normalize
            image_array = np.array(image, dtype=np.float32)
            image_array = image_array / 255.0  # Normalize to [0, 1]
            
            # Add batch dimension
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
            
        except Exception as e:
            logger.error(f"Error preprocessing image {image_path}: {e}")
            raise
    
    def detect_sign(self, image_path: str) -> Dict:
        """
        Detect traffic sign in image
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Detection results dictionary
        """
        try:
            # Preprocess image
            input_data = self.preprocess_image(image_path)
            
            # Run inference
            start_time = time.time()
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            inference_time = time.time() - start_time
            
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
                'image_path': image_path,
                'timestamp': datetime.now().isoformat(),
                'inference_time_ms': round(inference_time * 1000, 2),
                'detected': confidence > self.confidence_threshold,
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
            logger.error(f"Error detecting sign in {image_path}: {e}")
            return {
                'image_path': image_path,
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'detected': False
            }
    
    def detect_batch(self, image_paths: List[str]) -> List[Dict]:
        """
        Detect traffic signs in multiple images
        
        Args:
            image_paths: List of image file paths
            
        Returns:
            List of detection results
        """
        results = []
        total_images = len(image_paths)
        
        logger.info(f"Processing {total_images} images...")
        
        for i, image_path in enumerate(image_paths, 1):
            logger.info(f"Processing image {i}/{total_images}: {os.path.basename(image_path)}")
            result = self.detect_sign(image_path)
            results.append(result)
        
        return results
    
    def save_results_to_json(self, results: List[Dict], output_path: str):
        """
        Save detection results to JSON file
        
        Args:
            results: List of detection results
            output_path: Path to save JSON file
        """
        try:
            # Create summary statistics
            total_detections = len(results)
            successful_detections = sum(1 for r in results if r.get('detected', False))
            failed_detections = total_detections - successful_detections
            
            # Average inference time
            inference_times = [r.get('inference_time_ms', 0) for r in results if 'inference_time_ms' in r]
            avg_inference_time = np.mean(inference_times) if inference_times else 0
            
            # Prepare output data
            output_data = {
                'detection_summary': {
                    'total_images': total_detections,
                    'successful_detections': successful_detections,
                    'failed_detections': failed_detections,
                    'success_rate': round(successful_detections / total_detections * 100, 2) if total_detections > 0 else 0,
                    'average_inference_time_ms': round(avg_inference_time, 2),
                    'detection_timestamp': datetime.now().isoformat()
                },
                'detections': results
            }
            
            # Save to JSON file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Results saved to: {output_path}")
            logger.info(f"Summary: {successful_detections}/{total_detections} successful detections")
            
        except Exception as e:
            logger.error(f"Error saving results to {output_path}: {e}")
            raise


def main():
    """Main function for testing the detector"""
    # Initialize detector
    detector = TrafficSignDetector()
    
    # Test with sample images
    test_images_dir = 'test_images'
    output_file = 'output/detection_results.json'
    
    if not os.path.exists(test_images_dir):
        logger.error(f"Test images directory not found: {test_images_dir}")
        return
    
    # Get all image files
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    image_paths = []
    
    for file in os.listdir(test_images_dir):
        if file.lower().endswith(image_extensions):
            image_paths.append(os.path.join(test_images_dir, file))
    
    if not image_paths:
        logger.error(f"No image files found in {test_images_dir}")
        return
    
    logger.info(f"Found {len(image_paths)} images to process")
    
    # Run detection
    results = detector.detect_batch(image_paths)
    
    # Save results
    os.makedirs('output', exist_ok=True)
    detector.save_results_to_json(results, output_file)
    
    print(f"\n✅ Detection complete!")
    print(f"📁 Results saved to: {output_file}")
    print(f"🎯 Processed {len(results)} images")


if __name__ == "__main__":
    main()
