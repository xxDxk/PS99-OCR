# Hatch Detection Script

This is a Python script designed to monitor real-time **Pet Hatch** events in PS99, capture screenshots, and send notifications to a Discord channel using webhooks. It uses **OCR (Optical Character Recognition)** to detect the word **"Huge"** in the screenshots and sends a notification along with the image to a Discord server.

### Features:
- **Real-time monitoring**: Continuously watches for pet hatches in PS99. (every 5 sec)
- **OCR processing**: Detects the word "Huge" using image processing and OCR.
- **Discord Integration**: Sends notifications to a Discord channel, with a screenshot attached, whenever a huge hatch occurs.
- **Customizable**: Easily change the Discord role or user mentioned in the notification.

### Requirements:

**DOWNLOAD AND ADD TO SYSTEM PATH**: https://github.com/tesseract-ocr/tesseract ([Latest](https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe))

To run the script, you'll need the following Python libraries:
- Pillow
- pytesseract
- requests
- opencv-python
- numpy

You can install these dependencies using the following command:
```bash
pip install Pillow pytesseract requests opencv-python numpy
