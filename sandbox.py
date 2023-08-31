import os
from dotenv import load_dotenv
import psycopg2

from langchain_experimental.sql import SQLDatabaseChain
from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain.chat_models import ChatOpenAI

from langchain_experimental.sql.base import SQLDatabaseSequentialChain
from sqlalchemy.exc import ProgrammingError, DataError


load_dotenv() 
# Avoid huggingface/tokenizers parallelism error
os.environ["TOKENIZERS_PARALLELISM"] = "false"
# Load environment variables from .env file
load_dotenv()



#GET PARAMETERS FOR RDS
answer = ''
# SQLAlchemy 2.0 reference: https://pypi.org/project/sqlalchemy-RDS/
# Endpoint format: RDS+psycopg2://username@host.amazonaws.com:5439/database
RDS_HOST = os.getenv("RDS_ENDPOINT")
RDS_PORT = os.getenv("RDS_PORT")
RDS_DATABASE = os.getenv("RDS_DB_NAME")
RDS_USERNAME = os.getenv("RDS_USERNAME")
RDS_PASSWORD = os.getenv("RDS_PASSWORD")

RDS_ENDPOINT = f"postgresql://{RDS_USERNAME}:{RDS_PASSWORD}@{RDS_HOST}:{RDS_PORT}/{RDS_DATABASE}" + "?options=-c%20search_path%3Dmoma_generative_ai"

#print(RDS_ENDPOINT)


#CONNECT TO RDS

# Replace with your RDS details
host = RDS_HOST 
dbname = RDS_DATABASE 
user = RDS_USERNAME 
password = RDS_PASSWORD
port = RDS_PORT # Default is 5432 for PostgreSQL

# Establish a connection
try:
    connection = psycopg2.connect(
        host=host,
        dbname=dbname,
        user=user,
        password=password,
        port=port
    )
    #print("Connection successful!")
    
    # Optionally, execute a test query
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        print("Test query result:", result)
        
except psycopg2.Error as e:
    print("Error:", e)
finally:
    if connection:
        connection.close()

#LangChain OpenAI
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, verbose=True)



#####################################

# A few sample questions
QUESTION_01 = "How many artists are there?"
QUESTION_02 = "How many artworks are there?"
QUESTION_03 = "How many rows are in the artists table?"
QUESTION_04 = "How many rows are in the artworks table?"
QUESTION_05 = "How many artists are there whose nationality is French?"
QUESTION_06 = "How many artworks were created by artists whose nationality is Spanish?"
QUESTION_07 = "How many artist names start with 'M'?"
QUESTION_08 = "What nationality produced the most number of artworks?"
QUESTION_09 = "How many artworks are by Claude Monet?"
QUESTION_10 = "What is the oldest artwork in the collection?"



db = SQLDatabase.from_uri(RDS_ENDPOINT)

db_chain = SQLDatabaseSequentialChain.from_llm(
    llm, db, verbose=True, use_query_checker=True, return_intermediate_steps=True
)

instructions = """ 

"""

#try:
 #   db_chain(QUESTION_01 + instructions)
#except (ProgrammingError, ValueError, DataError) as exc:
    #print(f"\n\n{exc}")
 #   answer = f"\n\n{exc}"


try:
    answer =  db_chain(QUESTION_01 + instructions)
except (ProgrammingError, ValueError, DataError) as exc:
    answer = f"\n\n{exc}"


print(answer["intermediate_steps"][5])
