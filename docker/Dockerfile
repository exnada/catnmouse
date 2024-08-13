ARG OWNER=exnada
ARG BASE_CONTAINER=debian:11.10-slim # seems last version that works without needing venv
# ARG BASE_CONTAINER=python:3.12.2-slim # seems last version that works without needing venv

FROM $BASE_CONTAINER
LABEL maintainer="ExNada Inc. <info@exnada.com>"

ARG EXNADA_USER="exnada"
ARG EXNADA_UID="1000"
ARG EXNADA_GID="100"

ARG APT_GET_PACKAGES="packages.txt"
ARG PYTHON_REQUIREMENTS="requirements.txt"

USER root
COPY ${APT_GET_PACKAGES} /tmp/
RUN apt-get update && \
    xargs -a /tmp/${APT_GET_PACKAGES} apt-get install -y && \
    rm -rf /var/lib/apt/lists/* 

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

COPY ${PYTHON_REQUIREMENTS} /tmp/
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r /tmp/${PYTHON_REQUIREMENTS} && \
    rm -f /tmp/${PYTHON_REQUIREMENTS}

# Next two lines are not needed if using python image:
RUN rm -rf /var/lib/apt/lists/* && \
    ln -s /usr/bin/python3 /usr/local/bin/python

RUN useradd -l -m -s /bin/bash -N -u "${EXNADA_UID}" -g ${EXNADA_GID} "${EXNADA_USER}" && \
    chmod g+w /etc/passwd
 
USER ${EXNADA_USER}
ENV HOME="/home/${EXNADA_USER}"
WORKDIR ${HOME}

CMD ["echo", "hello"]
