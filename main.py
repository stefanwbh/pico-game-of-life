"""
Conway's Game of Life - MicroPython Edition

A hardware-accelerated implementation of the Game of Life for the Raspberry Pi Pico.
Uses Viper mode for smooth rendering and offers interactive real-time adjustments 
of cell size and simulation speed.

Required Hardware:
- Raspberry Pi Pico
- Waveshare 1.3-inch OLED Display (SH1107, 128x64 pixels, SPI) with built-in buttons

Pin Configuration:
- SPI1 (Display): SCK = Pin(10), MOSI = Pin(11), MISO = Pin(12)
- Display Control: DC = Pin(8), RES = Pin(12), CS = Pin(19)
- Input: Key0 (Start/Stop) = Pin(15), Key1 (Size/Speed) = Pin(17)

Author: Stefan Webhofer
Feel free to check out my artworks and designs over at https://stefanwbh.artstation.com/ :)
"""


from machine import Pin, SPI
from time import sleep
import sh1107
import array
import random

# Setup display
sq_size = 1
WIDTH, HEIGHT = 128, 64
cols, rows = int(WIDTH / sq_size), int(HEIGHT / sq_size)
speed = 2

spi1 = SPI(1, baudrate=1_000_000, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
display = sh1107.SH1107_SPI(128, 64, spi1, Pin(8), Pin(12), Pin(19), rotate=0)
key0 = Pin(15,Pin.IN,Pin.PULL_DOWN)
key1 = Pin(17,Pin.IN,Pin.PULL_DOWN)



# Draw grid based on sq_size
def draw_grid(grid):
    display.fill(0)
    for y in range(rows):
        for x in range(cols):
            if grid[y * cols + x] > 0:
                display.fill_rect(x * sq_size, y * sq_size, sq_size, sq_size, 1)
    display.show()

# Define grid
current_grid = bytearray(cols * rows)
next_grid = bytearray(cols * rows)

# Initialize start
def init_state(grid):
    for x in range(cols):
        for y in range(rows):
            idx = y * cols + x
            grid[idx] = random.getrandbits(1)

# Update grid according to rules of game of life
@micropython.viper
def update_grid(current_grid, next_grid):
    curr_ptr = ptr8(current_grid)
    next_ptr = ptr8(next_grid)
    
    h = int(rows)
    w = int(cols)
    
    for y in range(h):
        # Calculate neighbor rows
        y_up = ((y - 1 + h) % h) * w
        y_curr = y * w
        y_down = ((y + 1) % h) * w
        
        # Calculate neighor cols
        for x in range(w):
            x_left = (x - 1 + w) % w
            x_right = ((x + 1) % w) % w
            
            # Sum of neighbors
            n = (curr_ptr[y_up + x_left] + curr_ptr[y_up + x] +
                 curr_ptr[y_up + x_right] + curr_ptr[y_curr + x_left] +
                 curr_ptr[y_curr + x_right] + curr_ptr[y_down + x_left] +
                 curr_ptr[y_down + x] + curr_ptr[y_down + x_right])
            
            idx = y_curr + x
            
            # Apply rules
            if curr_ptr[idx] == 1:
                next_ptr[idx] = 1 if (n == 2 or n == 3) else 0
            else:
                next_ptr[idx] = 1 if (n == 3) else 0

# Draws speed screen during game
def draw_speed_screen(speed):
    display.fill(0)
    if speed == 0:
        # Draws infinity symbol
        display.text("Speed: o", 27, 27, 1)
        display.text("o", 88, 27, 1)
    elif speed < 0:
        display.text(f"Speed: 0", 27, 27, 1)
    else:
        display.text(f"Speed: {int(-(2 * speed) + 5)}", 27, 27, 1)
    display.show()
    sleep(1)

# Draw starting screen
def draw_starting_screen():
    display.fill(0)
    display.text("Starting", 27, 23, 1)
    display.text("game...", 27, 32, 1)
    display.show()
    sleep(1.5)

# Draw stopping screen
def draw_stopping_screen():
    display.fill(0)
    display.text("Stopping", 27, 23, 1)
    display.text("game...", 27, 32, 1)
    display.show()
    sleep(1.5)

def draw_start_screen(sq_size):
    display.fill(0)
    
    # Title text
    display.text("GAME OF LIFE", 18, 5, 1)
    display.hline(18, 15, 95, 1)
    
    # sq_size box
    display.rect(30, 20, 68, 18, 1)
    display.text(f"Size:{sq_size}", 38, 25, 1)
    
    # Help text
    display.text("Key0: Start/Stop", 0, 43, 1)
    display.text("Key1: Size/Speed", 0, 53, 1)
    
    display.show()

def game_loop():
    global speed
    while(True):
        # Stop game
        if key0.value() == 0:
            draw_stopping_screen()
            break
        # Change speed
        if key1.value() == 0:
            speed = speed - .5
            if speed < 0:
                print("speed: 0")
                draw_speed_screen(-1)
                # Speed 0 aka pause
                while True:
                    draw_grid(current_grid)
                    sleep(.1)
                    if key1.value() == 0:
                        break
                    if key0.value() == 0:
                        draw_stopping_screen()
                        return
                speed = 2
            draw_speed_screen(speed)
            
        # Update grid
        update_grid(current_grid, next_grid)
        current_grid[:] = next_grid[:]
        # Draw grid
        draw_grid(current_grid)
        sleep(speed)

def start():
    global sq_size, cols, rows, current_grid, next_grid, speed
    while True:
        # Start game
        if key0.value() == 0:
            cols = int(WIDTH / sq_size)
            rows = int(HEIGHT / sq_size)
            speed = 2
            current_grid = bytearray(cols * rows)
            next_grid = bytearray(cols * rows)
            init_state(current_grid)
            draw_starting_screen()
            game_loop()
        
        # Change size of tiles
        if key1.value() == 0:
            sq_size = (sq_size * 2) % 64
            if sq_size == 0:
                sq_size = 1
            sleep(.2)
            
        draw_start_screen(sq_size)
    
start()
