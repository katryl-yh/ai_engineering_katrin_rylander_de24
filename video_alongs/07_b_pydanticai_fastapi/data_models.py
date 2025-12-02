from pydantic import BaseModel, Field


class Movie(BaseModel):
    title: str
    year: int = Field(gt = 1970)
    genre: str = Field(
        description="genre of the movie, if there are many genres, take the dominant one"
    )
    rating: int = Field(
        gt=0, lt=6, description="higher rating the better, keep ratings realistic"
    )


class Prompt(BaseModel):
    prompt: str = Field(description="""
        Prompt from user to find a movie, try to find closest movie even if the user 
        prompts something else
    """)