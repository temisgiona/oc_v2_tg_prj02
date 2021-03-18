import csv
import os
import requests


def local_dir(folder):
    """

    find the local directory  and join
    the  folder nedeed for the link

    """
    root = os.path.dirname(__file__)
    rel_path = folder
    abs_path = os.path.join(root, rel_path)
    return abs_path


def directory_results(category, folder="data"):
    """
    creating file file name with the directory location of the file

    """
    my_csv_dir = 'data\\'
    my_csv_file_name = 'scrap_book_'

    result_file = my_csv_dir + my_csv_file_name + category + '.csv'
    return result_file


def read_writing_book_csv_file(csv_file, ma_liste):
    """
    function to read & write the book informations into a csv file.

    ma_ligne[] is a dictionnary
    the csv separator is a ";" due to the string imported.

    """
    abs_path = local_dir(csv_file)

    with open(abs_path, 'a', encoding='UTF-8-sig', newline='') as csvfile:

        writer = csv.DictWriter(
            csvfile,
            fieldnames=ma_liste.keys(),
            delimiter=";"
            )
        writer.writerow(ma_liste)


def create_csv_file(my_csv_file, ma_liste):
    """
creating csv files by personalized name of files
with head of columns
initalisation with head of columns

    """

    abs_path = local_dir(my_csv_file)

    f = open(abs_path, 'w')
    ligneEntete = ";".join(ma_liste.keys()) + "\n"

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

        abs_path = local_dir(folder)
        os.chdir(abs_path)

    except IOError:
        print("directory or file error !")
        pass

    name = (url.split('/'))[7]

    with open(name, 'wb') as f:
        im = requests.get(url)
        f.write(im.content)
