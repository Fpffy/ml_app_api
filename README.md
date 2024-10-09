# Simple ML API Application (PoC)

This is a proof-of-concept (PoC) for a simple machine learning API application. The primary functionality is to perform OCR (Optical Character Recognition) on images using Tesseract with Polish language support. Additionally, it includes a basic endpoint for predicting invoice payment status from text.

## Prerequisites

Before running the application, ensure you have the following installed:

- Docker version 20.10.7 or later

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

### Predict Invoice Payment Status

- Use the `/predict` endpoint with an invoice text to predict payment status:

  ```bash
  curl -X GET "http://0.0.0.0:80/predict?invoice_raw_text=Sample Text"
  ```

## Deploying on AWS ECS using Docker Hub

### Pushing the Docker Image to Docker Hub

1. **Create a repository on Docker Hub**. Below is a sample image of creating a Docker Hub repository:

   ![Zrzut ekranu 2024-10-9 o 09 17 17](https://github.com/user-attachments/assets/868439bd-e5c9-416b-a891-ea4c3c2514c4)

2. **Tag the Docker image:**

   ```bash
   docker tag ml_app_api_image username/ml-app-api-demo
   ```

3. **Push the image to your Docker Hub repository:**

   ```bash
   docker push username/ml-app-api-demo
   ```

### Running the Docker Image on AWS ECS

To deploy the Docker image on AWS ECS:

1. **Log in to your AWS Console** and navigate to the ECS (Elastic Container Service).

2. **Create a new ECS Cluster** or choose an existing one.
   ![image](https://github.com/user-attachments/assets/11609b6d-815b-4bd2-986d-6802e11ee171)


3. **Define a Task Definition**, specifying the Docker image from Docker Hub (`username/ml-app-api-demo`).
   ![image](https://github.com/user-attachments/assets/597dfc00-8942-4602-bfa3-051531483c6c)


4. **Create a Service** using the Task Definition to run and manage the application on ECS.
  ![image](https://github.com/user-attachments/assets/2ff143cd-336c-4cb1-b24a-4e6a38afa444)

5. **Update the Security Group** to allow incoming traffic on the necessary ports (e.g. port 80).
   ![image](https://github.com/user-attachments/assets/4908f648-69fb-430f-9a7c-184e5eaaf83f)

6. Once the service is running, find the public IP or DNS to access your application.
   ![image](https://github.com/user-attachments/assets/83a4281c-d29b-4f1b-9ed9-93ddc7dbb50a)

