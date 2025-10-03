# Robotframework-browser dockerfiles

Dockerfile.tests is used for our own CI and docker image build flow.

Dockerfile.latest_release is used as the base to build our published docker images.
See [packages](https://github.com/MarketSquare/robotframework-browser/packages) for latest released docker image on github packages, and [dockerhub tags](https://hub.docker.com/r/marketsquare/robotframework-browser/tags?page=1&ordering=last_updated) for latest image on dockerhub.

Example pull: `docker pull marketsquare/robotframework-browser`


Our published Dockerfile can be used as a base for running your own test suites inside docker.

The image comes with latest robotframework-browser and robotframework, and with pre-initialized browsers and other dependencies for running headful tests in the container.

Example usage:
``` bash
docker run --rm -v $(pwd)/atest/test/:/test --ipc=host --user pwuser --security-opt seccomp=seccomp_profile.json marketsquare/robotframework-browser:latest bash -c "robot --outputdir /test/output /test"
```

`docker run -v` is used to mount the directory containing tests on the supervising machine. In this example robot output will also be output inside the test directory


When testing with chrome we recommend downloading a copy of `seccomp_profile.json` security settings and using the following docker run flags ```--ipc=host --security-opt seccomp=seccomp_profile.json``` for best compatibility. [Explanations and the seccomp_profile.json can be found here](https://github.com/microsoft/playwright/blob/master/docs/src/docker.md#crawling-and-scraping)

(Get it directly with `wget https://raw.githubusercontent.com/microsoft/playwright/master/utils/docker/seccomp_profile.json` )

All dependencies are installed to support running tests as `pwuser` in the docker image. Running tests as root or other non `pwuser` can cause problems.

# Build docker file locally

To build docker image locally, go ./docker folder and give command

```bash
cd docker
docker build --no-cache -t tidii --file Dockerfile.latest_release .
```

or output to file:
```bash
cd docker
docker build --no-cache -t tidii --file Dockerfile.latest_release . > out.txt 2>&1
```

Run test with locally build image
```bash
docker run -v ./atest/:/home/pwuser/test  -t tidii:latest bash -c "robot --outputdir /test/output /home/pwuser/test"
````

To start bash in container
```bash
docker run -i  -t tidii:latest bash
```

# Run docker pr build test

1. Modify [Dockerfile.dev_pr](Dockerfile.dev_pr)
> COPY docker/dist/*.whl /home/pwuser/

to
> COPY dist/*.whl /home/pwuser/
2. Build Browser wheel with: `invoke package`
3. Build Docker pr container
> docker build -t tidii --file docker/Dockerfile.dev_pr .

4. Run test with command below:
```bash
docker run -v ./atest/:/home/pwuser/test  -t tidii:latest bash -c "robot -v SERVER:host.docker.internal:7272 --exclude no-docker-pr -L debug --outputdir /home/pwuser/output /home/pwuser/test"
```
