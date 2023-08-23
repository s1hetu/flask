### Migrations
<br>

#### Create migrations directory
```python 
flask db init
```
#### Create Migration File
```python 
flask db migrate -m "commit_message"
```

It will output :  Detected <changes>


**_NOTE_** : If you are not able to detect D changes while running flask db migrate, 
import your models in **_migrations/env.py_**

![img.png](img.png)

<br>

#### Migrate
```python
flask db upgrade   -> To apply migrations as written in generated script's upgrade()
flask db downgrade -> To apply migrations as written in generated script's downgrade()
```
It will output : Running upgrade -> <file_name>, <commit_message>

<br>

**_NOTE_** : Flask Migrations does not detect a field's length change
So, to be able to detect that, Add follwing to context.configure() in migration/env.py

run_migrations_online()
run_migrations_offline()

```python
compare_type = True
```


### Relationships

#### 1. One-to-Many

```python
class A(db.model):
    id = db.Column(db.Integer, primary_ky=True)
    name = db.Column(db.String)
    bb = db.relationship('B', backref='a', lazy=True)
     
class B(db.Model):
    id = db.Column(db.Integer, primary_ky=True)
    data = db.Column(db.String)
    aa = db.Column(db.Integer, db.ForeignKey('a.id'), nullable=False)
```


**_relationship_** : relationship(model_name, backref='backref_name', lazy=True)

**_ForeignKey_** : ForeignKey('DB_table_name_in_snake_case'.id)
snake_case = A -> a, ABC -> abc, AbcAbc -> abc_abc

**_backref_** : backref is a simple way to also declare a new property on the Child class. 
You can then also use b_obj.a to get to the A at that b_obj.

**_lazy_** : lazy defines when SQLAlchemy will load the data from the database:

    1. 'select' / True (default) : load the data as necessary in one go using a standard select statement.
    2. 'dynamic' : used when u want to apply additional SQL filters to them. Instead of loading the items SQLAlchemy will return another query object which you can further refine before loading the items. Note that this cannot be turned into a different loading strategy when querying so it’s often a good idea to avoid using this in favor of lazy=True. 
    3. 'joined' / False : load the relationship in the same query as the parent using a JOIN statement.
    4. 'subquery' : works like 'joined' but instead SQLAlchemy will use a subquery.

#### 2. One-to-One
```python 
realtionship(....., uselist=False)
``` 

#### 3. Many-to-Many

If you want to use many-to-many relationships you will need to define a helper table that is used for the relationship. For this helper table it is strongly recommended to not use a model but an actual table:

```python
tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('pages', lazy=True))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
```


filter vs filter_by : column == expression vs. keyword = expression