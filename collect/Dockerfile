# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /

# copy wait-for-it for database
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# copy the dependencies file to the working directory
COPY /requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .

# command to run on container start
CMD [ "python", "./pro/main.py" ]