from PIL import ImageGrab
import time
from pynput.mouse import Button, Controller

mouse = Controller()
avg_time = 0.0
throw_time = 0.0
catch_time = 0.0
time_to_catch = 0.0
total_time = 0.0
catch_number = 0
time_to_catch_string = ""
avg_time_string = ""
catch_number_string = ""

def right_click():
    mouse.press(Button.right)
    mouse.release(Button.right)

setup_detect = ImageGrab.grab(bbox=(1819, 912, 1823, 914))
setup_detect_rgb = setup_detect.convert("RGB")
initial_r, initial_g, initial_b = setup_detect_rgb.getpixel((2, 1))
while initial_r != 231:
    print("Please realign Volume Mixer window. Then, press ENTER to check its position again.")
    input("Expected R = 231, Detected Value = " + str(initial_r))
    setup_detect = ImageGrab.grab(bbox=(1819, 912, 1823, 914))
    setup_detect_rgb = setup_detect.convert("RGB")
    initial_r, initial_g, initial_b = setup_detect_rgb.getpixel((2, 1))

print("Success: Detected R value matches Expected R value.")

input("Press ENTER to run script")
print("Executing in 5 seconds... Ctrl + C to quit")
time.sleep(1)
print("Executing in 4...")
time.sleep(1)
print("Executing in 3...")
time.sleep(1)
print("Executing in 2...")
time.sleep(1)
print("Executing in 1...")
time.sleep(1)

right_click()
throw_time = time.time() # start timer
time.sleep(1)
while True:                                                     # forever loop (terminate with KeyboardInterrupt):
    bobber_sound = ImageGrab.grab(bbox=(1819, 912, 1823, 914))  # scan for Volume Meter
    bobber_sound_rgb = bobber_sound.convert("RGB")              # convert ImageGrab area to RGB
    r, g, b = bobber_sound_rgb.getpixel((2, 1))                 # read pixel RGB values
    time.sleep(0.02)                                           # scanning frequency
    if r == 51:                                                # is sound detected?
        right_click()                                           # catch fish
        catch_time = time.time()                                # end timer
        catch_number += 1                                       # increment number of catches by 1
        time_to_catch = catch_time - throw_time                 # end timer and save Δtime.time()
        total_time += time_to_catch                             # update total time spent fishing
        avg_time = total_time / catch_number                    # update average time per fish caught
        print("Catch " + str(catch_number) + ": " + str(round(time_to_catch, 2)) + " | AVG: " + str(round(avg_time, 2)))
                                                                # print fishing stats TODO: Formatting
        time.sleep(0.75)                                         # time delay between catch and recast rod
        right_click()                                           # cast fishing rod
        throw_time = time.time()                                # start timer
        time.sleep(2)                                         # wait for volume meter to die down