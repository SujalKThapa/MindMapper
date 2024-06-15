FROM mcr.microsoft.com/azure-functions/python:4-python3.11

# Install system dependencies
RUN apt-get update && apt-get install -y graphviz

# Copy the function app code
COPY . /home/site/wwwroot

# Install python dependencies
RUN pip install -r /home/site/wwwroot/requirements.txt

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
