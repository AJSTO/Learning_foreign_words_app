FROM python:3.8
COPY . .
RUN pip3 install -r requirements
ENV API_KEY=

CMD ["python", "apk.py"]
