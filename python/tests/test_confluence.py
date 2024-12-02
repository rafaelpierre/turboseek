from lumina.tools.confluence.client import ConfluenceClientTool
from dotenv import load_dotenv
import os
import logging

load_dotenv()

def test_client():

    token = os.getenv("ATLASSIAN_API_KEY")
    username = os.getenv("ATLASSIAN_API_USER_NAME")
    client = ConfluenceClientTool(
        username = username,
        token = token,
        base_url = "https://llmshowto.atlassian.net"
    )

    result = client.search(cql_query='text~"databricks"')
    logging.info(result.text)