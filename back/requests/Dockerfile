FROM ubuntu:latest

RUN apt update && apt upgrade -y && apt install python3 -y && apt install nmap -y && apt install python3-pip -y && apt install git -y && apt-get install libmysqlclient-dev -y && apt autoremove -y

RUN git clone https://github.com/jgomezb11/CarpetaCiudadana.git

WORKDIR /CarpetaCiudadana/back

RUN pip3 install -r requirements.txt

WORKDIR /requests

CMD python3 run.py