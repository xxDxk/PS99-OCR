from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import random
import string
import time
import requests
import json
import os

# Function to generate a random username
def generate_username():
    words = ["shadow", "phoenix", "blaze", "nova", "vortex", "echo", "frost", "ember", "storm", "nebula",
             "quantum", "chaos", "zenith", "lunar", "solar", "cosmic", "galaxy", "orbit", "pulse", "flare",
             "crimson", "azure", "onyx", "jade", "amber", "ruby", "sapphire", "emerald", "diamond", "pearl",
             "obsidian", "quartz", "topaz", "opal", "crystal", "silver", "gold", "platinum", "titanium", "iron",
             "steel", "bronze", "copper", "brass", "mercury", "neon", "argon", "krypton", "xenon", "radon"]
    word1 = random.choice(words)
    word2 = random.choice(words)
    numbers = ''.join(random.choices(string.digits, k=3))
    return f"{word1}{word2}{numbers}"

# Function to generate a random password
def generate_password():
    chars = string.ascii_letters + string.digits
    password = ''.join(random.choices(chars, k=10))
    return f"{password[0].upper()}{password[1:]}{'!'}"

# Function to save credentials and cookie to a text file
def save_to_file(username, password, cookie):
    with open("accounts.txt", "w") as file:
        file.write(f"{username}:{password}:{cookie}\n")

# Function to send a Discord webhook alert with a screenshot
def send_webhook(webhook_url, username, password, screenshot_path=None):
    # Create the embed
    embed = {
        "title": "Verification Needed!",
        "description": f"Verification needed for:\n\n> Username: ||{username}||\n> Password: ||{password}||",
        "footer": {"text": "made by jajts"}
    }

    # Add screenshot to the embed if provided
    if screenshot_path:
        embed["image"] = {"url": "attachment://screenshot.png"}

    # Prepare the payload
    payload = {
        "embeds": [embed]
    }

    # Send the webhook with or without the screenshot
    if screenshot_path:
        with open(screenshot_path, "rb") as file:
            screenshot_data = file.read()
        files = {
            "file": ("screenshot.png", screenshot_data)
        }
        requests.post(webhook_url, data={"payload_json": json.dumps(payload)}, files=files)
    else:
        requests.post(webhook_url, data=json.dumps(payload), headers={"Content-Type": "application/json"})

# Main script
def create_roblox_account():
    # Ask for webhook URL
    webhook_url = input("Enter your Discord webhook URL: ")

    # Initialize the WebDriver using WebDriver Manager
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    # Open the Roblox signup page
    driver.get("https://www.roblox.com/signup")

    # Wait for the page to load
    time.sleep(5)

    # Select random month, day, and year
    month_dropdown = Select(driver.find_element(By.ID, "MonthDropdown"))
    month_dropdown.select_by_index(random.randint(1, 12))

    day_dropdown = Select(driver.find_element(By.ID, "DayDropdown"))
    day_dropdown.select_by_index(random.randint(1, 31))

    year_dropdown = Select(driver.find_element(By.ID, "YearDropdown"))
    year_dropdown.select_by_index(random.randint(1, len(year_dropdown.options) - 1))

    # Generate username and password
    username = generate_username()
    password = generate_password()

    # Enter username and check for errors
    username_input = driver.find_element(By.ID, "signup-username")
    username_input.send_keys(username)

    # Wait for validation (adjust timing as needed)
    time.sleep(2)

    # Check for "has-error" or "has-success"
    validation_div = driver.find_element(By.CSS_SELECTOR, "div.form-group")
    if "has-error" in validation_div.get_attribute("class"):
        print(f"Username '{username}' is taken. Generating a new one...")
        username = generate_username()
        username_input.clear()
        username_input.send_keys(username)
    else:
        print(f"Username '{username}' is available!")

    # Enter password
    password_input = driver.find_element(By.ID, "signup-password")
    password_input.send_keys(password)

    # Click the signup button
    signup_button = driver.find_element(By.ID, "signup-button")
    signup_button.click()

    # Wait for a redirect to https://www.roblox.com/home
    print("Waiting for redirect to https://www.roblox.com/home...")
    webhook_sent = False  # Track if the webhook has been sent
    while True:
        if driver.current_url == "https://www.roblox.com/home":
            print("Redirect to /home occurred. Account creation successful.")
            break

        # Check every 5 seconds
        time.sleep(5)

        # If no redirect after 5 seconds and webhook hasn't been sent, send the webhook
        if not webhook_sent:
            print("No redirect to /home occurred within 5 seconds. Sending webhook...")

            # Capture screenshot
            screenshot_path = os.path.abspath("verification_challenge.png")
            driver.save_screenshot(screenshot_path)

            # Send webhook with screenshot
            send_webhook(webhook_url, username, password, screenshot_path)

            # Clean up the screenshot file
            try:
                os.remove(screenshot_path)
            except Exception as e:
                print(f"Failed to delete screenshot: {e}")

            webhook_sent = True  # Mark the webhook as sent

    # Get the .ROBLOSECURITY cookie
    cookie = driver.get_cookie(".ROBLOSECURITY")
    if cookie:
        roblosecurity_cookie = cookie["value"]
    else:
        roblosecurity_cookie = "COOKIE_NOT_FOUND"

    # Save credentials and cookie to a text file
    save_to_file(username, password, roblosecurity_cookie)

    # Close the browser
    driver.quit()

# Run the script
create_roblox_account()
