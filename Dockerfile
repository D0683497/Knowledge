FROM node:12 as builder

WORKDIR /app/frontend
ADD ./frontend /app/frontend

RUN npm install
RUN npm run build
RUN npm cache clean --force \
 && rm -r ./node_modules


FROM python:3.6 as prod
ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app
COPY --from=builder /app/frontend /app/frontend

RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN python manage.py collectstatic --noinput
