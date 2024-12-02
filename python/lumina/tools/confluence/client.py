import httpx
from pydantic import BaseModel
from urllib.parse import urlencode

class ConfluenceClient(BaseModel):

    token: str
    domain: str

    
    def get(self):

        headers = {"Content-Type": "application/json"}

        params = {
            "cql": "type=page AND text~\"databricks\"",
            "limit": 10,
            "expand": "body.storage"
        }

        query_string = urlencode(params)

        response = httpx.get(
            url = f"https://{self.domain}.atlassian.net/wiki/rest/api/content/search?{query_string}",
            headers = headers,
            auth = httpx.BasicAuth(username = 'hello@llmshowto.com', password = self.token)
        )

        return response