Fixing Puzzles – Hardware Tetris Game (Planning & Pre-Build Stage)
Project Overview

Fixing Puzzles is a microcontroller-based Tetris-style game designed to run on a Raspberry Pi Pico (RP2040) with a small OLED display and physical input buttons. The project focuses on recreating the core mechanics of classic Tetris while emphasizing hardware-level input handling, display rendering, and efficient game logic suitable for embedded systems.

This repository currently represents the design and preparation phase of the project, where hardware planning, pin mapping, and core software structure have been completed prior to physical assembly.

Current Status

At present, the Raspberry Pi Pico and other hardware components are not yet available. However, significant progress has already been made in preparation for the build:

A complete planned parts list has been finalized

GPIO pin assignments and wiring logic have been designed

A rough wiring sketch has been created to guide future assembly

The core game logic and code structure are written and organized

Input handling, rotation logic, and game state flow have been planned

This planning-first approach follows Hack Club Blueprint’s recommended workflow and ensures that once hardware is obtained, the build process can begin smoothly.

<img width="1536" height="1024" alt="Fixing_Puzzel Rough Diagram" src="https://github.com/user-attachments/assets/bd5a6ebd-2581-47d4-9dec-38958890725b" />


Planned Hardware Components

Raspberry Pi Pico (RP2040)

0.96″ SSD1306 OLED display (128×64, I2C)

6 push buttons (movement, rotation, drop, pause/reset)

Breadboard and jumper wires

Internal or external pull-up resistors

USB or battery-based power supply

Optional buzzer for audio feedback

Planned Controls & Gameplay

Left / Right – Move the block horizontally

Rotate – Rotate the active piece

Down – Soft drop

Pause – Pause the game

Reset – Restart gameplay

The control layout is intentionally minimal to match the limited hardware while remaining fully playable.

Software Design

The software for Fixing Puzzles is structured to be modular and readable, separating responsibilities into clear components:

OLED display rendering over I2C

Button input handling with debouncing

Main Tetris game loop and timing

Collision detection and rotation rules

Score tracking and game state management

The code is written with microcontroller constraints in mind, prioritizing clarity, efficiency, and maintainability.

Learning Objectives

This project is intended as a hands-on learning experience in:

Embedded GPIO input handling

I2C-based display communication

Real-time game logic without an operating system

Hardware-first project planning

Clear and honest technical documentation

Next Steps

Once the required hardware components are obtained:

Assemble the circuit on a breadboard using the planned wiring

Test individual components (OLED display, button inputs)

Integrate and debug the full game

Optimize performance and reliability

Document the physical build with photos and logs

Record a gameplay demonstration

Documentation & Transparency

Fixing Puzzles will be fully documented through:

Build journals and progress logs

Wiring explanations and pin mappings

Well-commented source code

Honest discussion of challenges and fixes

Disclaimer

This project is inspired by the classic game Tetris. The focus is on hardware implementation, embedded programming, and learning, rather than originality of the game concept.
