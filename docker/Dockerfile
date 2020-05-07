FROM continuumio/miniconda3

ENV ARGS=''

WORKDIR /app

RUN apt-get install -y curl &&\
  curl -Lf https://github.com/Electrostatics/apbs-pdb2pqr/releases/download/apbs-1.5/apbs-1.5-GCC4.8.tar.gz -o apbs.tar.gz &&\
  curl -Lf https://github.com/Electrostatics/apbs-pdb2pqr/releases/download/pdb2pqr-2.1.1_release/pdb2pqr-linux-bin64-2.1.1.tar.gz -o pdb2pqr.tar.gz &&\
  mkdir apbs && tar xf apbs.tar.gz -C /app/apbs &&\
  tar xf pdb2pqr.tar.gz && mv pdb2pqr-linux-bin64-2.1.1 pdb2pqr &&\
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
