FROM ubuntu:18.04

ENV USER_ID            1000
ENV GROUP_ID           985
ENV USER_GROUP_NAME    fia

RUN apt-get update && apt-get install -y \
    python \
    python3 \
    python3-venv \
    python-pip \
    poppler-utils \
    python-poppler \
    libpoppler-cpp-dev \
    vim \
    sudo

RUN ln -fs /ust/share/zoneinfo/Asia/Novosibirsk /etc/localtime

RUN groupadd -g $GROUP_ID $USER_GROUP_NAME
RUN useradd -u $USER_ID -g $GROUP_ID -m $USER_GROUP_NAME

RUN mkdir -p /home/fia/pyvenv
RUN python3 -m venv /home/fia/pyvenv
RUN /home/fia/pyvenv/bin/python3 -m pip install --upgrade pip
RUN /home/fia/pyvenv/bin/pip3 install schedule
RUN /home/fia/pyvenv/bin/pip3 install beautifulsoup4
RUN /home/fia/pyvenv/bin/pip3 install pdf2image
RUN /home/fia/pyvenv/bin/pip3 install requests

RUN mkdir -p /home/fia/fia
RUN chown -R $USER_GROUP_NAME:$USER_GROUP_NAME /home/fia/fia
RUN chmod -R 777 /home/fia/fia

