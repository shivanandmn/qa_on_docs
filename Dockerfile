# Use a Python base image
FROM python:3.10

# Set environment variables
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Create and set the working directory
WORKDIR /qa_on_docs

# Copy your Flask app code into the container
COPY . .

# Install Flask and other dependencies
RUN pip install --no-cache-dir -r requirements.txt 

# # Copy your ML code into the container
# COPY ml/ /ml

# Expose the port on which your Flask app will run (typically 5000)
EXPOSE 5000

# Command to run the Flask app with ML prediction
CMD ["flask", "run"]
