# SQLasagna
*Because Lasagna tastes better than soup...*

SQLasagna is a project built on top of SQLAlchemy 0.7.2 aiming to provide automatic table and relationship reflections along with object mapping and some Magic Mixins allowing you to do pretty much everything you can do with SQLSoup today but using an emphasized ORM Dialect approach.
It uses SQLAlchemy declarative base, class mapper and reflections to map your whole database into nice objects.

I started this project since SQLSoup WILL BE DISCONTINUED on the next SQLAlchemy release (0.8). I don't use a single line of SQLSoup, so when it was removed SQLasagna will continue to work.

Also SQLSoup has approximately 400 lines of code ( 800 if you count comments ). SQLasagna has about 150 ( 200 w\ comments ) and can map relationships automatically, which SQLSoup can't at this time. Simplicity is cool.


Ok, this sounds strange, so let's see some code:


Using SQLasagna, you don't have to configura absolutely nothing, other than your database connection details in order to create the engine.
In the future, you will be able to customize how automatic mapper will act, if relationships will be lazy or eager, etc... This will probably be done in a JSON config file or passing a config dict to the connect method.


#### Installing

You must have SQLAlchemy 0.7.2 or higher installed.

After that you just need to setup SQLasagna. For now you can copy it to your site-packages dir, but a regular Python installer is on the way and soon the package will be available on the cheeseshop so all you have to do will be:

    # pip install sqlasagna

#### Versions

I have used **SQLAlchemy 0.7.5** and **Python 3.2** so, by now, I'll only support environments running on those versions. Also, I'm focused on get it working for MySQL, PostgreSQL and SQLite first, but I believe that this will kick-off pretty much anything that SQLAlchemy already supports.

#### Architecture

Well, as I've mentioned before I have used SQLAlchemy internals in order to build this.
The focus is to keep it simple and fast.
I've used SQLAlchemy's native declarative_base ORM extensions in order to build the SQLasagna extension. It consists in a mixin that enhances the native Base classe and instantiates along with Base on the ORM objects. Also a tiny bit of code that plugs on the Base metadata, scan the tables and relations and create the mapper objects dynamically.

#### Using


##### In order to use SQLasagna you must import it on your code, of course:

    import sqlasagna
    
##### Then you connect:

    db = sqlasagna.connect("mysql+oursql://YOUR_SQLALCHEMY_DSN", SQLALCHEMY_ENGINE_OPTIONS)
    
##### Now use:

Let's say you have a table user and this table have a foreign_key to a table phones which helds users phones and is linked to user by users_id.
With SQLasagna you can do things like:

    # Get a user by ID:
    
    myuser = db.users.get(1)
    
    # Check user name
    
    print(myuser.name)
    
    # Check user phones stored in a foreign table
    
    print(myuser.phones)
    
    # Print all phone numbers for this user
    
    for phone in myuser.phones:
        print(phone.number)
        
    
Cool huh?

Soon I will make some screencasts showing SQL Tables and how SQLasagna deals with them.


...to be continued