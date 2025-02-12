FROM python:3.11-slim-bookworm

# Set the working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install requirements
RUN pip3 install --upgrade pip
COPY requirements.txt /usr/src/app/
RUN pip3 install -r requirements.txt

# Copy the source code
COPY . /usr/src/app

# Expose default streamlit port
EXPOSE 80

ENTRYPOINT ["streamlit", "run"]
CMD ["Chatbot.py"]
