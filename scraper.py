import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

def main():
    with requests.Session() as session:
        url = ""
       # headers = {'user-agent': }
        # teste da silva junior
        jumento = "teste de guimaraes silva"
        file_name = re.findall("[\-a-z]+(?=\.)", url) # type: ignore
        if file_name[1]:
            file_name = f"{file_name[1]}_{datetime.today().strftime('%d-%m-%Y')}_dump.json"
        else:
            file_name = f"{file_name[0]}_{datetime.today().strftime('%d-%m-%Y')}_dump.json"
        
        # gets the raw html data from the site
        raw_html = session.get(url, stream=True)

        # Tries to get the server ip and connection port
        try:
            iport = raw_html.raw._connection.sock.getpeername() # type: ignore
        except AttributeError:
            iport = 'Unable to fetch'
        # collects cookies from the site
        cookie_data = [(cookie.name, cookie.value, cookie.domain, cookie.path) for cookie in raw_html.cookies]
        # parses the raw html through python html parser using beautiful soup
        parsed_html = BeautifulSoup(raw_html.content, 'html.parser')
        # gets a list of tuples with all the links in the page
        links = get_links(parsed_html)
        # Whole text content of the page
        page_text = [line.strip() for line in parsed_html.get_text().split('\n') if line.strip() != ""]
        # Filtered text content (hopefully the main article)
        filtered_text = [text.get_text() for text in parsed_html.find_all('p')]

        json_consctructed = {
            'title': parsed_html.title, # type: ignore
            'response': (str(raw_html.request), str(raw_html.status_code)),
            'IP / Port': str(iport),
            'encoding': str(raw_html.encoding),
            'headers': dict(raw_html.headers),
            'cookies': cookie_data,
            'links': links['links_in_page'],
            'filtered_text_content': filtered_text,
            'text_content': page_text
        }
        with open(file_name, 'w') as file:
            json.dump(json_consctructed, file)

def get_links(parsed_html) -> dict:
    # Gets all links inside the html page (to other pages or inside the page)
    raw_links = parsed_html.find_all('a')
    # Removes all the links that point to inside the document
    links = [(link.get_text(), link.get('href')) for link in raw_links if (type(link.get('href')) != type(None)) if ('https' in link.get('href') or 'http' in link.get('href'))]
    # Formats the remaining links to a json format.
    formated_links = {
        'links_in_page': links
    }
    return formated_links
if __name__ == '__main__':
    main()
