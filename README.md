# Nude Detection - Web Version

## Overview

This project is a Flask-based web application designed to detect inappropriate content (nudity) in images. Users can upload images or provide URLs to images, and the application will analyze and determine whether the content is inappropriate. If the content is flagged as inappropriate, the image will be censored, and both appropriate and censored images will be displayed with clear visual feedback.

## Features

- **Image Upload and URL Detection**: Users can upload images directly from their local device or input an image URL for analysis.
- **Nudity Detection**: The application detects inappropriate content (nudity) in images using a custom image detection model.
- **Automatic Image Censorship**: In cases of inappropriate content, the image is automatically censored.
- **Visual Feedback**: The results page provides visual cues:
  - Green border for appropriate content.
  - Red border for inappropriate content.
- **Temporary File Storage**: Uploaded and processed images are stored temporarily.
- **Automated Cleanup**: Uploaded and censored images are automatically deleted after 5 minutes to ensure no data retention.

## Folder Structure

- **`/static/uploads`**: Stores the original images uploaded by users.
- **`/static/censored`**: Stores censored versions of images flagged as inappropriate.
- **`/templates`**: HTML templates for the user interface, including the main form for uploads and the results page.

## How It Works

1. **User Uploads Image or Enters URL**: The user uploads an image file or provides an image URL on the main page.
2. **Nudity Detection**: The application processes the image using a nudity detection model.
3. **Result Display**: The result is shown on a new page with visual indicators:
   - **Green border** for images with no inappropriate content.
   - **Red border** for images flagged as inappropriate (along with a censored version of the image).
4. **File Cleanup**: Uploaded and censored images are automatically deleted after 5 minutes to maintain privacy and avoid unnecessary storage.

## System Requirements

- **Python 3.x**
- **Flask**: A lightweight Python web framework.
- Additional dependencies (e.g., image processing libraries) as specified in the `requirements.txt`.

## License

This project is licensed under the MIT License.
