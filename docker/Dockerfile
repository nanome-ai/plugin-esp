FROM nanome/plugin-env

ENV ARGS=''
WORKDIR /app

RUN apt-get update && apt-get install -y unzip
ADD APBS-3.4.1.Linux.zip /app
RUN unzip APBS-3.4.1.Linux.zip

ENV APBS='/app/APBS-3.4.1.Linux/bin/apbs'
ENV PDB2PQR='pdb2pqr30'

RUN chmod +x $APBS
ARG CACHEBUST
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD python run.py ${ARGS}
