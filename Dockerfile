#Step 1 : Use an official Python runtime as the Base Image
FROM python:3.9-slim

# Set environment variables to prevent Python from writing .pyc files and buffer outputs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Step 2 : Set the working directory inside the container
WORKDIR /app

# Step 3 : Copy the current directory contents into the container
COPY . /app

# Step 4 : Install the dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Step 5 : Expose port 8000 to communicate with the outside world
EXPOSE 8000

# Step 6: Define the command to run the fastapi app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 

# Build de l'image
# docker build -t loan-image .
# -t loan-image : attribue le nom loan-image à l'image docker
# . pour indiquer où se trouve le dockerfile

# Run de l'image dans un container
# docker run --name loan_container -d -p 8000:8000 loan-image 
# -d pour run en background (mode detaché)
# -p pour mapper le port 8000 en local et le port 8000 du container
# loan-image: le nom de l'image