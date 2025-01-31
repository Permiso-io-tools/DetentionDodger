FROM python:3.10

WORKDIR /detentiondodger
COPY . .

ADD ./output /detentiondodger/output
ADD ./scenarios /detentiondodger/scenarios

RUN apt update && apt install python3-pip less -y
RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["python3", "detentiondodger.py"]
