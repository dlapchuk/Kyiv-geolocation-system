import xml.etree.ElementTree as et
import MySQLdb
from datetime import timedelta
import datetime
from pymongo import MongoClient
from random import randint


def random_date(start, end):
    return start + timedelta(
        seconds=randint(0, int((end - start).total_seconds())))

def clearTables(db):
    db.customer.remove({})
    db.distributor.remove({})
    db.product.remove({})
    db.sales.remove({})

def fillCustomer(db,root):
    raw={}
    for table in root.iter('customer'):
        for dat in table:
            raw[dat.tag]=dat.text
        db.customer.insert(raw)
        raw={}

def fillDistributor(db,root):
    raw={}
    for table in root.iter('distributor'):
        for dat in table:
            raw[dat.tag]=dat.text
        db.distributor.insert(raw)
        raw={}

def fillProduct(db,root):
    raw={}
    for table in root.iter('product'):
        for dat in table:
            raw[dat.tag]=dat.text
        db.product.insert(raw)
        raw={}
# number: the number of sales to generate
def fillSales(db,number):
    for i in range(1,number):
        prod = db.product.find(None,{'_id':1,'price':1}).limit(-1).skip(randint(0,4)).next()
        cust = db.customer.find(None,{'_id':1}).limit(-1).skip(randint(0,4)).next()
        distr = db.distributor.find(None,{'_id':1}).limit(-1).skip(randint(0,4)).next()
        date = random_date(datetime.datetime(2010,1,1,0,0,0),datetime.datetime.now())
        amount = randint(1,7)
        sum = int(prod['price'])*amount
        db.sales.insert({
            'customer_id':cust['_id'],
            'quantity': amount,
            'sum':sum,
            'date': date,
            'product_id' :prod['_id'],
            'distributor_id':distr['_id']
        })















