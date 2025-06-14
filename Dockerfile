FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN bash setup.sh
CMD ["python", "train.py", "--fast", "--seed", "0"]

