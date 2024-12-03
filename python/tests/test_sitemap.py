from lumina.ingestion.sitemap import SitemapIngestionPipeline
import logging


def test_url_list():

    pipeline = SitemapIngestionPipeline(
        sitemap_url = "https://lancedb.github.io/lancedb/sitemap.xml",
        xpath = '*//div[contains(@class, "md-content")]//text()'
    )
    result = pipeline(
        start = 0,
        end = 2
    )
    logging.debug(result)
