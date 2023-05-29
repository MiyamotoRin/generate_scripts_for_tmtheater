# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Add your application to the container
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install pipenv && \
    pipenv install && \
    pipenv shell

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "app.py"]
