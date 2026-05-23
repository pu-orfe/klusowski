FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir beautifulsoup4 requests pytest

COPY mirror.py test_mirror.py ./

CMD ["pytest", "-v", "test_mirror.py"]
