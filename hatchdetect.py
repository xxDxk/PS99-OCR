from PIL import ImageGrab, Image
import pytesseract
import requests
import time
import os
import cv2
import numpy as np
import json
import tempfile

WEBHOOK_URL = "https://discord.com/api/webhooks/1335972305230368878/mLQKlBUnDy7QKbA-7Hs6xFj2ga5kGx9PemeVNLTsRENtIjX0D8hHXmGpv8iQswZBLXfb" # enter webhook link here
DISCORD_ROLE_ID = "ENTER_ID" # enter a role ID / default
DISCORD_USER_ID = "ENTER_ID" # enter a user ID / overrides ROLE

def send_discord_message(image_path=None):
    try:
        print("📤 Preparing to send message...")
        mention = f"<@&{DISCORD_ROLE_ID}>" if DISCORD_USER_ID is None else f"<@{DISCORD_USER_ID}>"
        data = {
            "embeds": [
                {
                    "title": "New Pet Hatch",
                    "description": mention,
                    "image": {"url": "attachment://screenshot.png"},
                    "footer": {"text": "Hatches"}
                }
            ]
        }

        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as f:
                files = {"file": ("screenshot.png", f, "image/png")}
                response = requests.post(WEBHOOK_URL, data={"payload_json": json.dumps(data)}, files=files)
        else:
            response = requests.post(WEBHOOK_URL, json=data)

        if response.status_code in [200, 204]:
            print("✅ Message and image sent!")
        else:
            print(f"❌ Failed! Status Code: {response.status_code}, Response: {response.text}")

    except Exception as e:
        print(f"⚠️ Error sending message: {e}")

def process_image_for_ocr(image):
    print("🖼️ Preprocessing image for OCR...")
    img = np.array(image)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Invert colors
    inverted = cv2.bitwise_not(gray)

    # Apply thresholding to enhance text contrast
    _, thresh = cv2.threshold(inverted, 150, 255, cv2.THRESH_BINARY)

    # Upscale image 2x for better OCR
    upscaled = cv2.resize(thresh, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Apply slight blur
    blurred = cv2.GaussianBlur(upscaled, (5, 5), 0)

    return blurred, img

def check_for_pet():
    print("✅ Real-time monitoring started. Watching for Pet hatches...")
    while True:
        try:
            print("🖼️ Taking screenshot...")
            screenshot = ImageGrab.grab(all_screens=True)
            
            print("🔍 Enhancing image for better OCR...")
            processed_image, original = process_image_for_ocr(screenshot)

            print("📝 Running OCR...")
            custom_config = r'--oem 1 --psm 6'
            text = pytesseract.image_to_string(processed_image, config=custom_config)

            if "Pet" in text:
                print("👀 'Pet' found in text!")

                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
                    image_path = tmpfile.name
                    screenshot.save(image_path)

                send_discord_message(image_path)
            else:
                print("❌ 'Pet' not found in text")

            time.sleep(3)  # Faster real-time monitoring

        except Exception as e:
            print(f"⚠️ Error in loop: {e}")
            time.sleep(3)

def start_menu():
    print("🖥️ Welcome to the Hatch Detection Script! - by jajtxs_")
    print("===========================================")
    print("1. Start real-time monitoring for 'Pet' hatches.")
    print("2. Exit.")
    choice = input("Please select an option (1 or 2): ")
    if choice == '1':
        check_for_pet()
    elif choice == '2':
        print("👋 Exiting. Goodbye!")
        exit()
    else:
        print("❌ Invalid choice. Please select 1 or 2.")
        start_menu()

if __name__ == "__main__":
    start_menu()
