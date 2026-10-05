FROM python:latest

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY calendarsolver.py /app/calendarsolver.py

ENTRYPOINT ["python", "/app/calendarsolver.py"]
