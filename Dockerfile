# Use an official Python runtime as a parent image
FROM python:3.12-bookworm

# Set the working directory in the container
WORKDIR /app

COPY requirements.frozen /app/requirements.frozen

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.frozen

RUN playwright install --with-deps

# Copy the current directory contents into the container at /app
COPY . /app

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app/run.py"]
