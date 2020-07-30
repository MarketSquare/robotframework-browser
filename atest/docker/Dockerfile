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
COPY Browser/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

FROM BrowserBase AS BrowserBuilder
RUN \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list && \
    wget -qO- https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    apt-get update && \
    apt-get install -yqq yarn && \
    pip install pipenv && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . /app
RUN pip install -r Browser/dev-requirements.txt
RUN yarn install
RUN make package

FROM BrowserBase AS CleanInstallTester
WORKDIR /app
# Install WebKit dependencies
RUN apt-get update && apt-get install -y libwoff1 \
                                         libopus0 \
                                         libwebp6 \
                                         libwebpdemux2 \
                                         libenchant1c2a \
                                         libgudev-1.0-0 \
                                         libsecret-1-0 \
                                         libhyphen0 \
                                         libgdk-pixbuf2.0-0 \
                                         libegl1 \
                                         libnotify4 \
                                         libxslt1.1 \
                                         libevent-2.1-6 \
                                         libgles2 \
                                         libvpx5
# Install gstreamer and plugins to support video playback in WebKit.
RUN apt-get update && apt-get install -y gstreamer1.0-gl \
                                         gstreamer1.0-plugins-base \
                                         gstreamer1.0-plugins-good \
                                         gstreamer1.0-plugins-bad
# Install Chromium dependencies
RUN apt-get update && apt-get install -y libnss3 \
                                         libxss1 \
                                         libasound2 \
                                         fonts-noto-color-emoji
# Install Firefox dependencies
RUN apt-get update && apt-get install -y libdbus-glib-1-2 \
                                         libxt6
# Install ffmpeg to bring in audio and video codecs necessary for playing videos in Firefox.
RUN apt-get update && apt-get install -y ffmpeg
# Add user so we don't need --no-sandbox in Chromium
RUN groupadd -r pwuser && useradd -r -g pwuser -G audio,video pwuser \
    && mkdir -p /home/pwuser/Downloads \
    && chown -R pwuser:pwuser /home/pwuser
# (Optional) Install XVFB if there's a need to run browsers in headful mode
RUN apt-get update && apt-get install -y xvfb
COPY --from=BrowserBuilder /app/dist /app/dist
# Run everything after as non-privileged user.
RUN mv /root/.cache/ /home/pwuser/.cache
RUN chmod a+rwx -R /home/pwuser/.cache
USER pwuser
# Install pabot to support atest
RUN pip install --user robotframework-pabot
RUN pip install --user dist/robotframework_browser-*-py3-none-any.whl
RUN rfbrowser init
ENV NODE_PATH=/usr/lib/node_modules
