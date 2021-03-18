from booktoscrap import scrap_my_Book, scrap_category_page
from booktoscrap import scrap_category_list, new_next_page_link
from file_creation import download_picture, directory_results
from file_creation import create_csv_file, read_writing_book_csv_file


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
