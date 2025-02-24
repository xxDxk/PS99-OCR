from PIL import ImageGrab
import pytesseract
import requests
import time
import re  # For extracting words after "Huge"

def get_webhook_url():
    """ Prompts the user to input a Discord webhook URL """
    webhook_url = input("Enter your Discord webhook URL: ").strip()
    if not webhook_url:
        print("No webhook URL provided. Exiting...")
        exit()
    return webhook_url

def send_discord_message(webhook_url, message, image_path=None):
    """ Sends a message and optional image to the Discord webhook """
    try:
        data = {"content": message}
        files = {"file": open(image_path, "rb")} if image_path else None
        
        response = requests.post(webhook_url, json=data)  # Send message first
        if files:
            response = requests.post(webhook_url, files=files)  # Send image

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

def check_for_huge(webhook_url):
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

                send_discord_message(webhook_url, message, image_path)

            time.sleep(5)  # Prevent excessive CPU usage

        except Exception as e:
            print(f"Error in loop: {e}")
            time.sleep(5)

# Start the script
if __name__ == "__main__":
    webhook_url = get_webhook_url()  # Ask for the webhook URL
    check_for_huge(webhook_url)
