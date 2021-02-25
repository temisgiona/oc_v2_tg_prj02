
import requests
from bs4 import BeautifulSoup
import csv
import re
import os

def my_soup(page_url):
    """
funtion to create the soup with webiste target in argument
choose the link to scrap
"""
    try:
        resp = requests.get(page_url)
        r_status = resp.status_code
        resp.encoding = 'utf8'
        
    except Exception as error:
        print('erreur sur le lien')
        r_status = 505  
    soup = ""
    if r_status == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')

    return soup if soup else None, r_status


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
    soup, r_status = my_soup(book_target)
    #  print(soup)
    title_ori = (soup.title.string)[5:-28]
    title = title_ori.strip("/n")
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

    product_description_ori = soup.find_all('p')[3].text
    product_description = product_description_ori.strip('\n')
#  print(product_description)

    category_ori = soup.find_all('li')[2].text[1:]
    category = category_ori.strip('\n')
#  print("category " + category)

    image_url = soup.find_all('img')[0]
    image_url = image_url.attrs['src']
    image_url = book_target[:26] + image_url[5:]
#  print(image_url) 

    #  review_rating = (soup.find_all(attrs={"star-rating"})[0])['class'][1]
    review_rating = soup.find('p', attrs={"star-rating"})['class'][1]
    
    review_rating_text_number = conversion_rating2(review_rating)
#  print('rating ' + review_rating_text_number)

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

    book_info = book_target + ";" + title + ";" + upc_str + ";"
    book_info = book_info + category + ";" + number_available_str + ";"
    book_info = book_info + review_rating_text_number + ";" + image_url + ";"
    book_info = book_info + ";" + price_incl_tax_str + ";"
    book_info = book_info + price_excl_tax_str + ";" + product_description

    return book_info, category, image_url


def f_conversion_rating(v_review_rating):
    """convert the word extract from rating review to a number more explicit
example  : dectecting the word five , if 'five' --> vrr =5
the range is 0--> 5 
    """
    dict_rating = {"Zero":0, "One":1, "Two":2, "Three":3, "Four":4, "Five":5}
    try:
        vrr = dict_rating[v_review_rating]
    except:
        vrr = 0
    return vrr


def f_find_end_balise(ma_chaine):

    """ cherche la premiere occurence caractere designé d'une balise >
    """
    k = ">"
    x = ma_chaine.find(k)
    y = ma_chaine[22:(x-1)]
    return y


def directory_results(category):
    """
creating file file name with the directory location of the file

    """
    #  my_csv_dir = 'C:\\projet_OPC\\oc02\\oc_projet02\\data\\test\\'
    my_csv_dir = '.\\data\\test\\'
    my_csv_file_name = 'scrap_book_'
    
    result_file = my_csv_dir + my_csv_file_name + category + '.csv'
    return result_file


def f_read_writing_book_csv_file2(mon_book_text):
    """
function to read & write the book informations into a csv file.
the csv separator is a ";" due to the string imported.
    """
    my_csv_file = 'C:\\projet_OPC\\oc02\\oc_v2_tg_prj02\\data\\scrap_book_by_cat.csv'
    with open(my_csv_file, "a", encoding='utf-8', newline='') as mon_book:
        mon_book_text_w = csv.writer(mon_book, delimiter=';')     
        mon_book_text_w.writerow([mon_book_text])


def f_test_nextpage(test_pageup):
    """
    """
    pageup_link = ""
    try:
        test_pageup2 = test_pageup.find_all("li", {"class": "next"})[0]

        if test_pageup2 != "" or not None:
            pageup_link = test_pageup2.find("a").attrs['href']
            return pageup_link
        else:
            return None

    except ValueError:
        print("pas de page supplémentaire ! rubrique suivante...")


def new_next_page_link(next_url, next_page):
    """

clean the url of the end to start while a "/" found
concatenation the "next page name" 
   
"""
    if next_page:
        i = 0
        for i in range(len(next_url)):
            
            car = next_url[-i]
            if car == "/":
                j = i-1
        
                new_next_url = next_url[:-j] + next_page
                break     
            i += 1
        return new_next_url if new_next_url else None
    
    else:
        return None, None


