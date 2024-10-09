FROM python:3.12.6

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader punkt_tab

# Install Tesseract OCR with Polish language support
RUN apt-get update && apt-get install -y tesseract-ocr
RUN apt-get install -y tesseract-ocr-pol

# Set the TESSDATA_PREFIX environment variable
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/

# Download Polish language data
RUN mkdir -p /usr/share/tesseract-ocr/4.00/tessdata/ && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/pol.traineddata -P /usr/share/tesseract-ocr/4.00/tessdata/

COPY ./app /code/app

# Use uvicorn to run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
