FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# DON'T run expensive training during image build.
# Instead, have the container load a pre-trained model at runtime or
# download a model artifact from S3 inside your app startup if needed.

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
