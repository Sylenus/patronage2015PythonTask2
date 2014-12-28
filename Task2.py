import json  
import csv
import os
import ast
import pymongo
from pymongo import Connection

class Parser():      
   def __init__(self):

      dbCreated = False
      data = self.takeDataFromCSV()
      print ("Data from CSV file readed correctly")

      while True:
         print("Press 1 to save Json file")
         print("Press 2 to insert Json data to MongoDB")
         print("Press 3 to update record in database")
         print("Press 4 to delete record in database")
         print("Press 5 to tell a joke!")
         print("Press 6 to exit")
         try:
            choise = input('Select operation: ')
            choise = int(choise)
            if choise == 1:
               self.createJsonFile(data)
            elif choise == 2:
               self.insertIntoDB(data)
               dbCreated = True
            elif choise == 3:
               connection = Connection('localhost', 27017)
               dbNamesList = connection.database_names()
               if ("pb" in dbNamesList):
                  db = connection["pb"] 
                  collectionList = db.collection_names()
                  if ("pb_collection" in collectionList):
                     self.updateRecordInDB()
                  else:
                     print("Create collection first, by using option 2 in main manu")
               else:
                  print("Create database first, by using option 2 in main manu")
            elif choise == 4:
               try:
                  self.deleteRecordInDB()
               except Exception, e:
                  ("Unknown error, please conntact with provider. Error content: ", e)
            elif choise == 5:
               self.tellJoke()
          
            elif choise == 6:
               print("Bye, bye")
               break
            else:
               print("Error, plis enter 1,2 or 3 a")
         except Exception, e:
            print("Error, plis enter 1,2 or 3 b. Error: ", e)

   def takeDataFromCSV(self):
      try:
         try:
            #Open csv file
            f = open('Csv.csv', 'rU')  

            # Create 2 readers, one for keys, second for take keys argument
            readerForKey = csv.DictReader(f)
            reader = csv.DictReader(f, readerForKey.fieldnames)

            # Destroy readerForKey, no more needed 
            readerForKey = None
         
            #create and fill variable in json format
            toChange = json.dumps( [ row for row in reader ] )   
            toSave = toChange[1:-1]
            return toSave

         except Exception:
            print("Error, can't open file. Csv file need to be in the same folder")
            return None
      except Exception:
         print("Unknown error, please contact with provider ", Exception)
         return None

   def createJsonFile(self, data):
      try:
         try:
            #Creating json file
               f = open( 'jsonFile.json', 'w')  
               #Save json file
               f.write(data)  
               print "File saved, all works fine!"  
         except Exception:
            print("Problem with saving file, check local system permissions. Error: ", Exception)
      except Exception:
         print("Unknown error, please contact with provider. Error: ", Exception)

   def insertIntoDB(self,data):
      try:
         dataToSave = ast.literal_eval(data)
         client = pymongo.MongoClient()
         db = client.pb
         db.pb_collection.drop()
         pb_collection = db.pb_collection

         index = 1
         for row in dataToSave:
            row['id'] = index
            post_id = pb_collection.insert(row)
            post_id
            index += 1

         print ("Data inserted into DB")
      except Exception, e:
         ("Unknown error, please conntact with provider. Error content: ", e)
   def updateRecordInDB(self):
      try:
         while True:
            try:
               nameInRecrod = ["City", "Name", "Country", "Price", "Longitude", "State", "Transaction_date", "Last_Login", "Payment_Type", "Latitude", "Account_Created"]
               print ("Select record for update(1-100) any other action will take you back to main menu")
               index = input()
               if (0 < index < 101):
                  print ("select data to update from the list(write full word): ")
                  print (nameInRecrod)
                  nameInRecordForUpdate = raw_input()

                  if (nameInRecordForUpdate in nameInRecrod):
                     print ("Write new value: ")
                     newValue = raw_input()
                     client = pymongo.MongoClient()
                     db = client.pb
                     pb_collection = db.pb_collection
                     pb_collection.update({'id': index },{'$set':{nameInRecordForUpdate : newValue }},True, False)
                     print("Field updated")
                     break
            except:
               ("Record need to be a number")
      except Exception, e:
         ("Unknown error, please conntact with provider. Error content: ", e)

   def deleteRecordInDB(self):
      try:
         while True:
            print ("Select record for delete(1-100) any other action will take you back to main menu")
            index = input()
            if (0 < index < 101):
               client = pymongo.MongoClient()
               db = client.pb
               pb_collection = db.pb_collection
               pb_collection.remove({'id': index })
               print("Record deleted")
            break
      except Exception, e:
         ("Unknown error, please conntact with provider. Error content: ", e)
   def tellJoke(self):
      print("Find in web")
      print
      print("How do you count cows?")
      print("With a cowculator.")
      print
      print("Press enter to continue")
      raw_input()
if __name__ == "__main__":
   Parser()