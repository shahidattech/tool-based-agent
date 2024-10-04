from pymongo import MongoClient
from pymongo.errors import (ConnectionFailure, DuplicateKeyError, OperationFailure, ServerSelectionTimeoutError, PyMongoError)
import os
from app.utils.logging import logger
from bson import ObjectId

customer_deal_number = None

class MongoDal:
    def __init__(self, connection_string, db_name, collection_name) -> None:
        try:
            
            self.client = MongoClient(os.getenv('MONGODB_URI'))
            self.db = self.client[os.getenv('DB_NAME')]
            self.collection = self.db[collection_name]
            self.client.admin.command('ping')
            logger.info("Connected to MongoDB")
        except ConnectionFailure as e:
            logger.error(f"Could not connect to MongoDB:{str(e)}")
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {e}")

    def health_check(self):
        try:
            self.client.admin.command('ping')
            return True
        except ConnectionFailure as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            raise e
        except ServerSelectionTimeoutError:
            return False
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {e}")
            return False

    def get(self):
        return self.collection.find()
    
    def get_otp(self, query):
        try:
            logger.info(f"Fetching OTP data: {query}")
            if not isinstance(query, dict):
                raise ValueError("Query parameter must be a dictionary")
            return self.collection.find_one(query)
        except Exception as e:
            logger.error(f"Error fetching OTP data: {e}")
            return None

    def get_phone_numbers_by_deal_number(self, deal_number: str):
        # Fetch Phone numbers from Deal.Owner and Deal.co_owner
        phone_numbers = []
        result = {}
        for deal in self.collection.find({"deal_number": deal_number}):
            if deal["owner"]:
                phone_numbers.append(deal["owner"]["phone"]) if deal["owner"]["phone"] not in phone_numbers and deal["owner"]["phone"] and deal["owner"]["phone"]!="string" else None
            if deal["co_owner"]:
                phone_numbers.append(deal["co_owner"]["phone"]) if deal["co_owner"]["phone"] not in phone_numbers and deal["co_owner"]["phone"] and deal["co_owner"]["phone"]!="string" else None
        result["phone_numbers"] = phone_numbers
        result["deal_number"] = deal_number
        logger.info(f"Phone numbers fetched: {phone_numbers}")
        return result

    def get_phone_numbers_by_name(self, full_name: str):
        # Fetch Phone numbers from Deal.Owner and Deal.co_owner by name
        phone_numbers = []
        # Check if any document matches the query
        if cust_data := self.collection.find_one({"full_name": full_name.lower().strip()}):
            count = 0
            logger.debug(f"Customer data: {cust_data}")
            if phone_primary := cust_data.get("phone_primary"):
                phone_numbers.append(phone_primary)
            if phone_secondary := cust_data.get("phone_secondary"):
                phone_numbers.append(phone_secondary)
        return phone_numbers
    
    def fetch_customer_details_by_phone_number(self, phone_number: str):
        # Fetch Phone numbers from Deal.Owner and Deal.co_owner by name
        phone_numbers = []
        # Check if any document matches the query
        # Input Phone number is in the format xxx-xxx-4567  to be matched with  owner.phone that has  actual phone number
        last_four_digits = phone_number[-4:]
        if deal_info := self.collection.find_one({"phone_primary": {"$regex": last_four_digits + '$'}}):
            logger.info(f"Matched with primary_phone: {deal_info}")
            return deal_info
        if deal_info := self.collection.find_one({"phone_secondary": {"$regex": last_four_digits + '$'}}):
            logger.info(f"Matched with phone_secondary: {deal_info}")
            return deal_info
        else:
            return None

    

    def get_last_n_conversations(self, deal_number: str = None, n: int = None):
        
        # query = {"deal_number": {"$exists": True, "$eq": deal_number}}
        query = {}
        if not n:
            conversations = self.collection.find(query).sort([("session_time", -1)])
        else:
            conversations =  self.collection.find(query).sort([("session_time", -1)]).limit(n)

        logger.info(f"Conversations fetched: {conversations}")
            # Format the conversations
        # conversation_history = []
        # for conversation in conversations:
        #     if "customer" in conversation:
        #         conversation_history.append(f"Customer: {conversation['customer']}")       
        #     if "AI financial assistant" in conversation:
        #         conversation_history.append(f"AI financial assistant: {conversation['AI financial assistant']}")
        # return conversation_history
        return list(conversations)
    
    def delete_all(self):
        try:
            logger.info("Deleting all conversation history")
            self.collection.delete_many({})
            return True
        except Exception as e:
            logger.error(f"Error deleting all conversation history: {e}")
            return False

    def get_loan_package(self, loan_package_id: str):
        try:
            logger.info(f"get_loan_package:: Fetching loan package: {loan_package_id}")
            object_id = ObjectId(loan_package_id)
            return self.collection.find_one({"_id": object_id})
        except Exception as e:
            logger.error(f"get_loan_package:: Error fetching loan package: {e}")
            return None
    
    def get_loan_package_by_cibil_score(self, cibil_score: int):
        """Fetch all loan entries where civil_score > minimum_civil_score"""
        try:
            logger.info(f"Fetching loan package by civil score: {cibil_score}")
            matched_packages =  self.collection.find({"min_cibil_score": {"$lte": cibil_score}}).sort([("interest_rate", 1)])

            # Convert ObjectId to string
            packages = []
            for package in matched_packages:
                package['_id'] = str(package['_id'])
                packages.append(package)
            return packages
        except Exception as e:
            logger.error(f"Error fetching loan package by civil score: {e}")
            return None
        
    def get_loan_package_by_cibil_score_lender_name(self, cibil_score: int, lender_name: str):
        """Fetch all loan entries where civil_score > minimum_civil_score"""
        try:
            logger.info(f"Fetching loan package by civil score: {cibil_score}")
            matched_packages =  self.collection.find({"min_cibil_score": {"$lte": cibil_score}, "provider_name": {"$regex": lender_name, "$options": "i"}}).sort([("interest_rate", 1)])

            # Convert ObjectId to string
            packages = []
            for package in matched_packages:
                package['_id'] = str(package['_id'])
                packages.append(package)
            return packages
        except Exception as e:
            logger.error(f"Error fetching loan package by civil score: {e}")
            return None
        
    def get_available_lenders(self, limit: int = None)->list:
        """
        Fetch all available lenders
        """
        try:
            # logger.info(f"Fetching available lenders")
            # available_lenders =  self.collection.distinct("provider_name")
            if limit:
                available_lenders = self.collection.find().limit(limit).distinct("provider_name")
            else:
                available_lenders = self.collection.find().distinct("provider_name")
            return available_lenders
        except Exception as e:
            logger.error(f"Error fetching available lenders: {e}")
            return []
        
    def delete_all_loan_packages(self):
        """Delete all loan packages"""
        try:
            logger.info("Deleting all loan packages")
            self.collection.delete_many({})
            return True
        except Exception as e:
            logger.error(f"Error deleting all loan packages: {e}")
            return False
    
    def get_all_loan_packages(self, limit_count: int = None):
        try:
            logger.info(f"Fetching all loan packages")
            # Fetch all loan packages sort by interest_rate and fetch by limit
            packages_cursor = self.collection.find().sort([("interest_rate", 1)]).limit(limit_count)
            packages = list(packages_cursor)  # Convert cursor to list
            # # Convert ObjectId to string
            # for package in packages:
            #     package['_id'] = str(package['_id'])
            return packages
        except Exception as e:
            logger.error(f"Error fetching all loan packages: {e}")
            return None

    
    def post(self, data):
        try:
            logger.info(f"Inserting OTP  data: {data}")
            result = self.collection.insert_one(data)
            logger.info(f"Data inserted: {result.inserted_id}")
            return str(result.inserted_id)
        except DuplicateKeyError as e:
            logger.error(f"Duplicate key error: {e}")
            return False
        except OperationFailure as e:
            logger.error(f"Operation failure: {e}")
            return False
        except PyMongoError as e:
            logger.error(f"PyMongo error: {e}")
            return False
        except Exception as e:
            logger.error(f"Error inserting data: {e}")
            return False
    
    def put_otp(self, object_id: str,  data: dict)->bool:
        try:
            logger.info(f"Updating data: {data}")
            self.collection.update_one({"_id": object_id}, {"$set": data})
            return True
        except OperationFailure as e:
            logger.error(f"Operation failure: {e}")
            return False
        except PyMongoError as e:
            logger.error(f"PyMongo error: {e}")
            return False
        except Exception as e:
            logger.error(f"Error updating data: {e}")
            return False
        except Exception as e:
            logger.error(f"put_otp:::: Error updating data: {e}")
            return False
    
    def close(self):
        self.client.close()
        logger.info("Connection to MongoDB closed") 