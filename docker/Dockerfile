FROM continuumio/miniconda3

ENV ARGS=''

WORKDIR /app

COPY apbs-pdb2pqr.tgz .
RUN tar xf apbs-pdb2pqr.tgz &&\
  echo "/app/apbs/lib" >> /etc/ld.so.conf.d/local.conf &&\
  ln -s /app/pdb2pqr/libreadline.so.6 /app/apbs/lib &&\
  ln -s /app/pdb2pqr/libtinfo.so.5 /app/apbs/lib &&\
  ldconfig

ENV APBS='/app/apbs/bin/apbs'
ENV PDB2PQR='/app/pdb2pqr/pdb2pqr'

ARG CACHEBUST
RUN pip install nanome

COPY . .

CMD python run.py ${ARGS}
