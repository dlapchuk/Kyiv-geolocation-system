    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
from datetime import datetime, date, time
import xml.etree.ElementTree as et
from bson import ObjectId
from pymongo import MongoClient
from bson.code import Code
import fillDB
import os
import datetime

client = MongoClient()
dbm  = client['Course']

def findPlaces(sort, distr, type):
    rows = []
    print distr
    if(sort=="name"):
        if(distr=="All"):
            if(type=="All"):
                places = dbm.Places.find({}).sort('name')
            else:
                pl_type = dbm.Type.find_one({'name' : type})
                places = dbm.Places.find({'type_id' : pl_type['_id']}).sort('name')
        else:
            if(distr=="nearest"):
                if(type=="All"):
                    places = dbm.Places.find({})
                else:
                    type = dbm.Type.find_one({'name' : type})
                    places = dbm.Places.find({'type_id' : type['_id']}).sort('name')
            else:
                pl_distr = dbm.District.find_one({'name' : distr})
                if(type=="All"):
                    places = dbm.Places.find({'distributor_id':pl_distr['_id']}).sort('name')
                else:
                    pl_type = dbm.Type.find_one({'name' : type})
                    places = dbm.Places.find({'type_id' : pl_type['_id'], 'distributor_id':pl_distr['_id']}).sort('name')
    else:
        if(distr=="All"):
            if(type=="All"):
                places = dbm.Places.find({}).sort('rating', -1)
            else:
                pl_type = dbm.Type.find_one({'name' : type})
                places = dbm.Places.find({'type_id' : pl_type['_id']}).sort('rating', -1)
        else:
            if(distr=="nearest"):
                if(type=="All"):
                    places = dbm.Places.find({})
                else:
                    type = dbm.Type.find_one({'name' : type})
                    places = dbm.Places.find({'type_id' : type['_id']}).sort('rating', -1)
            else:
                pl_distr = dbm.District.find_one({'name' : distr})
                if(type=="All"):
                    places = dbm.Places.find({'distributor_id':pl_distr['_id']}).sort('rating', -1)
                else:
                    pl_type = dbm.Type.find_one({'name' : type})
                    places = dbm.Places.find({'type_id' : pl_type['_id'], 'distributor_id':pl_distr['_id']}).sort('rating', -1)


    #if(sort == "name"):
    #    places = dbm.Places.find({}).sort('name')
    #else:
    #    if(sort=="rating"):
    #        places = dbm.Places.find({}).sort('rating', -1)
    #    else:
    #        places = dbm.Places.find({})
    for place in places:
        place['type_id'] = dbm.Type.find_one({'_id' : place['type_id']},{'_id':0,'name':1})['name']
        place['distributor_id'] = dbm.District.find_one({'_id' : place['distributor_id']},{'_id':0,'name':1})['name']
    #    place['distributor_id'] = dbm.District.find_one({'_id' : place['distributor_id']},{'_id':0,'name':1})['name']
    #    sale['product_id'] = dbm.product.find_one({'_id' : sale['product_id']},{'_id':0,'name':1})['name']
        rows.append(place.values())
    return rows

def findFavorite(user):
    rows = []

    name_id = dbm.Users.find_one({'name': user}, {'_id':1})['_id']
    places = dbm.Favorite.find({'name_id': name_id}).sort("mark")

    for place in places:
        place['name'] = dbm.Places.find_one({'_id' : place['place_id']},{'_id':0,'name':1})['name']

        rows.append(place.values())
    return rows


def clearFacts():
    dbm.sales.remove({})

def getNearest(number):
    rows = []
    place = dbm.Places.find_one({'_id': ObjectId(number)})
    longitude = place['location']['coordinates'][0]
    latitude = place['location']['coordinates'][1]
    nearest = dbm.Places.find({'location': {'$near':{'$geometry' :{'type' : 'Point', 'coordinates': [longitude, latitude]} }}}).limit(5)
    for one in nearest:
        if(place['_id'] != one['_id']):
            rows.append(one.values())
        else:
            print 'get yaaaaaaaaaaaaaaaa!!!!!!!!!!!!!'
    return rows

