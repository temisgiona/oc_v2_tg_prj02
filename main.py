
import requests
from bs4 import BeautifulSoup
import os
from file_creation import local_dir, directory_results
from file_creation import create_csv_file, read_writing_book_csv_file


def my_soup(page_url):
    """
funtion to create the soup with webiste target in argument
choose the link to scrap
"""
    try:
        resp = requests.get(page_url)
        r_status = resp.status_code
        resp.encoding = 'utf8'

    except Exception:
        print('erreur sur le lien')
        r_status = 505
    soup = ""
    if r_status == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')

    return soup if soup else None, r_status


def scrap_my_Book(book_target):
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
    ma_ligne = {}
    soup, r_status = my_soup(book_target)
    
    title = (soup.title.string)[5:-28]
    ma_ligne["title"] = title.strip("/n")

    number_available = soup.find("div", {"class": "col-sm-6 product_main"}).find("p", {"class": "instock availability"}).text[25:27]
    ma_ligne["number available"] = str(number_available)

    upc = soup.find("table", {"class": "table table-striped"}).find("td")
    ma_ligne["upc"] = upc.text

    price_incl_tax = soup.find_all('td')[3].text[2:]
    ma_ligne["price incl tax"] = str(price_incl_tax)

    price_excl_tax = soup.find_all('td')[2].text[2:]
    ma_ligne["price excl tax"] = str(price_excl_tax)

    product_description = soup.find_all('p')[3].text
    ma_ligne["product description"] = product_description.strip('\n')

    category = soup.find_all('li')[2].text[1:]
    ma_ligne["category"] = category.strip('\n')

    image_url = soup.find_all('img')[0]
    image_url = image_url.attrs['src']
    ma_ligne["image url"] = book_target[:26] + image_url[6:]

    review_rating = soup.find('p', attrs={"star-rating"})['class'][1]
    ma_ligne["review rating"] = conversion_rating(review_rating)
    
    ma_ligne["product page url"] = book_target


    return ma_ligne


def conversion_rating(v_review_rating):
    """convert the word extract from rating review to a number more explicit
example  : dectecting the word five , if 'five' --> vrr =5
the range is 0--> 5
    """
    dict_rating = {
        "Zero": "0",
        "One": "1",
        "Two": "2",
        "Three": "3",
        "Four": "4",
        "Five": "5"
        }
    try:
        vrr = dict_rating[v_review_rating]
    except:
        vrr = "0"
        print("the rating is missing or not found")
    return vrr


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


def new_next_page_link2(next_url, next_page):
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
        return books_urls
    """
    soup, r_status = my_soup(page_url)
    books_urls = [
        a['href'].replace('../../../', page_url[:36])
        for a in soup.select(".image_container > a")
        ]

    next_a = soup.select_one('.next > a')

    return books_urls, next_a["href"] if next_a else None


def scrap_category_list(page_url):
    """
    return one item of the list of book's categorys

    """
    soup, r_status = my_soup(page_url)

    category = soup.select('li > a')
    category1 = [a['href'].replace('../', page_url[:45]) for a in category]

    category2 = []
    for i in range(len(category1)-1):
        soup_1, statut_url = my_soup(category1[i])
 
        if statut_url != 200:
            print(category1[i])
            print("erreur sur lien " + str(i))

        elif statut_url == 200:
            category2.extend([category1[i]])

        elif i == 0:
            break
        i += 1

    return category2


def download_picture(url, folder="image"):
    """
    download the picture file of the current book
    choosing the directory
    searching the name of the picture file
    copying the file into the directory

    """
    try:

        abs_path = local_dir(folder)
        os.chdir(abs_path)

    except IOError:
        print("directory or file error !")
        pass

    name = (url.split('/'))[7]

    with open(name, 'wb') as f:
        im = requests.get(url)
        f.write(im.content)


def main():
    """

    project 02 of openclassrooms learning session
    this projet has for mission to developp an application
    to scrap a website http://books.toscrape.com/
    first  operation :  choose a book's page and scrap  defined words

        """
    book_cat_links = []
    list_cat_book_url = []
    list_all_cat = []

    site_cible = "http://books.toscrape.com/"
    init_page_index = "index.html"

    site_cible_category_url = site_cible + "catalogue/category/books_1/"
    site_cible_category_url = site_cible_category_url + init_page_index
    print(len(book_cat_links))

    list_all_cat = scrap_category_list(site_cible_category_url)

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
                site_cible = new_next_page_link(site_cible, next_page_url)
        j = 0  # initialisation  pour permettre l'initialisation du csv
        if len(list_cat_book_url) > 0:
            for j in range(len(list_cat_book_url)):

                book_link_item = list_cat_book_url[j]

                ma_ligne = scrap_my_Book(book_link_item)

                download_picture(ma_ligne["image url"])
                my_file = directory_results(ma_ligne["category"])
                if j == 0:
                    create_csv_file(my_file, ma_ligne)

                read_writing_book_csv_file(my_file, ma_ligne)
                j += 1
        i += 1
        list_cat_book_url[:] = []

    print("This is the end of scrap session")


if __name__ == '__main__':
    main()
