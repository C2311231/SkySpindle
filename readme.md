# SkySpindle

[Video Demo](https://youtu.be/kn8z4xmTRlk)

SkySpindle is a web interface for GRBL CNC machines, inspired by Mainsail.
It was developed as a personal project to explore web-based CNC control.

## Status

⚠️ Inactive: The project is no longer actively developed.  
Core functionality works but is not maintained and is not safe for use. Do **NOT** use this software for any CNC operations.

## Structure

The project is separated into three main sections:

**1. Web Interface**  
Handles the user interface with modular HTML, CSS, and JavaScript files, supported by Python scripts for hosting and request handling. Modular design allows new sections to be added easily.

**2. GRBL Tools**  
Responsible for communication with the CNC machine, including sending commands and reading responses. Operations use threaded communication to avoid conflicts and maintain timing. (Some components are experimental and not fully reliable.)

**3. Helpers**  
Contains utility functions used across the project, mostly for internal purposes.

Other files include version control, dependencies (`requirements.txt`), and main program startup.

## Features (Implemented)

- Web-based control interface for GRBL CNC
- Basic job management
- Web UI G-code editing
- Program updates from Web UI
- Threaded operation for concurrency
- Real-time connection to backend over WebSockets
- Emergency stop/restart button
- Machine Settings editor (full support for Grbl $-commands)
- Jog controls with adjustable distance, feed, spindle, and rapid overrides
- Homing and axis zeroing
- Spindle and coolant control (Mist/Flood)
- Job status with live ETA, progress, and line number
- Alarm unlock for Grbl alarm states
- Operation list management (upload, start, pause, cancel)

## Tech Stack

HTML, CSS, JavaScript, Python, WebSockets

## Notes

This project was primarily a learning exercise in web interfaces and web development, created after acquiring a low-cost CNC machine.
It demonstrates experimentation with web-based CNC control, threading, and real-time updates. It is unmaintained, has little error handling, and is ABSOLUTELY NOT recommended for use on a live machine.
