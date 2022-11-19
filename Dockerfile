FROM python:3.8
WORKDIR /Users/adamstolarczyk/Downloads/apk_slowka
COPY . .
COPY ./dictionary.xlsx .
RUN pip3 install pandas
RUN pip3 install numpy
RUN pip3 install requests
RUN pip3 install openpyxl


CMD ["python", "apka.py"]