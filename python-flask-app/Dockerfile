# Copyright (c) 2023, WSO2 LLC. (https://www.wso2.com/) All Rights Reserved.

# WSO2 LLC. licenses this file to you under the Apache License,
# Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.


# dont use alpine! https://pythonspeed.com/articles/alpine-docker-python/
FROM python:3.8-slim

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
RUN ls
# Create a new user with UID 10016
RUN addgroup --gid 10016 choreo && \
    adduser  --disabled-password  --no-create-home --uid 10016 --ingroup choreo choreouser

# make a tmp dir to hold csv and png files
RUN rm -rf tmp 
RUN python --version
RUN mkdir tmp
RUN chmod -0644 tmp
run chown choreouser tmp

USER 10016
EXPOSE 5000
CMD [ "flask", "run", "--host=0.0.0.0"]
