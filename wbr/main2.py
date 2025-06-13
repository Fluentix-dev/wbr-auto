import pyautogui
import time
from PIL import Image
import sys

# ─── CONFIGURATION ─────────────────────────────────────────────────────────────

INPUT_IMG = 'wbr/imgs/input_field.png'  # Path to the input field image
NEXT_IMG  = 'wbr/imgs/next_button_mac.png'  # Path to the next button image

pyautogui.PAUSE = 0.3
pyautogui.FAILSAFE = True

# ─── FUNCTIONS ─────────────────────────────────────────────────────────────────

def get_scaling_factor():
    screen_width, screen_height = pyautogui.size()
    screenshot = pyautogui.screenshot()
    img_width, img_height = screenshot.size
    scale_x = img_width / screen_width
    scale_y = img_height / screen_height
    return scale_x, scale_y

def wait_and_click(image_path, label, confidence=0.8, timeout=20):
    scale_x, scale_y = get_scaling_factor()
    start_time = time.time()
    while time.time() - start_time < timeout:
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if location:
            center_x, center_y = pyautogui.center(location)
            # Adjust for Retina scaling
            adjusted_x = center_x / scale_x
            adjusted_y = center_y / scale_y
            pyautogui.click(adjusted_x, adjusted_y)
            pyautogui.click(adjusted_x, adjusted_y)
            print(f"✅ Clicked {label} at ({adjusted_x}, {adjusted_y})")
            return True
    print(f"❌ Timeout: {label} not found.")
    return False

# ─── MAIN SCRIPT ───────────────────────────────────────────────────────────────

def main():
    try:
        with open("wbr/data.txt", "r", encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("⚠️ 'data.txt' not found.")
        return

    if not words:
        print("⚠️ No words found in data.txt.")
        return

    print()
    input("🌐 Open https://whatbeatsarock.com and press ENTER to begin...")

    NUMS = {
        '0': "zero", '1': "one", '2': "two", '3': "three", '4': "four",
        '5': "five", '6': "six", '7': "seven", '8': "eight", '9': "nine"
    }
    p = 0
    for i, word in enumerate(words, 1):
        for number in NUMS:
            word = word.replace(number, NUMS[number])

        print(f"[{i}/{len(words)}] Typing: {word}")
        img_found = False
        while not img_found:
            try:
                wait_and_click(INPUT_IMG, "input field")
                img_found = True
            except:
                pass

        pyautogui.write(word)
        pyautogui.press('enter')

        img_found = False
        while not img_found:
            try:
                wait_and_click(NEXT_IMG, "next button")
                img_found = True
                p += 1
            except KeyboardInterrupt:
                print("Stopped")
                sys.exit(1)
            except:
                if p < 11:
                    pyautogui.scroll(-1)

    print("🎉 All words processed!")

if __name__ == "__main__":
    main()