def getComments(number):
    rows = []
    place = dbm.Places.find_one({'_id': ObjectId(number)})
    comments = dbm.Comment.find({'place_id': place['_id']})
    for comment in comments:
        comment['name_id'] = dbm.Users.find_one({'_id' : comment['name_id']},{'_id':0,'name':1})['name']
        rows.append(comment.values())
    return rows

def getShow(number, user):
    rows = []
    place = dbm.Places.find_one({'_id': ObjectId(number)})
    place['type_id'] = dbm.Type.find_one({'_id' : place['type_id']},{'_id':0,'name':1})['name']
    place['distributor_id'] = dbm.District.find_one({'_id' : place['distributor_id']},{'_id':0,'name':1})['name']
    if(user):
        name_id = dbm.Users.find_one({'name': user}, {'_id':1})['_id']
    #name_id = dbm.Users.find_one({'name': user}, {'_id':1})['_id']
    place['longitude']= place['location']['coordinates'][0]
    place['latitude']= place['location']['coordinates'][1]
    check = None
    if(user):
        check = dbm.Favorite.find_one({'place_id': place['_id'], 'name_id' : name_id})
    if(check):
        place['adres'] = check['mark']
        place['nazvanie'] = str("/dbSearch/deleteFavorite/")
    else:
        place['adres'] = str("Add")
        place['nazvanie'] = str("/dbSearch/addFavorite/")

    rows.append(place.values())
    return rows

def fillDatabase():
    tree = et.parse("dbSearch/xmlFiles/dbxml.xml")
    root= tree.getroot()
    fillDB.clearTables(dbm)
    fillDB.fillCustomer(dbm,root)
    fillDB.fillDistributor(dbm,root)
    fillDB.fillProduct(dbm,root)
    fillDB.fillSales(dbm,100)

def sendMessage(user, number, message):
    name_id = dbm.Users.find_one({'name' : user}, {'_id':1})['_id']
    dbm.Comment.insert({
        'name_id': name_id,
        'place_id': ObjectId(number),
        'text': message,
        'date': datetime.datetime.utcnow()
    })

def getPlaceID(number):
    print number
    comment = dbm.Comment.find_one({'_id': ObjectId(number)})
    print "BBBBBBBBBBBBBBBBBBBBBBBB"
    print comment['_id']
    print "AAAAAAAAAAAAAAAAAAAA"
    print comment['text']
    return comment['place_id']

def getPlaceIDbyMark(number):
    comment = dbm.Favorite.find_one({'_id': number})
    return comment['place_id']

def makeDump():
    os.system("mongodump --host 127.0.0.1 --db Course")

def makeRestore():
    os.system("mongorestore --db Course --drop dump/Course")

def getPlaces(sort):
    rows = []
    if(sort == "name"):
        places = dbm.Places.find({}).sort('name')
    else:
        if(sort=="rating"):
            places = dbm.Places.find({}).sort('rating', -1)
        else:
            places = dbm.Places.find({})
    for place in places:
        place['type_id'] = dbm.Type.find_one({'_id' : place['type_id']},{'_id':0,'name':1})['name']
        place['distributor_id'] = dbm.District.find_one({'_id' : place['distributor_id']},{'_id':0,'name':1})['name']
    #    place['distributor_id'] = dbm.District.find_one({'_id' : place['distributor_id']},{'_id':0,'name':1})['name']
    #    sale['product_id'] = dbm.product.find_one({'_id' : sale['product_id']},{'_id':0,'name':1})['name']
        rows.append(place.values())
    return rows



def getPlace(number):
    rows = []
    place = dbm.Places.find_one({'_id': ObjectId(number)})
    place['type_id'] = dbm.Type.find_one({'_id' : place['type_id']},{'_id':0,'name':1})['name']
    place['distributor_id'] = dbm.District.find_one({'_id' : place['distributor_id']},{'_id':0,'name':1})['name']
    place['longitude']= place['location']['coordinates'][0]
    place['latitude']= place['location']['coordinates'][1]
    rows.append(place.values())
    return rows

def deletePlace(number):
    comments = dbm.Comment.find({'place_id': ObjectId(number)})
    for comment in comments:
        dbm.Comment.remove({'_id': comment["_id"]})
    favorites = dbm.Favorite.find({'place_id': ObjectId(number)})
    for favorite in favorites:
        dbm.Favorite.remove({'_id': favorite["_id"]})
    dbm.Places.remove({'_id': ObjectId(number)})


