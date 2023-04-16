FROM jupyter/datascience-notebook:python-3.10

RUN python --version

USER root

ARG DEBIAN_FRONTEND=noninteractive

COPY ./ .

RUN pip install -e .

RUN apt-get update && \
        apt-get install -y \
        make \
        curl \
        vim \
        jq \
        autoconf \
        automake \
        libtool \
        pkg-config \
        python3-pip \
        ssh-client \
        binutils \
        libproj-dev \
        gdal-bin

ADD env/jupyter/fonts /usr/share/fonts/truetype/

RUN fc-cache
RUN fc-list

RUN jupyter contrib nbextension install --sys-prefix
RUN jupyter nbextension install --py --sys-prefix keplergl
RUN jupyter nbextension enable --py --sys-prefix keplergl

USER root

VOLUME /notebooks
WORKDIR /notebooks
