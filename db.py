from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL should be in the following format:
# "postgresql://user:password@host:port/database_name"
# For example, "postgresql://scott:tiger@localhost/mydatabase"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres.zftdtawwskwhmusyawrm:Garvit99284@aws-0-us-west-1.pooler.supabase.com:6543/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Each instance of the SessionLocal class will be a database session. 
# The class itself is not a database session yet.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# We will use this Base class to create each of the database models or classes (the ORM models).
Base = declarative_base()