def deleteMessage(number):
    dbm.Comment.remove({'_id': ObjectId(number)})
#Done
def getTypes():
    names=[]
    rez = dbm.Type.find(None,{'name': 1,'_id':0})
    for i in rez:
        names.append(i['name'])
    return names
#Done
def getDistricts():
    names=[]
    rez = dbm.District.find(None,{'name': 1,'_id':0})
    for i in rez:
        names.append(i['name'])
    return names
#Done
def getProducts():
    names=[]
    rez = dbm.product.find(None,{'name': 1,'_id':0})
    for i in rez:
        names.append(i['name'])
    return names

def updatePlace(number,distr,type,name, image, longitude, latitude, description):
    type_id = dbm.Type.find_one({'name' : type},{'_id': 1})['_id']
    distr_id = dbm.District.find_one({'name' : distr},{'_id':1})['_id']

    dbm.Places.update({'_id': ObjectId(number)},
                      {'$set':
                           {'type_id': type_id,
                            'distributor_id': distr_id,
                            'name': name,
                            'image':image,
                            'location':{
                                'coordinates':[longitude, latitude],
                                'type' : 'Point'
                            },
                            'description':description }
                       })

#Done
def addPlace(distr,type,name,image,longitude,latitude,description):
    type_id = dbm.Type.find_one({'name' : type},{'_id': 1})['_id']
    distr_id = dbm.District.find_one({'name' : distr},{'_id':1})['_id']
    dbm.Places.insert({
        'name': name,
        'type_id': type_id,
        'location':{
        'coordinates':
            [longitude,latitude],
        'type' : 'Point'
        },
        'distributor_id': distr_id,
        'description':description,
        'image':image,
        'rating': 0.00
    })

def addFavorite(number, user, mark):
    name_id = dbm.Users.find_one({'name' : user}, {'_id':1})['_id']
    dbm.Favorite.insert({
        'name_id': name_id,
        'mark': mark,
        'place_id': ObjectId(number)
    })

def deleteFavorite(number, user):
    name_id = dbm.Users.find_one({'name' : user}, {'_id':1})['_id']
    fav_id = dbm.Favorite.find_one({'place_id' : ObjectId(number),'name_id': name_id},  {'_id': 1})['_id']
    dbm.Favorite.remove({'_id': fav_id})

def getCustStat():
    map =   Code("function(){"
                    "emit(this.place_id,{mark_count: this.mark, count: 1});}"
                )
    reduce = Code("function(key,values){"
                    "var sum=0;"
                    "var count=0;"

                    "for(var i in values){"
                    "sum+=values[i].mark_count;"
                    "count += values[i].count;}"
                    "return {mark_count: sum, count: count}};"
                  )
    finalize = Code("function(key, reduceValue){"
                    "return reducedValue.mark_count / reducedValue.count;")
    dbm.Favorite.map_reduce(map,reduce,'customerStats')

    rows = []
    custs = dbm.customerStats.find({})
    for pl in custs:
        rating = pl['value']['mark_count']/pl['value']['count']
        dbm.Places.update({'_id': pl['_id']},{'$set': {'rating': rating} })
        pl['_name'] = dbm.Places.find_one({'_id' : pl['_id']},{'_id':0,'name':1})['name']
        pl['middle'] = rating
        pl['count'] = pl['value']['count']
        rows.append(pl.values())
    return rows

def getProdStat():
    map =   Code(   "function(){"
                    "var key = {product: this.product_id, year: this.date.getFullYear()};"
                    "emit(key,this.quantity);}"
                )

    reduce = Code("function(key,values){"
                    "var sum=0;"
                    "for(var i in values)"
                    "sum+=values[i];"
                    "return sum};"
                  )
    dbm.sales.map_reduce(map,reduce,'productStats')
    rows = []
    prods = dbm.productStats.find({})
    for prod in prods:
        values = []
        values.append(dbm.product.find_one({'_id' : prod['_id']['product']},{'_id':0,'name':1})['name'])
        values.append(int(prod['_id']['year']))
        values.append(int (prod['value']))
        rows.append(values)
    return rows










