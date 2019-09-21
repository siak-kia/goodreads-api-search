#! /usr/bin/python


import requests

import xml.etree.ElementTree as ET


class GoodReadsAPISearch:

    GOODREADS_URL = "https://www.goodreads.com/search/index.xml"
    API_KEY = "key"

    def __init__(self, book_title):
        self.book_title = book_title

    def find_top_rated_books(self, number_of_pages):
        print (number_of_pages)
        for i in range(1 , number_of_pages + 1):
            url = self.GOODREADS_URL+ "?search%5Bfield%5D=title&page=" + str(i) + "&"
            response = requests.request("GET", url + "&" + "key=" + self.API_KEY + "&q=" +  self.book_title)
            with open("elon_books" + str(i) + ".xml", 'wb') as f:
                f.write(response.content)

            self.parseXMLToFindGoodRatedBooks("elon_books" + str(i) + ".xml")



    def find_the_number_of_result_pages(self):


            url = self.GOODREADS_URL + "?search%5Bfield%5D=title&page=1&"
            response = requests.request("GET", url + "&" + "key=" + self.API_KEY + "&q=" +  self.book_title)
            with open('elon_books.xml', 'wb') as f:
               f.write(response.content)

            total_results = self.parseXMLToFindNumPages("elon_books.xml")

            number_of_pages= (total_results // 20) + 1
            print(f"number_of_pages", number_of_pages)
            return number_of_pages

    def parseXMLToFindNumPages(self, xmlfile):

            # create element tree object
            tree = ET.parse(xmlfile)
            root = tree.getroot()

            for child in root:
                #print (child)
                if child.tag == "search":
                    for item in child.iter():
                        if item.tag == "total-results":
                            return int(item.text)

    def parseXMLToFindGoodRatedBooks(self, xmlfile):
            # create element tree object
            tree = ET.parse(xmlfile)
            root = tree.getroot()

            for child in root:
                if child.tag == "search":
                    for item in child.iter():

                        if item.tag == "results":
                            average_rating = 0
                            rating_count = 0
                            title = ""
                            for h in item.iter():
                                if h.tag == "average_rating":
                                    average_rating = float(h.text)

                                if h.tag == "ratings_count":
                                    rating_count = int(h.text)
                                if h.tag == "title":
                                    title = h.text
                                    if average_rating > 4 and rating_count > 50:
                                        print(title,average_rating, rating_count)
                                    average_rating = 0
                                    rating_count = 0

def main():
    elon_musk_search = GoodReadsAPISearch("elon musk")
    number_of_pages = elon_musk_search.find_the_number_of_result_pages()
    elon_musk_search.find_top_rated_books(number_of_pages)

if __name__ == "__main__":
    main()

