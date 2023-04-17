from urllib.parse import urlencode, urlparse, parse_qs
from requests import get

from django.shortcuts import get_object_or_404, render
from bs4 import BeautifulSoup
import re

def search(request):
    # Set the query from the user as the query for the google search
    # also ensure language is english by sending hl=en
    query = request.GET.get('query', '')
    url = f"https://www.google.com/search?hl=en&q={query}"

    # Set headers to mimic browser behavior and avoid getting blocked
    headers = {
        "Accept-Language": "en",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Send a GET request to Google and retrieve the HTML content
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")


    # Find the div containing the id result-stats which has the number of results
    number_of_results = soup.find("div", {"id": "result-stats"})
    if number_of_results is not None:
        number_of_results = number_of_results.get_text()
        number_of_results = " ".join(number_of_results.split(" ")[:-2])
    else:
        number_of_results = "No results to show"

    # Find the div with the id search which will contain the search results
    search_results = soup.find("div", {"id": "search"})

    if search_results is not None:
        # Find all <a> tags that are not inside a <span> tag as those
        # are not a search results but suggestions
        # also make sure the href text starts with https to filter out links specific
        # to google
        result_links = search_results.find_all(
            lambda tag: tag.name == 'a' 
            and not tag.find_parent('span')
            and tag.get('href', '').startswith('https')
        )
        top_results = [link.get("href") for link in result_links][:5]
    else:
        top_results = []

    return render(
        request, 'search.html', 
        {
            'query': query,
            'results': top_results,
            'number_of_results': number_of_results
        }
    )
        