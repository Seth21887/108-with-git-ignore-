import json #importing json will allow us to import lists through JSON notation
from flask import Flask, abort, request
from about_me import me
from mock_data import catalog
from config import db
from bson import ObjectId

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
    results = []
    cursor = db.products.find({}) #get all the data from the collection

    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results) #the function dumps will convert some python object to json notation.

    

#POST Method to create new products
@app.route("/api/catalog", methods=["POST"])
def save_products():
    try:
        product = request.get_json()
        errors = ""    

        # make sure title exists in the product dictionary, if not, return bad request
        #5 characters long, if shorter, show error
        if not "title" in product or len(product["title"]) < 5:
            errors = "Title is required and should have at least 5 characters."

        # must have an image
        if not "image" in product:
            errors += "Image is required"

        #must have a price, the price should be greater/equal to 1
        if not "price" in product or product["price"] < 1:
            errors += "Price is required and should be >= 1"

        if errors:
            return abort(400, errors)

        db.products.insert_one(product)

        product["_id"] = str(product["_id"])

        return json.dumps(product)
    except Exception as ex:
        return abort(500, F"Unexpected error: {ex}")


#make an endpoint to send back how many products we have in the catalog
@app.route("/api/catalog/count", methods=["GET"])
def get_count():
    cursor = db.products.find({})
    num_items = 0
    for prod in cursor:
        num_items += 1
    #Here...count how many products are in the list catalog
    # counts = len(catalog)

    return json.dumps(num_items) #return the value

#Request 127.0.0.1:5000/api/product/1 (1 is the product _id here)
#instead of doing that for each product, it should be dynamic
#by using <id>, now anything we enter as the endpoint, will show up
@app.route("/api/product/<id>", methods=["GET"])
def get_product(id):
    try:
        if not ObjectId.is_valid(id):
            return abort(400, "Invalid ID")

        product = db.products.find_one({"_id": ObjectId(id)})

        if not product:
            return abort(404, "Product not found")

        product["_id"] = str(product["_id"])
        return json.dumps(product)
    
    #instead of crashing, using a try-except will just do what you want it to do when an invalid id is entered.
    except:
        return abort(500, "Unexpected error")
    #find the product whose _id is equal to id
    #travel mock_data with a for loop
    #get every product inside the list
    #if the _id of the product is equal to the id variable, found it.
    #return the product as json.
    # for prod in catalog:
    #     if prod["_id"] == id:
    #         return json.dumps(prod)
    
    #return an error code
    # return abort(404, "ID does not match any product")

#Create an endpoint that returns the SUM of all the products prices
@app.get("/api/catalog/total")
def get_total():
    total = 0
    cursor = db.products.find({})
    for prod in cursor:
        # total = total + prod["price"]
        total += prod["price"]

    return json.dumps(total)

#get product by category
#get /api/products/<category>
@app.get("/api/products/<category>")
def products_by_category(category):
    results = []
    cursor = db.products.find({"category": category})

    # category = category.lower() #doing this only once is better than parsing a million times if adding the .lower() on the if statement below.
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)
        # if prod["category"].lower() == category: # == will always be case sensitive, the solution is to parse both sides to a common ground.
        #     results.append(prod)
    return json.dumps(results)
        
    return abort (404, "Category does not exist")


#get the list of categories
#get /api/categories
@app.get("/api/categories")
def get_categories():
    cursor = db.products.find({})
    categories=[]
    for prod in cursor:
        cat = prod["category"]
        #if category doesn't already exist in results, then I will append.
        #google question: if a string exists inside a list in python
        if not cat in categories: #this line is checking if the list doesn't exist already, if i wanted to check if it does exist, i would use 'if cat in categories'
            categories.append(cat)

    return json.dumps(categories)

#get the cheapest product
@app.get("/api/products/cheapest")
def get_cheapest_product():
    cursor = db.products.find({})
    solution = cursor[0] #usually here, we can use any number at random, it won't make a difference where we start.
    for prod in cursor:
        if prod["price"] < solution["price"]:
            solution = prod
    
    solution["_id"] = str(solution["_id"])
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


#####################################################COUPON CODES ####################################################

#get all
@app.route("/api/coupons", methods=["GET"])
def get_all_coupons():
    cursor = db.coupons.find({})
    results = []
    for cc in cursor:
        cc["_id"] = str(cc["_id"])
        results.append(cc)

    return json.dumps(results)

#save coupon code
@app.route("/api/coupons", methods=["POST"])
def save_coupon():
    coupon = request.get_json()

    #validations
    #discount must be between 1 and 50%
    #code should have at least 5 characters
    if not "code" in coupon or len(coupon["code"]) < 5:
        return abort(400, "Coupon should have at least 5 chars")

    if not "discount" in coupon or coupon["discount"] < 1 or coupon["discount"] > 50:
        return abort(400, "Discount is required and should be between 1 and 50")

    #do not allow duplicate code
    #query database to see if there is an object with the same code, if there is return an error, otherwise save.
    exist = db.coupons.find_one({"code"})
    if exist:
        return abort(400, "A coupon already exists for that code")

    db.coupons.insert_one(coupon)

    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)

#get CC by code
@app.route("/api/coupons/<code>", methods=["GET"])
def get_coupons_by_code(code):

    coupon = db.coupons.find_one({"code": code})
    if not coupon:
        return abort(404,"Coupon not found")

    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)


app.run(debug=True)