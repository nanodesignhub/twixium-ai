import os
import sys
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError, ProgrammingError, SQLAlchemyError

# Define a base for declarative models
Base = declarative_base()

# Define a minimal User model that mirrors your application's User model
# This allows us to query the table without needing the full Flask app context
class User(Base):
    __tablename__ = 'user' # Ensure this matches your actual table name if different
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128))
    is_admin = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', is_admin={self.is_admin})>"

def verify_database():
    """
    Connects to the database and verifies the existence of the 'user' table
    and optionally checks for the default admin user.
    """
    # Get database URI from environment variable
    # Ensure DATABASE_URL is set on your Droplet, e.g.,
    # export DATABASE_URL="mysql+pymysql://user:password@host/db_name"
    # or export DATABASE_URL="sqlite:///site.db"
    database_url = os.environ.get('DATABASE_URL')

    if not database_url:
        print("Error: DATABASE_URL environment variable is not set.")
        print("Please set it to your database connection string, e.g.:")
        print("  export DATABASE_URL=\"mysql+pymysql://user:password@host/db_name\"")
        print("  or export DATABASE_URL=\"sqlite:///site.db\"")
        sys.exit(1)

    print(f"Attempting to connect to database using: {database_url.split('@')[-1] if '@' in database_url else database_url}")

    try:
        # Create a database engine
        engine = create_engine(database_url)

        # Try to connect to the database to check connectivity
        with engine.connect() as connection:
            print("Successfully connected to the database.")

        # Create a session to interact with the database
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            # Check if the 'user' table exists by attempting a simple query
            # This will raise an error if the table does not exist
            user_count = session.query(User).count()
            print(f"Table 'user' exists. Found {user_count} users.")

            # Optionally, check for the default admin user
            admin_email = os.environ.get('ADMIN_EMAIL', 'admin@twixium.ai')
            admin_user = session.query(User).filter_by(email=admin_email).first()

            if admin_user:
                print(f"Default admin user '{admin_email}' found in the database.")
                print(f"Admin user details: {admin_user.to_dict() if hasattr(admin_user, 'to_dict') else admin_user}")
            else:
                print(f"Default admin user '{admin_email}' NOT found in the database.")
                print("You might need to ensure create_admin_user() ran successfully during Flask app startup.")

            print("\nDatabase verification successful!")

        except (OperationalError, ProgrammingError) as e:
            print(f"Error: Database table 'user' not found or inaccessible.")
            print(f"Please ensure Flask's db.create_all() has been run to create tables.")
            print(f"Details: {e}")
            sys.exit(1)
        except SQLAlchemyError as e:
            print(f"An unexpected SQLAlchemy error occurred during table check: {e}")
            sys.exit(1)
        finally:
            session.close()

    except OperationalError as e:
        print(f"Error: Could not connect to the database.")
        print(f"Please check your DATABASE_URL, database server status, and network connectivity.")
        print(f"Details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during database connection: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify_database()
