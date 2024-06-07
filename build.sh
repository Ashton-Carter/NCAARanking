#!/bin/sh
# Build the Docker image
docker build -t my-streamlit-app .

# Run the Docker container
docker run -d -p 8501:8501 my-streamlit-app

# Generate a simple HTML file that redirects to the Streamlit app
echo "<meta http-equiv=\"refresh\" content=\"0; url=http://localhost:8501/\">" > public/index.html
