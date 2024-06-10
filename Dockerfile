# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for dlib
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-python-dev \
    libboost-thread-dev \
    pulseaudio \
    alsa-utils \
    python3-dev \
    python3-pip \
    gcc \
    libportaudio2 \
    libportaudiocpp0 \
    portaudio19-dev xvfb && \
    apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the dlib wheel file into the container# Set the display environment variable
ENV DISPLAY=:99

# Install dlib from the local wheel file
RUN pip install dlib


# Install any needed packages specified in requirements.txt, excluding dlib
RUN grep -v dlib req.txt > requirements_no_dlib.txt && \
    pip install -r requirements_no_dlib.txt
# Make port 5005 available to the world outside this container
EXPOSE 5005

# Run chatbot5.py when the container launches
CMD ["python", "FaceRec/PlayWithDatas/chatbot5.py"]
