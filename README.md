# Love You

A full-screen generative art piece built with **Pygame** that renders an animated heart shape composed of glowing, flickering text particles, synchronized with background music.

### Direct Downloads 

[![Download Linux](https://img.shields.io/badge/Download-Linux_Binary-7C3AED?style=for-the-badge&logo=linux&logoColor=white)](https://github.com/luoijin/Love-You/releases/download/v1.0.1/LoveYou-Linux)
[![Download macOS App](https://img.shields.io/badge/Download-macOS_.app-7C3AED?style=for-the-badge&logo=apple&logoColor=white)](https://github.com/luoijin/Love-You/releases/download/v1.0.1/LoveYou-macOS.zip)
[![Download Windows](https://img.shields.io/badge/Download-Windows_.exe-7C3AED?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/luoijin/Love-You/releases/download/v1.0.1/LoveYou.exe)

[![Total Downloads](https://img.shields.io/github/downloads/luoijin/Love-You/total?style=for-the-badge&logo=github&logoColor=7C3AED&label=TOTAL%20DOWNLOADS&labelColor=0f172a&color=7C3AED&v=1)](https://github.com/luoijin/Love-You/releases)


## Overview

The program procedurally constructs a heart shape from parametric equations, then populates it with two categories of animated text particles:

- **Outline particles** — trace the boundary of the heart and appear sequentially, giving the impression of the heart being "drawn."
- **Fill particles** — populate the interior of the heart and fade in progressively after the outline completes, adding volume and density to the shape.

Each particle renders a short phrase in a randomly assigned color, with a soft multi-layer glow effect and a subtle flicker animation. Once the heart has fully formed, a pulsing centered message fades in at the middle of the screen. When the accompanying audio track finishes playing, the entire animation resets and loops.

## Features

- Procedurally generated heart outline using a parametric heart curve
- Randomized, non-overlapping placement of outline and fill particles
- Glow rendering via layered, scaled, alpha-blended text surfaces
- Per-particle flicker animation using sine-wave modulation
- Staggered fade-in timing to animate the heart being "written" into existence
- Pulsing center text with its own glow and fade-in effect
- Background music playback with automatic animation reset on loop
- Full-screen rendering, scaled to the user's display resolution

## Requirements

- Python 3.8 or later
- [Pygame](https://www.pygame.org/) library


## Assets

The script expects an audio file named `love_you.mp3` to be present in the same directory as the script. If this file is missing or fails to load, the animation will still run, but without music playback (an error message will be printed to the console).

## Setup & Usage
 
The project is distributed as source only; run it with a local Python installation using the platform-specific steps below.
 
### Linux
 
```bash
# Install Python and required system libraries
sudo apt update
sudo apt install python3 python3-venv python3-pip
 
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate
 
# Install dependencies
pip install pygame
 
# Run the animation
python3 LoveYou.py
```
 
> Ensure an X11 or Wayland display server is available; the script will not run on a headless session without a virtual display (e.g. `xvfb`).
 
### macOS
 
```bash
# Install Python via Homebrew if not already present
brew install python
 
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate
 
# Install dependencies
pip install pygame
 
# Run the animation
python3 LoveYou.py
```
 
> On first run, macOS may prompt for permission to control the display or access audio devices — allow these prompts for the animation and music to work correctly.
 
### Windows
 
```powershell
# Ensure Python 3.8+ is installed and available on PATH
 
# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate
 
# Install dependencies
pip install pygame
 
# Run the animation
python LoveYou.py
```
 
> Run the command from PowerShell or Command Prompt in the project directory. If `python` is not recognized, use `py` instead (e.g. `py -m venv venv`).
 
---
 
In all cases, the application launches in full-screen mode at the display's native resolution.

### Controls

| Input | Action |
|---|---|
| `Esc` | Exit the application |
| Close window / Quit event | Exit the application |

## Configuration

The following constants near the top of the script can be adjusted to customize the animation:

| Constant | Description |
|---|---|
| `WIDTH`, `HEIGHT` | Initial window dimensions (overridden by detected display resolution at runtime) |
| `BACKGROUND_COLOR` | RGB background color |
| `FPS` | Target frame rate |
| `SCALE` | Scale factor applied to the parametric heart curve |
| `WORDS` | List of phrases randomly assigned to individual particles |
| `CENTER_TEXT` | Text displayed at the center of the screen once the heart completes |
| `COLORS` | Palette of RGB colors randomly assigned to particles |

Particle density and spacing can be tuned via the `n_outline`, `n_fill`, and `min_gap` parameters in `build_heart_particles()`, `build_fill_particles()`, and `reset_animation()`.

## How It Works

1. **Heart geometry** — `heart_xy(t)` computes points along a parametric heart curve for a given angle `t`. `to_screen()` maps these coordinates into screen space using the configured scale and screen center.
2. **Particle generation** — `build_heart_particles()` samples points along the curve's outline; `build_fill_particles()` samples points within the curve's interior using polar-style sampling with a minimum spacing constraint to avoid overlap.
3. **Timing** — `reset_animation()` assigns each particle a `delay` value (in frames) so that outline particles appear sequentially first, followed by fill particles, creating a "drawing in" effect.
4. **Rendering loop** — On each frame, particle alpha values are incremented until fully visible, then modulated with a sine-based flicker. Each particle's text is rendered with a two-layer glow effect via `draw_glow_text()`, composited onto separate glow and text surfaces, and blitted to the screen.
5. **Center reveal** — After a configured delay past the fill animation, a pulsing, fading center message is rendered on top of the completed heart.
6. **Looping** — When the background track finishes playing, the particle system and frame counter are reset, restarting the animation in sync with the music.

## Notes

- The application runs in full-screen mode by default; modify the `pygame.display.set_mode()` call to run in a windowed mode instead.
- Font rendering uses the system-installed `Arial` and `Georgia` fonts via `pygame.font.SysFont`; availability may vary by operating system.
- All exceptions raised during execution are caught and printed with a full traceback to aid debugging.

## License

This project is licensed under the [MIT License](LICENSE).