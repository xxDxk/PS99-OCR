# Hatch Detection Script

This is a Python script designed to monitor real-time **Pet Hatch** events in PS99, capture screenshots, and send notifications to a Discord channel using webhooks. It uses **OCR (Optical Character Recognition)** to detect the word **"Huge"** in the screenshots and sends a notification along with the image to a Discord server.

![ocr example](https://github.com/user-attachments/assets/4656955a-c5db-40f7-9f7e-3c36d74283db)

*image is an example of the embed and functionality*

*please ensure you close chat and do not have the word "Huge" anywhere on your screen when you start the program*

*OCR relies on imaage clarity, so if your device runs lower graphics, there is a chance it may not work*

*i am currently training an OCR model specifically for the PS99 font, until then there may be the occasional hatch that isn't caught by the program*

### Features:
- **Real-time monitoring**: Continuously watches for pet hatches in PS99. (every 5 sec)
- **OCR processing**: Detects the word "Huge" using image processing and OCR.
- **Discord Integration**: Sends notifications to a Discord channel, with a screenshot attached, whenever a huge hatch occurs.
- **Customizable**: Easily change the Discord role or user mentioned in the notification.

### Requirements:

**DOWNLOAD AND ADD TO SYSTEM PATH**: https://github.com/tesseract-ocr/tesseract / Direct Download: ([Latest](https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe))

To run the script, you'll need the following Python libraries:
- Pillow
- pytesseract
- requests
- opencv-python
- numpy

You can install these dependencies using the following command:
```bash
pip install Pillow pytesseract requests opencv-python numpy
