FROM osrf/ros:humble-desktop

RUN apt-get -y update && apt-get install -y ros-humble-ros-gz

# Install dev env
RUN apt-get -y update && apt-get install -y curl
RUN curl https://raw.githubusercontent.com/xRetry/dev-env/main/setup_env.sh | sh -s -- python

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Create a workspace folder
RUN mkdir -p /ws
WORKDIR /ws
