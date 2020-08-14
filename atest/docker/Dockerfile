FROM python:3.8-buster AS BrowserBuilder
RUN mkdir /app
WORKDIR /app
RUN \
    echo "deb https://deb.nodesource.com/node_12.x buster main" > /etc/apt/sources.list.d/nodesource.list && \
    wget -qO- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
    apt-get update && \
    apt-get install -yqq nodejs && \
    pip install -U pip && \
    rm -rf /var/lib/apt/lists/*
COPY Browser/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY Browser/dev-requirements.txt /app/dev-requirements.txt
RUN pip install -r dev-requirements.txt

RUN \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list && \
    wget -qO- https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    apt-get update && \
    apt-get install -yqq yarn && \
    rm -rf /var/lib/apt/lists/*
COPY package.json /app/package.json
COPY yarn.lock /app/yarn.lock
RUN yarn install

COPY . /app
RUN make package

FROM playwright-focal AS CleanInstallTester
# Add pip
USER root
RUN apt-get update
RUN apt-get install -y python3-pip python-invoke
USER pwuser

# Install pabot to support atest
RUN pip3 install --user robotframework-pabot

WORKDIR /app
COPY --from=BrowserBuilder /app/dist /app/dist
RUN pip3 install --user dist/robotframework_browser-*-py3-none-any.whl
# Hard to update PATH for all shells in a docker image so we run python scripts with manual paths
RUN ~/.local/bin/rfbrowser init

# What were these used for previously
# RUN mv /root/.cache/ /home/pwuser/.cache
# RUN chmod a+rwx -R /home/pwuser/.cache
ENV NODE_PATH=/usr/lib/node_modules
