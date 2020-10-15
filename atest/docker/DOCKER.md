# Robotframework-browser dockerfiles

Dockerfile and Dockerfile.playwright20.04 are used for our own CI and docker image build flow.

Dockerfile.latest_release is used as the base to build our published docker images. 
See [packages](https://github.com/MarketSquare/robotframework-browser/packages) for latest released docker image.


Our published Dockerfile can be used as a base for running your own test suites inside docker.

The image comes with latest robotframework-browser and robotframework, and with pre-initialized browsers and other dependencies for running headful tests in the container.

Example usage:
``` bash
docker run --rm \
  -v $(pwd)/atest/test/:/test \
    docker.pkg.github.com/marketsquare/robotframework-browser/rfbrowser-stable:1.0.0 \
      bash -c "robot --outputdir /test/output /test"
```

`docker run -v` is used to mount the directory containing tests on the supervising machine. In this example robot output will also be output inside the test directory


When testing with chrome we recommend downloading a copy of `chrome.json` security settings and using the following docker run flags ```--ipc=host --security-opt seccomp=chrome.json``` for best compatibility. [Explanations and the chrome.json can be found here](https://github.com/microsoft/playwright/tree/master/docs/docker#run-the-image)

All dependencies are installed to support running tests as `pwuser` in the docker image. Running tests as root or other non `pwuser` can cause problems.
