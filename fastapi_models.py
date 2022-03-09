from doctest import Example
from pydantic import BaseModel, Field
from typing import Optional, List


class Item(BaseModel):
    date: Optional[str] = Field(None, example = "2022-02-26 10:01:09")
    data: Optional[str] = Field(None, example = "Green Hydrogen Policy - another positive step towards India's energy security - Power Technology")
    source: Optional[str] = Field(None, example = "The Indian Express")
    score:Optional[float] = Field(None, example = -0.9987684)