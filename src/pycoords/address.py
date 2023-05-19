from pydantic import BaseModel


class Address(BaseModel):
    def __str__(self):
        pass
        # TODO: @aein return the right f string
        # return f""
