FROM python:3.10

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./app /app

COPY kaggle.json /root/.kaggle/kaggle.json

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]