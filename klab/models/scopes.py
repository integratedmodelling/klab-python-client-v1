from pydantic import BaseModel

class UserScope(BaseModel):
    pass

class SessionScope(BaseModel):
    pass

class ContextScope(BaseModel):
    pass
