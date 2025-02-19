FROM python:3.12-slim-bookworm

# Set the working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install system dependencies required for pyodbc and the Microsoft ODBC driver
RUN apt-get update && apt-get install -y \
    gcc \
    unixodbc \
    unixodbc-dev \
    curl \
    gnupg \
    apt-transport-https \
    && rm -rf /var/lib/apt/lists/*

# Add Microsoft's GPG key and configure the Microsoft package repository for Debian 12 (Bookworm)
# Required to install msodbcsql17
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Install uv and use it to install dependencies
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH and install dependencies
ENV PATH="/root/.local/bin:$PATH"
COPY pyproject.toml /usr/src/app/
RUN uv pip sync --system pyproject.toml

# Copy the source code
COPY . /usr/src/app

# Expose Streamlit port
EXPOSE 80

ENTRYPOINT ["streamlit", "run"]
CMD ["chatbot.py"]
