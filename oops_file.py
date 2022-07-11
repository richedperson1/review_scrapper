# import requests
import pymongo
from bs4 import BeautifulSoup as bs
from dataclasses import dataclass
from urllib.request import urlopen as uReq


@dataclass
class fetching_info:
    search_obj: str
    list_of_element: str
    flipkart = "https://www.flipkart.com/search?q="
    # client = pymongo.MongoClient(
    #     "mongodb+srv://mongodb:ru15070610@cluster0.4olre.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    # db = client.test

    def search_obj_url(self, index=0) -> str:
        """
        Selecting first rank product when search some product's
        When can select any box/rank of search product by just changing index number

        """
        try:
            flipkart_link = self.flipkart+self.search_obj.replace(",", "")
            uClien = uReq(flipkart_link)
            uClient = uClien.read()
            uClien.close()
            flipkart_soup = bs(uClient, "html.parser")
        except Exception as e:
            print("Error at url side search_obj_url ")
            print(e)

        try:
            all_search_object = flipkart_soup.find_all(
                "div", {"class": self.list_of_element})

            del all_search_object[:3]

            actual_url = flipkart_link+all_search_object[index].a['href']

            return actual_url
        except Exception as e2:
            print("Error at searching side")
            print(e2)

    def getting_info_of_one(self) -> list:
        """
        Through this function Product title , Price of that product is to scrapped 
        """
        try:
            single_search_obj_url = self.search_obj_url()
            single_uclient1 = uReq(single_search_obj_url)
            single_uclient = single_uclient1.read()
            flipkart_soup = bs(single_uclient, "html.parser")
            single_uclient1.close()
        except Exception as ghe:
            print("Error at url side getting_info_of_one")
            print(ghe)

        try:

            self.heading_of_obj = flipkart_soup.find_all(
                "h1", {"class": "yhB1nd"})[0].text

            self.price_of_product = flipkart_soup.find_all(
                'div', {'class': "_30jeq3 _16Jk6d"})[0].text

            self.dist2 = {"price_of_product": self.price_of_product,
                          "describe_product_short": self.heading_of_obj}
            return [self.heading_of_obj, self.price_of_product]

        except Exception as ghe1:

            print("Error at heading(searching object heading) side")
            print(ghe1)
            # return ghe1

    def getting_info_of_all(self):
        """
        In this function comments on the Product ,rating of product for each customers ,headline of product ,Purchase date of search product's
        is scrapped on real time ! 
        """
        try:
            single_search_obj_url = self.search_obj_url()
            single_uclient1 = uReq(single_search_obj_url)
            single_uclient = single_uclient1.read()
            flipkart_soup = bs(single_uclient, "html.parser")
            single_uclient1.close()
            self.getting_info_of_one()
            self.dist2 = {"describe_product_short": self.heading_of_obj,
                          "price_of_product": self.price_of_product}

        except Exception as gre:
            print("Error at url side getting_info_of_all")
            print(gre)
            # return gre
        try:
            ratings = []
            comments = []
            heading_of_comments = []
            purchase_time = []
            data_stored_mongodb = []
            object_rating = flipkart_soup.find_all(
                "div", {"class": "_16PBlm"})
            all_material = object_rating
            iteration = len(object_rating)
            for i in range(iteration-1):
                rating_of_product = all_material[i].find(
                    "div", {"class": "_3LWZlK _1BLPMq"}).text

                headline_of_product = all_material[i].find_all("p")[0].text
                # name_of_customer = all_material[i].find_all("p")[1].text
                purchase_date = all_material[i].find_all("p")[3].text

                comment = all_material[i].find(
                    'div', {"class": "t-ZTKy"}).div.div.text

                comments.append(comment)
                ratings.append(rating_of_product)
                heading_of_comments.append(headline_of_product)
                purchase_time.append(purchase_date)

                self.dist1 = {"name_of_search_product": self.search_obj, "user_comment": comment,
                              "review_headline": headline_of_product, "rating": rating_of_product, "purchase_date": purchase_date}

                update_one = dict(self.dist2, **self.dist1)
                data_stored_mongodb.append(update_one)

            # connection = self.client["review_scapper_data"]
            # collection = connection['flipkart_data']
            # collection.insert_many(data_stored_mongodb)
            return [heading_of_comments, ratings, comments, purchase_time]

        except Exception as gre1:
            print(gre1)
            # return gre1
