
import requests
from bs4 import BeautifulSoup
import csv


def f_conversion_rating(v_review_rating):
    """convert the word extract from rating review to a number more explicit
example  : dectecting the word five , if 'five' --> vrr =5
the range is 0--> 5 
    """
    if v_review_rating == "Zero":
        vrr = "0"
        return vrr
    elif v_review_rating == "One":
        vrr = "1"
        return vrr
    elif v_review_rating == "Two":
        vrr = "2"
        return vrr
    elif v_review_rating == "Three":
        vrr = "3"
        return vrr
    elif v_review_rating == "For":
        vrr = "4"
        return vrr
    elif v_review_rating == "Five":
        vrr = "5"
        return vrr
    else:
        print("valeur non reconnue !")


def f_find_end_balise(ma_chaine):

    """ cherche la premiere occurence caractere 
    designé d'une balise >
    """
    k = ">"
    x = ma_chaine.find(k)
    y = ma_chaine[22:(x-1)]
    return y


    """
project 02 of openclassrooms learning session
this projet has for mission to developp an application 
to scrap a website http://books.toscrape.com/
 first  operation :  choose a book's page and scrap  defined words
*********************************************************
                initialisation of the path
*********************************************************

    product_page_url =
    upc = ok
    title = ok
    price_including_tax ok
    price_excluding_tax ok
    number_available ok
    product_description ok
    category ok
    review_rating ok
    image_url = ok

**********************************************************
    """


site_cible = "http://books.toscrape.com/"
response = requests.get(site_cible)
response_book_link = site_cible + "/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"
response_book = requests.get(response_book_link)
response_book_txt = "C:\projet_OPC\oc02\oc_v2_tg_prj02\data\bookstoscrap.com.html"
r_temp = response_book.text  
#  choose the link to scrap

soup = BeautifulSoup(r_temp, 'html.parser')


"""
************************************************************
 results
*************************************************************

 find results within product_page
"""

results = soup.find_all("div",{"class": "item active"})

#  results2 = soup.find("div", {"class": "col-sm-6 product_main"}).find("p",
# {"class": "price_color"})
#  print('results2 ' + results2.text[2:])  # enleve le caractere pound

#  results3 = soup.find("div", {"class": "item active"}).find("div", 
# {"class": "col-sm-6 product_main"})

title = (soup.title.string)[5:-28]  # nettoyage de la 28 lettre de droite
#  print(' title ' + title)

number_available = soup.find("div", {"class": "col-sm-6 product_main"}).find("p",
    {"class": "instock availability"}).text[25:27]
number_available_str = str(number_available)
#  print(number_available)

upc = soup.find("table", {"class": "table table-striped"}).find("td")
upc_str = str(upc)
#  print('results upc ' + upc.text)

price_incl_tax = soup.find_all('td')[3].text[2:]
price_incl_tax_str = str(price_incl_tax)
#  print("price with tax " + price_incl_tax)

price_excl_tax = soup.find_all('td')[2].text[2:]
price_excl_tax_str = str(price_excl_tax)
#  print("price excl tax " + price_excl_tax)

product_description = soup.find_all('p')[3].text
#  print(product_description)

category = soup.find_all('li')[2].text[1:]
#  print("category " + category)

image_url = soup.find_all('img')[0]
image_url = image_url.attrs['src']
image_url = site_cible + image_url[5:]
#  print(image_url) 

review_rating = soup.find_all(attrs={"star-rating"})[0]
review_rating_text = str(review_rating)
review_rating_text_number = f_find_end_balise(review_rating_text)
review_rating_text_number = f_conversion_rating(review_rating_text_number)
#  print('rating ' + review_rating_text_number)

#  <a href="/catalogue/while-you-were-mine_97/reviews/">

product_url = response_book_link
#  print(product_url)

ma_ligne = {}
ma_ligne["product page url"] = response_book_link
ma_ligne["title"] = title
ma_ligne["upc"] = upc_str
ma_ligne["category"] = category
ma_ligne["number available"] = number_available_str
ma_ligne["review rating"] = review_rating_text_number
ma_ligne["image url"] = image_url
ma_ligne["price incl tax"] = price_incl_tax_str
ma_ligne["price excl tax"] = price_excl_tax_str
ma_ligne["product description"] = product_description

#   print(ma_ligne)

test_w = response_book_link + ";" + title + ";" + upc_str + ";" + category + ";"
test_w = test_w + number_available_str + ";" + review_rating_text_number + ";"
test_w = test_w + image_url + ";" + price_incl_tax_str
test_w = test_w + ";" + price_excl_tax_str + ";" + product_description
#  print(test_w)
#  f_read_writing_book_csv_file2(ma_ligne)

#  print(test_w)


       