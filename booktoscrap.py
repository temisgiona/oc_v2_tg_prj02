import requests
from bs4 import BeautifulSoup


def my_soup(page_url):
    """
funtion to create the soup with website target in argument
choose the link to scrap with beautifulsoup4
"""
    try:
        resp = requests.get(page_url)
        r_status = resp.status_code
        resp.encoding = 'UTF-8'

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
    product_page_url,upc,title,price_including_tax,price_excluding_tax,
    number_available,product_description, category, review_rating, 
    image_url ,  in a dict ma_ligne. 

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
    except ValueError:
        vrr = "0"
        print("the Value rating is missing or not found")
    return vrr


def new_next_page_link(next_url, next_page):
    """
    clean the url of the end to start while a "/" found
    concatenation the full correct link of "next page name"
    pick the base link and join the name of next page link.
    """
    if next_page:
        url = next_url.split('/')[:7]
        url = "/".join(url) + "/"
        new_next_url = url + next_page
        return new_next_url if new_next_url else None
    else:
        return None, None


def scrap_category_page(page_url):
    """
        return the list of books page's url for the given
        category page
        return  books_urls[] in a page
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
            print("si les erreurs persistent, verifier la connection internet")

        elif statut_url == 200:
            category2.extend([category1[i]])

        elif i == 0:
            break
        i += 1

    return category2
