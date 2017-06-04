#wxrobot
FROM python:3
RUN mkdir -p /usr/src/app
RUN mkdir -p /usr/src/app/saved
WORKDIR /usr/src/app
ONBUILD COPY requirements.txt /usr/src/app/
ONBUILD RUN pip install --no-cache-dir -r requirements.txt
ONBUILD COPY . /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY weixin.py /usr/src/app/
COPY wxrobot.py /usr/src/app/
COPY wxmgt.py /usr/src/app/
COPY wxdb.py /usr/src/app/
CMD ["python", "/usr/src/app/wxmgt.py"]
