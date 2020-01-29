from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup

# the url to scrape from.
base_url = 'https://qisahn.com/pg/nintendo-nintendo-switch-games-brand-new'

# pretend to be a Mozilla Browser when using the url; this bypasses error 403.
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent':user_agent}

my_url = base_url   # set the url for the first page before the loop.
contents = []       # set an array to store the contents.

while True:
    
    # debug information.
    print("Retrieving: " + my_url)
    
    my_request = Request(my_url, None, headers)     # the request is to be made under the name of a Mozilla Browser.
    uClient = urlopen(my_request)                   # open a connection, grab the webpage.
    page_html = uClient.read()                      # offload the content into a variable.
    uClient.close()                                 # close the connection.

    # parse the HTML content.
    page_soup = BeautifulSoup(page_html, "html.parser")

    # grabs all the products and stores them in the contents array.
    contents += page_soup.findAll("div", {"class":"product-wrapper col-md-3 col-sm-4 col-xs-12"})

    # check if there is a next page.
    next_page = page_soup.find("li", {"class":"next_page"})
    if next_page:
        
        # break down the url to find the next page number.
        url_array = list(str(next_page.a))
        for char in url_array:
            if char.isdigit():
                next_page = str(char)
        
        # set the url to open the next page on the next loop.
        my_url = base_url + '?page=' + next_page
    
    # break the loop if there isn't a next page.
    else:
        print("Process completed!")
        break

# open a csv file and prepare to write on the file.
filename = "Qisahn_Products.csv"
f = open(filename, "w")

# write the respective headers on the csv file.
headers = "No., Product Name, Product Price\n"
f.write(headers)

# loop through all the products in the array.
for number, content in enumerate(contents):
        
    # retrieve and format the product names and prices.
    product_name = content.find("a", {"class":"product-name"}).text.strip()
    product_price = content.find("div", {"class":"product-price"}).text.strip()

    # write to the csv file.
    f.write(str(number + 1) + "," + product_name.replace(",", " |") + "," + product_price + "\n")

# close the csv file writer.
f.close()