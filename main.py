
import requests
from bs4 import BeautifulSoup
import csv


def my_soup(website_target):
    """
funtion to create the soup with webiste target in argument
choose the link to scrap
"""
    response_book = requests.get(website_target)
    response_book_txt = response_book.text
      
    soup = BeautifulSoup(response_book_txt, 'html.parser')

    return soup


def f_scrap_my_Book(book_target):
    """
    function to catch all information needed about the book page designed
    product_page_url=
    upc = ok
    title=ok
    price_including_tax ok
    price_excluding_tax ok
    number_available ok
    product_description ok
    category ok
    review_rating ok
    image_url= ok

    """
    soup = my_soup(book_target)
    #  print(soup)
    title = (soup.title.string)[5:-28]  # nettoyage de la 28 lettre de droite
#  print(' title ' + title)

    number_available = soup.find("div", {"class": "col-sm-6 product_main"}).find("p", {"class": "instock availability"}).text[25:27]
    number_available_str = str(number_available)
#  print(number_available)

    upc = soup.find("table", {"class": "table table-striped"}).find("td")
    upc_str = str(upc)
    upc_str = upc.text
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

    product_url = book_target
#  print(product_url)

    ma_ligne = {}
    ma_ligne["product page url"] = book_target
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

    test_w = book_target + ";" + title + ";" + upc_str + ";"
    test_w = test_w + category + ";" + number_available_str + ";"
    test_w = test_w + review_rating_text_number + ";" + image_url + ";"
    test_w = test_w + ";" + price_incl_tax_str + price_excl_tax_str + ";"
    test_w = test_w + product_description
    #  print(test_w)
    return test_w
    print(len(test_w))

    #  f_read_writing_book_csv_file2(test_w)  a conserver
    #  print(test_w)


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
    elif v_review_rating == "Four":
        vrr = "4"
        return vrr
    elif v_review_rating == "Five":
        vrr = "5"
        return vrr
    else:
        print("valeur non reconnue !")


def f_find_end_balise(ma_chaine):

    """ cherche la premiere occurence caractere designé d'une balise >
    """
    k = ">"
    x = ma_chaine.find(k)
    y = ma_chaine[22:(x-1)]
    return y


def f_read_writing_book_csv_file2(mon_book_text):
    """
function to read & write the book informations into a csv file.
the csv separator is a ";" due to the string imported.
    """
    my_csv_file = 'C:\\projet_OPC\\oc02\\oc_v2_tg_prj02\\data\\scrap_book.csv'
    with open(my_csv_file, "a", encoding='utf-8', newline='') as mon_book:
        mon_book_text_w = csv.writer(mon_book, delimiter=';')     
        mon_book_text_w.writerow([mon_book_text])


def f_test_nextpage(test_pageup):
    """
    """
    pageup_link = ""
    try:
        test_pageup2 = test_pageup.find_all("li", {"class": "next"})[0]
        #  test_pageup3 = test_pageup2.find("a").attrs['href']

        if test_pageup2 != "" or not None:
            pageup_link = test_pageup2.find("a").attrs['href']
            return (pageup_link)
        else:
            return ""

    except ValueError:
        print("pas de page supplémentaire ! rubrique suivante...")

"""
def f_next_construct_link (page_up_index):
   
#concatenation of name of page index into a library

   
    test = 10
"""

def f_catch_book_into_category(site_cible):
    """
     catch books links into the category page

    """

    url_cat = "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
    response_url_cat = requests.get(url_cat)
    response_url_cat_text = response_url_cat.text
    if response_url_cat.ok:
        book_cat_links = []
        book_cat_soup = BeautifulSoup(response_url_cat_text, 'html.parser')
        catch_cat_bib = book_cat_soup.find_all("div", {"class": "image_container"})

        i = 0
        # if 
        for ccb in catch_cat_bib:
            a = ccb.find('a')  #  ("div",{"class": "item active"})
            i += 1
            link = "catalogue/" + a['href'][9:]
            #  print(site_cible)
            book_cat_links.append(site_cible[:26] + link)
    #  test_pageup = f_test_nextpage(response_url_cat_text)
        if i == 20:
            try:
                test_pageup = f_test_nextpage(book_cat_soup)
                if test_pageup != "":
                    tesst = 10
    #  print(len(book_cat_links))
                return(book_cat_links)
            except:

def scrap_category_page(page_url):
    """ 
        return the list of books page's url for the given 
        category page
    """
    try:
        resp = requests.get(page_url)
        
    except Exception as error: #
        pass   
    resp.encoding = 'utf8'
            
    if not resp.ok:

        raise Exception("url erreur 404") # resp.status ?
         
    soup = BeautifulSoup(resp, 'html.parser')
    
    #  catch_cat_bib = soup.find_all("div", {"class": "image_container"})
    books_urls = [
        a['href'].replace('../../..', page_url[:-10])for a in soup.select(".image_container > a")]

    next_a = soup.select_one('.next > a')
    
    return books_urls, next_a["href"] if next_a else None

"""

project 02 of openclassrooms learning session
this projet has for mission to developp an application 
to scrap a website http://books.toscrape.com/
 first  operation :  choose a book's page and scrap  defined words
*********************************************************
                    initialisation of the path
*********************************************************

    

**********************************************************
    """


site_cible = "http://books.toscrape.com/"
response = requests.get(site_cible)
response_book_link = site_cible + "/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"
response_book = requests.get(response_book_link)
response_book_txt = "C:\\projet_OPC\\oc02\\oc_v2_tg_prj02\\bookstoscrap.com.html"
r_temp = response_book.text  
#  choose the link to scrap

soup = BeautifulSoup(r_temp, 'html.parser')


"""
************************************************************
 results
*************************************************************

 find results within product_page
"""

results = soup.find_all("div", {"class": "item active"})


#  f_read_writing_book_csv_file2(ma_ligne)
book_cat_links = []
list_cat_links = []
list_all_cat =[]
it = 1
category_section = "mystery_3"
init_page_index = "index.html"
site_cible = site_cible + "catalogue/category/books/" + category_section + "/" + init_page_index
book_cat_links = f_catch_book_into_category(site_cible)

# boot_cat_link catch the link of book into a category to scrap information
#  in the book page
print(len(book_cat_links))
#  print (book_cat_links)
i = 0
while True:

    books_list, next_page_url = scrap_category_page(url)
    if not next_page_url:
        break

# def f_iterativ_link_catch():


"""

for i in range(len(list_cat_links)):
    while it > 0:
        (book_cat_links, it) = f_catch_book_into_category(site_cible)
        
    item_page_cat = list_cat_links[i]

    for j in range(len(book_cat_links)):
        #  print(i)
        book_link_item = book_cat_links[j]
        #  print(book_link_item)

        book_writer = f_scrap_my_Book(book_link_item)
        #  print(book_writer)
        f_read_writing_book_csv_file2(book_writer)
        j += 1
    i +=1


    """
       