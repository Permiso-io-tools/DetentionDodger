FROM python:3.10

WORKDIR /detectiondodger
COPY . .

ADD ./output /detectiondodger/output
ADD ./scenarios /detectiondodger/scenarios

RUN apt update && apt install python3-pip -y
RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["python3", "detectiondodger.py"]
