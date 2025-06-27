# ADAS Project

This repository contains a collection of projects related to Advanced Driver-Assistance Systems (ADAS). The project is divided into the following components:

## Components

*   **ADAS-screen**: A C++ Qt application for displaying ADAS information on a Raspberry Pi. It provides a full-screen display with different modes for dashboard information, rear view camera, and navigation.

*   **LORA**: This directory appears to contain a PlatformIO project for LoRa communication, likely used for vehicle-to-vehicle or vehicle-to-infrastructure communication.

*   **TRAFFICSIGN/CORE**: A Python-based traffic sign detection module using TensorFlow Lite. It can detect and classify German traffic signs from single images or a batch of images.

*   **Ultra-Fast-Lane-Detection**: A PyTorch implementation of the "Ultra Fast Structure-aware Deep Lane Detection" paper. This component is for detecting lane lines on the road.

## Getting Started

Each component has its own set of instructions and dependencies. Please refer to the `README.md` file within each subdirectory for more information on how to set up and use each component.

*   [ADAS-screen/README.md](/ADAS-screen/README.md)
*   [LORA/README.md](/LORA/README.md)
*   [TRAFFICSIGN/CORE/README.md](/TRAFFICSIGN/CORE/README.md)
*   [Ultra-Fast-Lane-Detection/README.md](/Ultra-Fast-Lane-Detection/README.md)

## Usage

The components in this repository can be used together to build a complete ADAS system. For example, the lane detection and traffic sign detection modules can provide input to the ADAS display screen.
