# Simple API OCR ML Application

This is a proof-of-concept (PoC) for a simple machine learning API application.
The primary functionality is to perform OCR (Optical Character Recognition)
on images using Tesseract with Polish language support. Additionally,
it includes a basic endpoint for predicting invoice payment status from text.

## Prerequisites

Before running the application, ensure you have the following installed:

- Docker version 20.10.7 or later
- Python 3.8 or later (if testing outside Docker)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/username/repo.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd repo
   ```

3. **Build the Docker image:**

   ```bash
   docker build -t ml_app_api_image .
   ```

4. **Run the Docker container:**

   ```bash
   docker run -d --name ml_app_api_container -p 80:80 ml_app_api_image
   ```

## Usage

### Access the Health Check Endpoint

- Ensure the application is running and check its health status:

  ```bash
  curl -X GET http://0.0.0.0:80/
  ```

Example response:
```json
{
  "health_check": "OK"
}
```

### Perform OCR on an Image

- Use the `/ocr_image` endpoint to perform OCR on an image file via URL:

  **Using `curl` in Terminal:**

  ```bash
  curl -X GET 'http://0.0.0.0:80/ocr_image?image_url=https://i.ibb.co/vw3M7Xz/mikolaj-tomczak-faktura-paliwo.png' -H 'Content-Type: application/json'
  ```

  **Using Python `requests`:**

  ```python
  import requests

  image_url = 'https://i.ibb.co/vw3M7Xz/mikolaj-tomczak-faktura-paliwo.png'
  url = 'http://0.0.0.0:80/ocr_image'

  params = {'image_url': image_url}
  response = requests.get(url, params=params)

  print(response.json())
  ```

Example response:
```json
{
  "ocr_raw_text": "Your OCR result from the image"
}
```

### Predict Invoice Payment Status

- Use the `/predict` endpoint with an invoice text to predict payment status:

  ```bash
  curl -X GET "http://0.0.0.0:80/predict?invoice_raw_text=Sample Text"
  ```

Example response:
```json
{
  "prediction": "Predicted Status"
}
```

