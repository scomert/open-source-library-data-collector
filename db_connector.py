import os
import urlparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import Config

if (os.environ.get('ENV') != 'prod'):
    Config.init_environment()
    mysql_db = os.environ.get('MYSQL_DB')
    mysql_host = os.environ.get('MYSQL_HOST')
    mysql_username = os.environ.get('MYSQL_USERNAME')
    mysql_password = os.environ.get('MYSQL_PASSWORD')
    mysql_port = os.environ.get('MYSQL_PORT')
else: # We are in Heroku
    url = urlparse.urlparse(os.environ['CLEARDB_DATABASE_URL'])
    mysql_db = url.path[1:]
    mysql_host = url.hostname
    mysql_username = url.username
    mysql_password = url.password
    mysql_port = '3306'
    
connect_string = 'mysql+pymysql://' + mysql_username + ':' + mysql_password + '@' + mysql_host + ':' + mysql_port + '/' + mysql_db
engine = create_engine(connect_string)
Base = declarative_base(engine)

class GitHubData(Base):
    """Autogenerated model for the github_data table, see db/data_schema.sql for details
    
    This table stores GitHub data (e.g. Pull Requests, Forks, Stars, etc.)
    """
    __tablename__ = 'github_data'
    __table_args__ = {'autoload':True}
    
class PackageManagerData(Base):
    """Autogenerated model for the package_manager_data table, see db/data_schema.sql for details
    
    This table stores Package Manager (e.g. Nuget, Packagist, npm, etc.) download data 
    """
    __tablename__ = 'package_manager_data'
    __table_args__ = {'autoload':True}
    
def loadSession():
    """Return a DB session
    :returns: A SQLAlchemy DB session
    :rtype:   session
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
    
class DBConnector(object):
    """CRUD for the sync email list database, focused on un/resubscribes"""    
    def __init__(self):
        self.session = loadSession()
        return
    
    """Add an item to the DB
    :returns:   True if the addition was successful
    :rtype:     bool
    """    
    def add_data(self, data_object):
        self.session.merge(data_object)
        self.session.commit()
        return True

    """Add an item to the DB
    :returns:   All data objects (GitHubData or PackageManagerData) in the DB
    :rtype:     List
    """      
    def get_data(self, data_object):
        return self.session.query(data_object).all()