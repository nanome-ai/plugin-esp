FROM nanome/plugin-env

ENV ARGS=''
WORKDIR /app

ADD apbs-pdb2pqr.tgz .
RUN echo "/app/apbs/lib" >> /etc/ld.so.conf.d/local.conf &&\
  ln -s /app/pdb2pqr/libreadline.so.6 /app/apbs/lib &&\
  ln -s /app/pdb2pqr/libtinfo.so.5 /app/apbs/lib &&\
  ldconfig

ENV APBS='/app/apbs/bin/apbs'
ENV PDB2PQR='/app/pdb2pqr/pdb2pqr'

ARG CACHEBUST
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN rm apbs-pdb2pqr.tgz

CMD python run.py ${ARGS}
