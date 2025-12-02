from pydantic_ai import Agent
from data_models import Movie
from dotenv import load_dotenv

load_dotenv()

movie_agent = Agent(model="google-gla:gemini-2.5-flash", output_type=Movie, retries=3)
