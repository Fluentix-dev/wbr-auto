import pyautogui
import time
import sys

# ─── CONFIG ────────────────────────────────────────────────────────────────────

INPUT_IMG = 'wbr/imgs/input_field.png'
NEXT_IMG  = 'wbr/imgs/next_button.png'

pyautogui.PAUSE = 0.3
pyautogui.FAILSAFE = True

# ─── FUNCTIONS ─────────────────────────────────────────────────────────────────

def wait_and_click(image_path, label, confidence=0.8, timeout=20):
    start_time = time.time()
    while time.time() - start_time < timeout:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        if location:
            pyautogui.click(location)
            print(f"✅ Clicked {label} at {location}")
            return True
        time.sleep(0.3)

    print(f"❌ Timeout: {label} not found.")
    return False

# ─── MAIN SCRIPT ───────────────────────────────────────────────────────────────

def main():
    # Load word list
    with open("wbr/data.txt", "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]

    if not words:
        print("⚠️ No words found in data.txt.")
        return

    print()
    input("🌐 Open https://whatbeatsarock.com and press ENTER to begin...")

    not_found_img = True
    while not_found_img:
        try:
            wait_and_click(INPUT_IMG, "input field")
            not_found_img = False
        except:
            pass

    NUMS = {'0': "zero", '1': "one", '2': "two", '3': "three", '4': "four", "5": "five", "6": "six", "7": "seven", '8': 'eight', '9': 'nine'}
    p = 0
    for i, word in enumerate(words, 1):
        for number in NUMS:
            word = word.replace(number, NUMS[number])

        print(f"[{i}/{len(words)}] Typing: {word}")
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.write(word)
        pyautogui.press('enter')
        
        not_found_img = True
        while not_found_img:
            try:
                wait_and_click(NEXT_IMG, "next button")
                not_found_img = False
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
