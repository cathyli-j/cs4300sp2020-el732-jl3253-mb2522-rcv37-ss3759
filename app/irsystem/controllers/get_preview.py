from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
# response = urllib.request.urlopen('https://www.yelp.com/search?find_desc=empanadas%20house&find_loc=404%20E%20Green%20St%2C%20Champaign%2C%20IL')


# html = str(response.read())

# soup = BeautifulSoup(html, 'html.parser')

# preview_div = soup.find_all('div', class_='container__373c0__3HMKB')[1]

# imgs = preview_div.find_all('img')


def get_data_for_preview(bid):
    response = urllib.request.urlopen('https://www.yelp.com/biz/' + bid)
    html = str(response.read())
    return BeautifulSoup(html, 'html.parser')

def get_img_src(bid):
    #this is very slow so it returns nothing for now
    return ""
    response = urllib.request.urlopen('https://www.yelp.com/biz/' + bid)
    html = str(response.read())
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all('img')[3]['src']

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