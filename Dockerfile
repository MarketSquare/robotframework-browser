FROM python:3.8-buster AS BrowserBase
RUN mkdir /app
WORKDIR /app
RUN \
    echo "deb https://deb.nodesource.com/node_12.x buster main" > /etc/apt/sources.list.d/nodesource.list && \
    wget -qO- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
    apt-get update && \
    apt-get install -yqq nodejs && \
    pip install -U pip && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

FROM BrowserBase AS BrowserBuilder
WORKDIR /app
RUN \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list && \
    wget -qO- https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    apt-get update && \
    apt-get install -yqq yarn && \
    pip install pipenv && \
    rm -rf /var/lib/apt/lists/*
COPY dev-requirements.txt /app/dev-requirements.txt
RUN pip install -r dev-requirements.txt
COPY package.json /app/package.json
COPY yarn.lock /app/yarn.lock
RUN yarn install
COPY . /app
RUN \
    make build && \
    rm -rf dist/ && \
	cp package.json Browser/wrapper && \
	python setup.py sdist bdist_wheel

FROM BrowserBase
WORKDIR /app
COPY --from=BrowserBuilder /app/dist /app/dist
RUN pip install dist/robotframework_browser-*-py3-none-any.whl
RUN rfbrowser init