def scrap_category_page(page_url):
    """ 
        return the list of books page's url for the given 
        category page
    """
        soup, r_status = my_soup(page_url)
    books_urls = [
        a['href'].replace('../../../', page_url[:36])for a in 
        soup.select(".image_container > a")]

    next_a = soup.select_one('.next > a')
    
    return books_urls, next_a["href"] if next_a else None


def scrap_category_list(page_url):
    """
    return de list of categorys of books

    """
    soup, r_status = my_soup(page_url)

    category = soup.select('li > a')
    category1 = [a['href'].replace('../', page_url[:45]) for a in category]
    
    i = 0
    category2 = []
    for i in range(len(category1)-1):
        soup_1, statut_url = my_soup(category1[i])
        #  print(category1[i])
        #  print(i)
        if statut_url != 200:
            print(category1[i])
            print("erreur sur lien " + str(i))
            #  del(category1[i])
        elif statut_url == 200:
            category2.extend([category1[i]])   
            
        elif i == 0:
            break
        i += 1
    #  next_a = soup.select_one('.next > a')
    return category2


def create_csv_file(my_csv_file):
    """
creating csv files by personalized name of files
with head of columns
initalisation with head of columns

    """
    entetes = [
        "product_page_url",
        "title",
        "upc",
        "category",
        "number_available",
        "review_rating",
        "image_url",
        "price_including_tax",
        "price_excluding_tax",
        "product_description"
    ]
    f = open(my_csv_file, 'w')
    ligneEntete = ";".join(entetes) + "\n"

    f.write(ligneEntete)
    f.close()


    def download_picture(url, folder="image"):


    """
        download the picture file of the current book
        choosing the directory
        searching the name of the picture file
        copying the file into the directory

    """
    try:
        
        #  os.chdir('C:\\projet_OPC\\oc02\\oc_projet02\\' + folder + '\\')
        os.chdir('.\\' + folder + '\\')
    except IOError:
        pass
        
    i = 0
    name = url
    for i in range(len(url)):
        
        if url[-i] == "/":
            name = url[-i+1:]
            break
    i += 1

    with open(name, 'wb') as f:
        im = requests.get(url)
        f.write(im.content)
        #  print('Writing: ', name)

def main()
    
    """

    project 02 of openclassrooms learning session
    this projet has for mission to developp an application 
    to scrap a website http://books.toscrape.com/
    first  operation :  choose a book's page and scrap  defined words


        """
    book_cat_links = []
    list_cat_book_url = []
    list_all_cat =[]
    site_cible = "http://books.toscrape.com/"
    init_page_index = "index.html"

    category_section = "sequential-art_5"
    site_cible_category_url = site_cible + "catalogue/category/books_1/" + category_section + "/" + init_page_index
    # boot_cat_link catch the link of book into a category to scrap information
    #  in the book page
    print(len(book_cat_links))
    #  print (book_cat_links)
    i = 0

    list_all_cat = scrap_category_list(site_cible_category_url)]
    for i in range(len(list_all_cat)):
        site_cible = list_all_cat[i]
        while True:
            next_page_url = None
            
            if not site_cible:
                break
            else:
                books_list_url, next_page_url = scrap_category_page(site_cible)
                list_cat_book_url.extend(books_list_url)
                
            if not next_page_url:
                break
            else:
                # on prend url refaite de avec next_page_url
                site_cible = new_next_page_link(site_cible, next_page_url)
        j=0 # initialisation  pour permttre l'initialisation du csv
        f len(list_cat_book_url) > 1:
            for j in range(len(list_cat_book_url)):
                
                book_link_item = list_cat_book_url[j]
                #  print(book_link_item)

                book_writer, category, image_url = f_scrap_my_Book(book_link_item)
                #  print(book_writer)

                download_picture(image_url)
                my_file = directory_results(category)
                create_csv_file(my_file)

                f_read_writing_book_csv_file2(book_writer)
                j += 1
        i += 1
        list_cat_book_url[:] = []
        
    print("c'est la fin " + str(len(list_cat_book_url)))
    
    if __name__ == '__main__':
    main()