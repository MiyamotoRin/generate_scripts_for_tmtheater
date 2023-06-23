# Use an official Python runtime as a parent image
FROM python:3.9.12-slim-buster

# Set the working directory in the container
WORKDIR /app

# Add your application to the container
ADD . /app

# Install any needed packages specified in Pipfile
RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install 

# Install Voicevox Core Dependencies
RUN apt-get update && \
    apt-get install -y wget unzip

# Install Voicevox Core 
RUN wget https://github.com/VOICEVOX/voicevox_core/releases/download/0.14.4/voicevox_core-linux-x64-cpu-0.14.4.zip \
    && unzip voicevox_core-linux-x64-cpu-0.14.4.zip \
    && rm voicevox_core-linux-x64-cpu-0.14.4.zip

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
# CMD ["pipenv", "run", "python", "app.py"]
