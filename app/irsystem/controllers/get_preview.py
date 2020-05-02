from bs4 import BeautifulSoup
import urllib.request
import urllib.parse



def get_img_src(bid):
    response = urllib.request.urlopen('https://www.yelp.com/biz/' + bid)
    html = str(response.read())
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all('img')[3]['src'] if len(soup.find_all('img')) > 40 else ""

def get_description(soup):
    return soup.find_all('section')[4].text

def get_url(name, address_str):
    base_url = 'https://www.yelp.com/search?'
    name_enc =  urllib.parse.quote(name.lower())
    loc_enc = urllib.parse.quote(address_str)
    params = f'find_desc={name_enc}&find_loc={loc_enc}'
    return base_url + params

# d = get_data_for_preview('f9NumwFMBDn751xgFiRbNA')
# print(get_description(d))