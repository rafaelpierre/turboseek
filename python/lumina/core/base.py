from pydantic import BaseModel


class BaseTool(BaseModel):

    name: str
    max_retries: int

    
    def use(self, **kwargs):
        raise NotImplementedError("This method should be implemented by subclasses.")
    
 