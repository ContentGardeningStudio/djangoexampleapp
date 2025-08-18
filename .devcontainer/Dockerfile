# Base on slim Python
FROM python:3.12-slim

# System deps
RUN apt-get update && apt-get install -y \
    curl git build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv via official script
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add both possible install locations to PATH
ENV PATH="/root/.local/bin:/root/.cargo/bin:$PATH"

# Verify installation
RUN uv --version

# Set workdir
WORKDIR /workspace

# (Optional) Pre-create venv
RUN uv venv

# Default shell
CMD [ "bash" ]
