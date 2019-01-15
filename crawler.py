import requests
import pandas as pd
from bs4 import BeautifulSoup as Soup
import re

data = {"Title": [], "SM":[], "Rooms": [], "Location":[], "Floor": [], "Type": [], "New building": [], "Price": [], "Link": []}
for page_no in range(1, 5):
    print(page_no)
    URL = 'https://www.imobiliare.ro/vanzare-apartamente/iasi?pagina='+str(page_no)
    page_content = requests.get(URL).content
    page = Soup(page_content, 'lxml')
    apartments = page.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['box-anunt'])
    for apartment in apartments:
        title = apartment.find('h2', class_="titlu-anunt hidden-xs").get_text()
        link = apartment.find('h2', class_="titlu-anunt hidden-xs").find('a')['href']
        location = apartment.find('div', class_="localizare").get_text()
        location = location.split("zona")[1].strip()
        price = apartment.find(lambda tag: tag.name == 'span' and tag.get('class') == ['pret-mare']).get_text()
        features = apartment.find("ul", class_="caracteristici").get_text().lower()
        print(features)
        square_meters = re.search("[1-9][0-9]{0,2} mp|[1-9][0-9]{0,2}.[1-9][0-9]{0,2} mp", features).group(0)
        square_meters = square_meters.split("mp")[0].strip()
        rooms = re.search("[1-9][0-9]{0,1} camer|o camer", features).group(0)
        rooms = rooms.split("camer")[0].strip()
        rooms = '1' if rooms == 'o' else rooms
        floor = re.search("etaj [1-9]|etaj [1-9][0-9]{0,2}/[1-9][0-9]{0,2}|parter|demisol|mansarda", features).group(0)
        if "etaj" in floor:
            floor = floor.split("etaj")[1].strip()
        apt_type = re.search("decomandat|semidecomandat", features).group(0) if re.search("decomandat|semidecomandat", features) else ""
        new_building = 1 if re.search("bloc nou", features) else 0
        data['Title'].append(title)
        data['Link'].append(link)
        data['Location'].append(location)
        data['Price'].append(price)
        data['SM'].append(square_meters)
        data['Rooms'].append(rooms)
        data['Floor'].append(floor)
        data['Type'].append(apt_type)
        data['New building'].append(new_building)
    pd.DataFrame(data=data).to_excel("apartments.xlsx", index=False)
