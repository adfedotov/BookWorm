# BookWorm
BookWorm is a project developed to help people keep their initial thoughts on the books they have read. 

This project was created to solve my personal problem of reading books
and quickly forgetting the main ideas and highlights from them. 

What I used:
- Python's Flask framework
- SQLAlchemy for ORM
- Integrated GoodReads API
- Quilljs for note taking
- HTML, CSS, JavaScript

## Setup
- You need to install dependencies
```
pip install -r requirments.txt
```
- Edit the config file 'config.py' to include a URI for your database (I use PostgreSQL). You will also need to include
a GoodReads API key.
- Initialize the database by running the app in shell context
```
set FLASK_APP=shell_context.py
flask shell
>>> db.create_all()  # This will create all the tables you need in the database
```
- You should be set! Run the app
```buildoutcfg
set FLASK_APP=main.py
flask run
```
*You should be able to access it by going to 127.0.0.1:5000*

## Database

![bookworm](https://user-images.githubusercontent.com/38639610/65824665-871af600-e221-11e9-9cab-3c7320911a8b.png)


## To Do

- Update data displayed when making a book search
- Tests
- GoodReads has limitations on API usage, need to set certain restrictions
- Improve design
