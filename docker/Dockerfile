# Use the official Python image from the Docker Hub
FROM --platform=linux/amd64 python:3.9

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential libpoppler-cpp-dev pkg-config python3

# Download and install pdftotext from Xpdf tools
RUN wget --no-check-certificate https://dl.xpdfreader.com/xpdf-tools-linux-4.05.tar.gz && \
    tar -xvf xpdf-tools-linux-4.05.tar.gz && \
    cp xpdf-tools-linux-4.05/bin64/pdftotext /usr/local/bin

# Clean up
RUN rm -rf xpdf-tools-linux-4.05.tar.gz xpdf-tools-linux-4.05

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8501

# Run the Streamlit app
ENTRYPOINT [ "streamlit", "run" ]
CMD [ "app.py", "--server.headless", "true", "--server.fileWatcherType", "none", "--browser.gatherUsageStats", "false"]
