# pull official base image
FROM python:latest
# set work directory
WORKDIR /usr/src/app
# set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
# install dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# copy project
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]