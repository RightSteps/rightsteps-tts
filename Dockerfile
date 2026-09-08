FROM python:3.11-slim

RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

# Install piper
WORKDIR /opt
RUN wget -q https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz \
    && tar -xzf piper_linux_x86_64.tar.gz \
    && rm piper_linux_x86_64.tar.gz

# Download voice model
RUN mkdir -p /opt/piper/models \
    && wget -q -O /opt/piper/models/en_GB-cori-medium.onnx \
        "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/cori/medium/en_GB-cori-medium.onnx" \
    && wget -q -O /opt/piper/models/en_GB-cori-medium.onnx.json \
        "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/cori/medium/en_GB-cori-medium.onnx.json"

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml .
RUN uv sync --frozen --no-dev

COPY app/ ./app/

ENV PIPER_BINARY=/opt/piper/piper
ENV PIPER_MODEL=/opt/piper/models/en_GB-cori-medium.onnx

EXPOSE 8080

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
