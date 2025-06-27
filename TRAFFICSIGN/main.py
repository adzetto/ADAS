#!/usr/bin/env python3
"""
GTSRB CORE - Main Entry Point
=============================

Main script that provides a simple interface to all CORE functionality.
"""

import sys
import os
import argparse

def main():
    """Main entry point with command routing"""
    
    parser = argparse.ArgumentParser(
        description='GTSRB Traffic Sign Detection - CORE Module',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py test                    # Run tests
  python main.py demo                    # Run interactive demo
  python main.py detect image.jpg       # Detect single image
  python main.py batch images/          # Batch process directory
  python main.py pi-camera              # Run Pi camera detection
  python main.py pi-camera -c 0.4 -i 0.5 # High-frequency Pi detection
  python main.py usage                  # Show usage guide
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Run module tests')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run interactive demo')
    
    # Single detection command
    detect_parser = subparsers.add_parser('detect', help='Detect single image')
    detect_parser.add_argument('image', help='Path to image file')
    detect_parser.add_argument('-o', '--output', help='Output JSON file')
    detect_parser.add_argument('-c', '--confidence', type=float, default=0.3,
                              help='Confidence threshold (default: 0.3)')
    
    # Batch processing command
    batch_parser = subparsers.add_parser('batch', help='Batch process directory')
    batch_parser.add_argument('directory', help='Directory containing images')
    batch_parser.add_argument('-o', '--output', default='output/batch_results.json',
                             help='Output JSON file (default: output/batch_results.json)')
    batch_parser.add_argument('-c', '--confidence', type=float, default=0.3,
                             help='Confidence threshold (default: 0.3)')
    
    # Usage command
    usage_parser = subparsers.add_parser('usage', help='Show usage guide')
    
    # Pi Camera command
    pi_parser = subparsers.add_parser('pi-camera', help='Run Raspberry Pi camera detection')
    pi_parser.add_argument('-c', '--confidence', type=float, default=0.3,
                          help='Confidence threshold (default: 0.3)')
    pi_parser.add_argument('-r', '--resolution', default='1920x1080',
                          help='Camera resolution WxH (default: 1920x1080)')
    pi_parser.add_argument('-i', '--interval', type=float, default=1.0,
                          help='Detection interval in seconds (default: 1.0)')
    pi_parser.add_argument('-d', '--duration', type=float,
                          help='Detection duration in seconds (optional)')
    pi_parser.add_argument('--no-save', action='store_true',
                          help='Do not save results to file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Route to appropriate script
    if args.command == 'test':
        import test_core
        return test_core.main()
    
    elif args.command == 'demo':
        import demo
        return demo.main()
    
    elif args.command == 'detect':
        import single_detect
        
        # Prepare arguments for single_detect
        sys.argv = ['single_detect.py', args.image]
        if args.output:
            sys.argv.extend(['-o', args.output])
        if args.confidence != 0.3:
            sys.argv.extend(['-c', str(args.confidence)])
        
        return single_detect.main()
    
    elif args.command == 'batch':
        import batch_detect
        
        # Prepare arguments for batch_detect
        sys.argv = ['batch_detect.py', args.directory]
        if args.output != 'output/batch_results.json':
            sys.argv.extend(['-o', args.output])
        if args.confidence != 0.3:
            sys.argv.extend(['-c', str(args.confidence)])
        
        return batch_detect.main()
    
    elif args.command == 'usage':
        import usage
        return usage.main()
    
    elif args.command == 'pi-camera':
        import pi_camera_detector
        
        # Prepare arguments for pi_camera_detector
        sys.argv = ['pi_camera_detector.py']
        if args.confidence != 0.3:
            sys.argv.extend(['--confidence', str(args.confidence)])
        if args.resolution != '1920x1080':
            sys.argv.extend(['--resolution', args.resolution])
        if args.interval != 1.0:
            sys.argv.extend(['--interval', str(args.interval)])
        if args.duration:
            sys.argv.extend(['--duration', str(args.duration)])
        if args.no_save:
            sys.argv.append('--no-save')
        
        return pi_camera_detector.main()
    
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
