# Url shortener

This is a simple URL shortener made for learning the basics of Flask and
Vue.

It uses PostgreSQL as the database and `Flask-SQLAlchemy`. It has a
very simple database model: a single table with a primary key, a URL, a short
token and an optional expiration date.

I was especially interested in learning how to test the server.

The front-end was made with vue and is not very involved.

I used to host it on Heroku but decided to not do it anymore since these
applications can be exploited.
