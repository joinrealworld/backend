import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_live_streams():
    from .models import Stream  # Importing Stream model from the current app's models
    url = "https://the.streameast.app/v78"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    streams = []
    for item in soup.find_all('li', class_='f1-podium--item'):
        anchor = item.find('a', class_='f1-podium--link')
        title = anchor.find('span', class_='f1-podium--driver').get_text(strip=True)
        status = anchor.find('span', class_='f1-podium--time').get_text(strip=True)

        if 'live' in status.lower():
            stream_url = anchor['href']
            full_stream_url = urljoin(url, stream_url)

            stream_response = requests.get(full_stream_url)
            stream_soup = BeautifulSoup(stream_response.content, 'html.parser')

            # Find the iframe URL using exact start and end points
            iframe_script = stream_soup.find('script', text=lambda t: t and 'var iframeURL =' in t)
            if iframe_script:
                script_content = iframe_script.string

                # Locate the starting and ending points of the URL
                start_index = script_content.find('var iframeURL = "') + len('var iframeURL = "')
                end_index = script_content.find('=', start_index)
                
                # Extract the URL between the starting and ending points
                iframe_url = script_content[start_index + 1:end_index].strip()

                iframe_url += '=the.streameast.app'
                
                # Ensure the URL is correctly formatted
                if iframe_url.startswith('http'):
                    streams.append({'title': title, 'url': iframe_url, 'is_live': True})

    # Update the database with the live streams
    Stream.objects.all().delete()  # Clear existing streams
    for stream in streams:
        Stream.objects.create(**stream)
    return streams

# Example usage within your Django application
if __name__ == '__main__':
    fetch_live_streams()
