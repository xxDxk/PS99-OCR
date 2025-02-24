from PIL import ImageGrab
import pytesseract
import requests
import time
import re  # For extracting words after "Huge"

WEBHOOK_URL = "https://discord.com/api/webhooks/1335972305230368878/mLQKlBUnDy7QKbA-7Hs6xFj2ga5kGx9PemeVNLTsRENtIjX0D8hHXmGpv8iQswZBLXfb"

def send_discord_message(message, image_path=None):
    """ Sends a message and optional image to the Discord webhook """
    try:
        data = {"content": message}
        files = {"file": open(image_path, "rb")} if image_path else None
        
        response = requests.post(WEBHOOK_URL, json=data)  # Send message first
        if files:
            response = requests.post(WEBHOOK_URL, files=files)  # Send image

        if response.status_code in [200, 204]:
            print("Message and image sent!")
        else:
            print(f"Failed! Status Code: {response.status_code}")

    except Exception as e:
        print(f"Error sending message: {e}")

def extract_text_after_huge(text):
    """ Finds 'Huge' and returns the words after it """
    match = re.search(r"Huge\s+([A-Za-z0-9]+)", text)  # Looks for 'Huge' followed by a word
    if match:
        return match.group(1)  # Returns the word after 'Huge'
    return None

def check_for_huge():
    """ Continuously checks for 'Huge' and extracts text after it """
    while True:
        try:
            screenshot = ImageGrab.grab()
            text = pytesseract.image_to_string(screenshot)

            if "Huge" in text:
                image_path = "screenshot.png"
                screenshot.save(image_path)  # Save the screenshot
                
                word_after_huge = extract_text_after_huge(text)
                if word_after_huge:
                    message = f"Huge {word_after_huge} appeared!"
                else:
                    message = "Huge appeared!"

                send_discord_message(message, image_path)

            time.sleep(5)  # Prevent excessive CPU usage

        except Exception as e:
            print(f"Error in loop: {e}")
            time.sleep(5)

# Start the script
if __name__ == "__main__":
    check_for_huge()
