import requests
import urllib.parse

def search(query):    
    url = 'https://api.hellopeter.com/api/search/business?name={0}'
    # encode the query string
    query = urllib.parse.quote(query)
    # make the request
    response = requests.get(url.format(query))
    # return the response
    return response.json()

if __name__ == '__main__':
    # test the function
    print(search('game'))    