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
    
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
