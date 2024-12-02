import httpx
from pydantic import BaseModel
from urllib.parse import urlencode


class ConfluenceClientTool(BaseModel):
    """
        Wrapper class around Confluence REST API.

        Constructor params:

        `username`: Username for Authentication.
        `token`: Authentication token.
        `base_url`: Base URL for your Confluence website (for instance, `https://<org-id>.atlassian.net`)
        `search_endpoint`: REST API endpoint used for searching.
        `headers`: HTTP headers.

        More details: https://developer.atlassian.com/cloud/confluence/rest/v1/intro
    """

    username: str
    token: str
    base_url: str
    search_endpoint: str = "wiki/rest/api/content/search"
    headers: dict = {"Content-Type": "application/json"}


    def search(
        self,
        cql_query: str,
        query_prefix: str = "type=page",
        expand: str = "body.storage",
        limit: int = 3
    ):
        """
            Performs search over your Confluence pages.

            Params:

            `cql_query`: The query in CQL (Confluence Query Language)
            `query_prefix`: Query prefix that can be used for filtering results
            `expand`: Defines which page content will be returned for each search result.
            `limit`: Max number of search results.

            More details: https://developer.atlassian.com/server/confluence/advanced-searching-using-cql/
        """

        params = {
            "cql": f"{query_prefix} AND {cql_query}",
            "limit": limit,
            "expand": expand
        }

        query_string = urlencode(params)
        url = f"{self.base_url}/{self.search_endpoint}?{query_string}"

        response = httpx.get(
            url = url,
            headers = self.headers,
            auth = httpx.BasicAuth(
                username = self.username,
                password = self.token
            )
        )

        return response