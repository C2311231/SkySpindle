# SkySpindle

SkySpindle is a web interface for GRBL CNC machines, inspired by Mainsail.
It was developed as a personal project to explore web-based CNC control.

## Status

⚠️ Inactive: The project is no longer actively developed.
Core functionality works but is not maintained for production use and may be buggy.

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
It demonstrates experimentation with web-based CNC control, threading, and real-time updates. It is unmaintained ABSOLUTELY NOT recommended for use on a live machine.
