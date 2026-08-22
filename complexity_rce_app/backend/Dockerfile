FROM python:3.12-slim

WORKDIR /app

#Only copying the requirements is faster for changes
#Requirements.txt is generated via: pip freeze > requirements.txt
COPY requirements.txt .
#This might be cumbersom to install docker for the subprocesses but using Docker SDK instead would make injecting into stdin significantly more fragile 
RUN apt-get update && apt-get install -y docker.io 
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]