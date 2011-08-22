# SQLasagna
*Because Lasagna tastes better than soup...*

Hi! SQLasagna is a project built on top of SQLAlchemy 0.7.2 aiming to provide automatic table and relationship reflections along with object mapping and some Magic Mixins allowing you to do pretty much everything you can do with SQLSoup today but using an emphasized ORM Dialect approach.

Ok, this sounds strange, so let's see some code:


Using SQLasagna, you don't have to configura absolutely nothing, other than your database connection details in order to create the engine.


#### Installing

You don't have to install anything, just download the main script **sqlasagna.py** and you're ready to go. One of the main goals of this project it to keep it very simply and fast.

Also, you must have SQLAlchemy already installed on your machine along with Python.

#### Versions

I have used **SQLAlchemy 0.7.2** and **Python 3.2** so at least at the beginning, I'll only support environments running on those versions. Also, I'm focused on get it working for MySQL, PostgreSQL and SQLite first, but I believe that this will kick-off pretty much anything that SQLAlchemy already supports.

#### Architecture

Well, as I've mentioned before I have used SQLAlchemy internals in order to build this.
The focus is to keep it simple and fast.
I've used SQLAlchemy's native declarative_base ORM extensions in order to build the SQLasagna extension. It consists in a mixin that enhances the native Base classe and instantiates along with Base on the ORM objects. Also a tiny bit of code that plugs on the Base metadata, scan the tables and relations and create the mapper objects dynamically.

#### Using

###### Configure it

In the very beggining of the code, configure your connection to the database, according to SQLAlchemy instructions.

    # CONFIGURE YOUR CONNECTION HERE - Follow SQLAlchemy create_engine instructions.
    engine = create_engine("mysql+oursql://user:password@yourserver.domain/dbname?charset=utf8&use_unicode=True&autoping=True", echo=True)
    

In order to use SQLasagna you must import it on your code, of course:

    import sqlasagna
    
Or you can play interactively with SQLasagna and test some queries on the shell by running:

    # python3 -i sqlasagna.py
    
...to be continued