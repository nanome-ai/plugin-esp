FROM nanome/plugin-env

ENV ARGS=''
WORKDIR /app

ADD APBS-3.4.1.Linux.zip /app
RUN unzip APBS-3.4.1.Linux.zip

ENV APBS='/app/apbs/bin/apbs'
ENV PDB2PQR='pdb2pqr30'

ARG CACHEBUST
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN rm apbs-pdb2pqr.tgz

CMD python run.py ${ARGS}
