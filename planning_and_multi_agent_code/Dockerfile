# Use an official Python runtime as a base image
FROM python:3.11

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN apt-get update && apt-get install -y git
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install -e git+https://github.com/saumya06/crewAI_nlsql.git@nlsql#egg=crewai
RUN pip install crewai[tools] 
# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable to run the server on all network interfaces
ENV HOST 0.0.0.0

# Run the application command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]