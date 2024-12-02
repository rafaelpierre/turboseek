from lumina.tools.confluence.client import ConfluenceClient
from dotenv import load_dotenv
import os
import logging

load_dotenv()

def test_client():

    token = os.getenv("ATLASSIAN_API_KEY")
    client = ConfluenceClient(
        token = token,
        domain = "llmshowto"
    )

    result = client.get()
    logging.info(result.text)