FROM python:3.8
COPY . .
RUN pip3 install -r requirements


CMD ["python", "apk.py"]
