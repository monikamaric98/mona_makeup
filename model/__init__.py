from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base , sessionmaker

engine = create_engine("mysql+pymysql://mona_makeup:lozinka@mysql:3306/mona_makeup" , connect_args={'unix_socket': None})
Session = sessionmaker(bind=engine)

session = Session()
Base = declarative_base()

