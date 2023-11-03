print("Preparing detection system... ", end="")
import time
from pynput.mouse import Button, Controller
import keyboard
import win32con
import win32api
from window_image import snapshot
print("Done.")

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
exit_key = "ctrl"
mouse_move_dir = True

def right_click():
    mouse.press(Button.right)
    mouse.release(Button.right)

hundredpct_coords = ((178, 261), (288, 261), (398, 261))
mcidx = int(input("Where is Minecraft located in the Volume Mixer? Enter 1-3. ")) - 1
move_mouse = input("Bypass McMMO's overfishing anti-autofisher? [Y]es/[Any]No: ").lower() in ["yes", "y"]

print("\n\nConfiguration Details:")
print(f"Key to stop the autofisher: {exit_key.upper()}")
print(f"Minecraft location in VMix: {mcidx+1}")
print(f"McMMO Overfishing Bypass: {move_mouse}")
input("\nPress [Enter] to confirm these settings and start the autofisher. If not, press Ctrl+C to exit.")

print("Starting in 5 seconds.")

time.sleep(5)

right_click()
throw_time = time.time()
time.sleep(1)
while True:
    if keyboard.is_pressed(exit_key):
        raise Exception(f"Terminated by user: pressed {exit_key.upper()}")
    snap = snapshot()
    if snap.getpixel(hundredpct_coords[mcidx])[0] < 231:        # Red-value < 231
        right_click()                                           # reel in fish
        catch_time = time.time()                                # end timer
        catch_number += 1                                       # increment number of catches by 1
        time_to_catch = catch_time - throw_time                 # end timer and save Δtime.time()
        total_time += time_to_catch                             # update total time spent fishing
        avg_time = total_time / catch_number                    # update average time per fish caught
        print("Catch " + str(catch_number) + ": " + str(round(time_to_catch, 2)) + " | AVG: " + str(round(avg_time, 2)))
                                                                # print fishing stats TODO: Formatting
        time.sleep(0.75)                                        # time delay between catch and recast rod
        if move_mouse:
            if mouse_move_dir:
                for i in range(160):
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 5, 0, 0, 0)
                mouse_move_dir = False
            else:
                for i in range(160):
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -5, 0, 0, 0)
                mouse_move_dir = True
        right_click()                                           # cast fishing rod
        throw_time = time.time()                                # start timer
        time.sleep(2)                                           # wait for volume meter to die down
