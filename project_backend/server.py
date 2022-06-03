import json #importing json will allow us to import lists through JSON notation
from flask import Flask, abort
from about_me import me
from mock_data import catalog

app = Flask('Project')

@app.route("/", methods=["GET"]) #this is a decorator in python, the route will define an endpoint. the / means the root. The GET method means the user is trying to get something from the server
def home():
    return "This is the home page."

#Create an about endpoint and show your name
@app.route("/about", methods=["GET"]) #if no method is entered, by default it will be get.
def about():
    # return me["first"] + " " + me["last"]
    return f"{me['first' ]} {me['last']}"

@app.route("/myaddress")
def address():
    return f' {me["address"]["street"]} {me["address"]["number"]}' #this is a nested object

##########################################################################
##################### API ENDPOINTS #########################
################################################################
#Postman --> Tests endpoints of REST APIs

#the catalog that we are retrieving is just a python list of dictionaries.
@app.route("/api/catalog", methods=["GET"]) 
def get_catalog():
    return json.dumps(catalog) #the function dumps will convert some python object to json notation.

#make an endpoint to send back how many products we have in the catalog
@app.route("/api/catalog/count", methods=["GET"])
def get_count():
    #Here...count how many products are in the list catalog
    counts = len(catalog)

    return json.dumps(counts) #return the value

#Request 127.0.0.1:5000/api/product/1 (1 is the product _id here)
#instead of doing that for each product, it should be dynamic
#by using <id>, now anything we enter as the endpoint, will show up
@app.route("/api/product/<id>", methods=["GET"])
def get_product(id):
    #find the product whose _id is equal to id
    #travel mock_data with a for loop
    #get every product inside the list
    #if the _id of the product is equal to the id variable, found it.
    #return the product as json.
    for prod in catalog:
        if prod["_id"] == id:
            return json.dumps(prod)
    
    #return an error code
    return abort(404, "ID does not match any product")

#Create an endpoint that returns the SUM of all the products prices
@app.get("/api/catalog/total")
def get_total():
    total = 0
    for prod in catalog:
        # total = total + prod["price"]
        total += prod["price"]

    return json.dumps(total)

#get product by category
#get /api/products/<category>
@app.get("/api/products/<category>")
def products_by_category(category):
    results = []
    category = category.lower() #doing this only once is better than parsing a million times if adding the .lower() on the if statement below.
    for prod in catalog:
        if prod["category"].lower() == category: # == will always be case sensitive, the solution is to parse both sides to a common ground.
            results.append(prod)
    return json.dumps(results)
        
    return abort (404, "Category does not exist")


#get the list of categories
#get /api/categories
@app.get("/api/categories")
def get_categories():
    categories=[]
    for prod in catalog:
        cat = prod["category"]
        #if category doesn't already exist in results, then I will append.
        #google question: if a string exists inside a list in python
        if not cat in categories: #this line is checking if the list doesn't exist already, if i wanted to check if it does exist, i would use 'if cat in categories'
            categories.append(cat)

    return json.dumps(categories)

#get the cheapest product
@app.get("/api/products/cheapest")
def get_cheapest_product():
    solution = catalog[0] #usually here, we can use any number at random, it won't make a difference where we start.
    for prod in catalog:
        if prod["price"] < solution["price"]:
            solution = prod
    
    return json.dumps(solution)

@app.get("/api/exercise1")
def get_exe1():
    nums = [123,123,654,124,8865,532,4768,8476,45762,345,-1,234,0,-12,-456,-123,-865,532,4768]
    solution = {} #dictionary

    # A. find the lowest number
    solution["a"] = 1
    # B. find how many numbers are lowe than 500

    # C. sum all the negatives

    # D. findthe sum of numbers except negatives

    return json.dumps(solution)


app.run(debug=True)