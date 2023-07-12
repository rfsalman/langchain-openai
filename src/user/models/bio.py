from pydantic import BaseModel, Field

class UserBioModel(BaseModel):
  full_name: str = Field(default=None, description="The user's full name")
  date_of_birth: str = Field(default=None, description="Date of birth in YYYY-MM-DD format")
  gender: str = Field(default=None, description="User's gender: (male|female)")
  interests: list[str] = Field(default=[], description="List of user's interest, deducted from chat topics")
  relationship_goal: str = Field(default=None, description="Could be one of: friends, short-term, long-term")