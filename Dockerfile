FROM python:3.8.3

ENV HOME /root
WORKDIR /root

COPY . .
RUN pip install -r requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

# Run the app
CMD /wait && python server.py