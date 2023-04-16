FROM ghcr.io/cloudnative-pg/postgis:14

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    wget make gcc libtool unzip pgxnclient libpq-dev postgresql-server-dev-14

RUN apt-get update \
    && apt-get -y install build-essential \
    && apt-get install -y wget \
    && rm -rf /var/lib/apt/lists/* \
    && wget https://github.com/Kitware/CMake/releases/download/v3.24.1/cmake-3.24.1-Linux-x86_64.sh \
    -q -O /tmp/cmake-install.sh \
    && chmod u+x /tmp/cmake-install.sh \
    && mkdir /opt/cmake-3.24.1 \
    && /tmp/cmake-install.sh --skip-license --prefix=/opt/cmake-3.24.1 \
    && rm /tmp/cmake-install.sh \
    && ln -s /opt/cmake-3.24.1/bin/* /usr/local/bin

RUN apt-get update \
    && apt-get install -y lsb-release wget \
    && echo "deb https://packagecloud.io/timescale/timescaledb/debian/ $(lsb_release -c -s) main" | tee /etc/apt/sources.list.d/timescaledb.list \
    && wget --quiet -O - https://packagecloud.io/timescale/timescaledb/gpgkey | apt-key add - \
    && apt-get update \
    && apt-get install -y "timescaledb-2-postgresql-${PG_MAJOR}" \
    && apt-get remove -y lsb-release wget \
    && 	rm -fr /tmp/* \
    && 	rm -rf /var/lib/apt/lists/*

RUN pgxn install h3