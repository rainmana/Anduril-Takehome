# Use Python 3.11.6 on Alpine Linux
FROM python:3.11.6-alpine3.18

# Set the workng directory 
WORKDIR /alec-anduril-app

# Copy the current directory contents into the container at /alec-anduril-app for ./app
COPY ./app /alec-anduril-app

# Install any needed packages specified in requirements.txt by copying it to WORKDIR and runing pip
COPY requirements.txt /alec-anduril-app/
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80 to the world outside of the container
EXPOSE 80

# Run main.py when the container launches via uvicorn since we're using FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
