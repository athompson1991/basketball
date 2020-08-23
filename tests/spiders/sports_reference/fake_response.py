import os

from scrapy.http import Response, Request, HtmlResponse


def fake_response(file_path, url=None):
    """
    Create a Scrapy fake HTTP response from a HTML file
    @param file_name: The relative filename from the responses directory,
                      but absolute paths are also accepted.
    @param url: The URL of the response.
    returns: A scrapy HTTP response which can be used for unittesting.
    """
    request = Request(url=url)

    file_content = open(file_path, 'r').read()
    response = HtmlResponse(
        url=url,
        request=request,
        body=file_content,
        encoding='utf-8'
    )
    return response