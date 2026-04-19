# Pico Game of Life

A hardware-accelerated implementation of Conway's Game of Life for the Raspberry Pi Pico and the Waveshare 1.3-inch OLED display (SH1107). This project utilizes the MicroPython Viper mode for smooth, high-performance rendering.

## Hardware Requirements
* **Raspberry Pi Pico**
* **Waveshare 1.3-inch OLED Display** (SH1107, 128x64 pixels, SPI) with built-in buttons

## Installation
1. Flash your Raspberry Pi Pico with the latest MicroPython firmware.
2. Create a folder named `lib` on your Pico and upload the `sh1107.py` driver file into it.
3. Upload the `main.py` file to the root directory of your Pico and restart the device.

## Controls
> **Important:** Hold the buttons for start, stop, and speed adjustments until the corresponding loading or info screen appears on the display.

* **Key 0:** Starts the simulation from the start menu. During an active simulation or while the game is paused, holding this key stops the game and returns you to the menu.
* **Key 1:** Changes the cell size (square size) while in the start menu. During an active simulation, holding this key cycles through the speed settings or pauses the game.

## Author
Created by **Stefan Webhofer**.  
Feel free to check out my artworks and designs over at [stefanwbh.artstation.com](https://stefanwbh.artstation.com/) :)
