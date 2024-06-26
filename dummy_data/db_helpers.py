from history_database.schema import User, Reading
from history_database.alembic_utils import get_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc

def add_user():
    # Setup the engine and session
    engine = get_engine()
    Session = sessionmaker(bind=engine)

    # Step 2: Create a session
    session = Session()

    # Step 3: Create an instance of your model
    new_user = User(name='John Doe')

    # Step 4: Add the instance to the session
    session.add(new_user)

    # Step 5: Commit the transaction
    session.commit()

    # Close the session
    session.close()

def add_reading_record(record):
    engine = get_engine()
    Session = sessionmaker(bind=engine)

    session = Session()

    new_reading = Reading(**record)

    session.add(new_reading)

    session.commit()

    session.close()

def get_10_reading_records():
    engine = get_engine()
    Session = sessionmaker(bind=engine)

    session = Session()
    query = session.query(Reading).order_by(desc(Reading.created_at)).limit(10)

    # Using `with_entities` to specify the columns you want as dictionary keys
    dict_results = [
        {column.name: getattr(row, column.name) 
        for column in Reading.__table__.columns}
        for row in query
    ]

    session.close()

    return dict_results
