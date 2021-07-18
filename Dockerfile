FROM python:3.9

WORKDIR /usr/src/book_bot/

COPY . /usr/src/book_bot/
COPY start_gunicorn.sh /usr/src/book_bot/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x /usr/src/book_bot/start_gunicorn.sh

