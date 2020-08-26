
FROM python:3.8-slim
COPY . /slice/deploy
COPY  . /requirements.txt/slice/deploy
WORKDIR /slice/deploy
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT [ "python" ]
CMD ["main.py"]

