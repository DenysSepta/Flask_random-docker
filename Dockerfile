FROM ubuntu:latest

USER root

RUN echo "locales locales/locales_to_be_generated multiselect en_US.UTF-8 UTF-8" | debconf-set-selections \
    && echo "locales locales/default_environment_locale select en_US.UTF-8" | debconf-set-selections \
    && apt-get update \
    && apt-get --yes --no-install-recommends install \
        locales tzdata ca-certificates sudo \
        bash-completion iproute2 tar unzip curl rsync vim nano tree \
    && rm -rf /var/lib/apt/lists/*
ENV LANG en_US.UTF-8


RUN apt-get update \
    && apt-get --yes --no-install-recommends install \
        python3 python3-dev \
        python3-pip python3-venv python3-wheel python3-setuptools 
ADD requirements.txt /tmp/requirements.txt


WORKDIR /app

COPY . /app 

RUN pip3 install --no-cache-dir -r requirements.txt 


EXPOSE 5000

ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]


