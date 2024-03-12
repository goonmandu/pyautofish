print("Preparing detection system... ", end="")
import time
from pynput.mouse import Button, Controller
import keyboard
import win32con
import win32api
from window_image import snapshot

mouse = Controller()
avg_time = 0.0
throw_time = 0.0
catch_time = 0.0
time_to_catch = 0.0
total_time = 0.0
catch_number = 0
exit_key = "f7"
mouse_move_dir = True


def right_click():
    mouse.press(Button.right)
    mouse.release(Button.right)


def format_number(number, decimal_digits):
    if number < 10:
        return f" {round(number, decimal_digits)}"
    else:
        return f"{round(number, decimal_digits)}"


hundredpct_coords = ((178, 261), (288, 261), (398, 261))
print("Done.")

mcidx = int(input("Where is Minecraft located in the Volume Mixer? Enter 1-3. ")) - 1
move_mouse = input("Bypass McMMO's overfishing anti-autofisher? [Y]es/[Any]No: ").lower() in ["yes", "y"]

print("\n\nConfiguration Details:")
print(f"Key to stop the autofisher: {exit_key.upper()}")
print(f"Minecraft location in VMix: {mcidx+1}")
print(f"McMMO Overfishing Bypass: {move_mouse}")
input("\nPress [Enter] to confirm these settings and start the autofisher. If not, press Ctrl+C to exit.")

print("Starting in 5 seconds.\n")
time.sleep(5)
print("---- Autofish Statistics ----")

right_click()

throw_time = time.time()
time.sleep(3)

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
        print(f"Catch {catch_number}: {format_number(time_to_catch,1)}s "
              f"| Avg: {format_number(avg_time, 1)}s")
                                                                # print fishing stats
        time.sleep(1)                                           # time delay between catch and recast rod
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
        time.sleep(3)                                           # wait for volume meter to die down
