import json
import pprint
from constants import DATA_PATH, CURRENT_YEAR
from pydantic import BaseModel, Field, field_validator

# convenience function to read json data
def read_json(filename):
    with open(DATA_PATH / filename, "r") as file:
        data = json.load(file)

    return data

# pydantic models 
class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int = Field(gt=1000, lt=CURRENT_YEAR + 1, description="The year of when book is published.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 11,
                "title": "Learn with AIgineer",
                "author": "Kokchun Giang",
                "year": 2025,
            }
        }
    }

class Library(BaseModel):
    name: str
    books: list[Book]

# data validation function
def library_data(filename):
    json_data = read_json(filename)
    return Library.model_validate(json_data)

class YearFilter(BaseModel):
    start_year: int = Field(1800, gt=1000, lt=2026)
    end_year: int = Field(2000, gt=1000, lt=2026)

    @field_validator("end_year")
    @classmethod
    def validate_end_year(cls, value, info):
        if value <= info.data.get("start_year"):
            raise ValueError("end_year must be greater than start_year")
        return value
    
if __name__ == "__main__":
    print(repr(read_json("library.json")))