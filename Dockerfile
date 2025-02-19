# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app/src

# Copy dependency file
COPY requirements.txt /app/src/requirements.txt

# Copy application files (fixing the issue)
COPY src/ /app/src/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your application runs on
EXPOSE 8080

# Command to run the application (update to match your file)
CMD ["python", "app.service.py"]
