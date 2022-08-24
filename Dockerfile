# Initialize the application...
FROM python:latest

RUN pip install -r requirements.txt

# Bla bla.

CMD ["python" "server.py" "run" "--pro"]