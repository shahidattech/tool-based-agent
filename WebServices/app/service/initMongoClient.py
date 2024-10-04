from app.service.mongoDal import MongoDal
import os



class MongoDBService(MongoDal):
    def __init__(self,
                 connection_string=os.getenv('MONGODB_URI'),
                 db_name=os.getenv('DB_NAME'),
                 collection_name=os.getenv('COLLECTION_NAME_DEAL')) -> None:
        super().__init__(connection_string, db_name, collection_name)

class MongoDBServiceOTP(MongoDal):
    def __init__(self,
                 connection_string=os.getenv('MONGODB_URI'),
                 db_name=os.getenv('DB_NAME'),
                 collection_name=os.getenv('COLLECTION_NAME_OTP')) -> None:
        super().__init__(connection_string, db_name, collection_name)
    
class MongoDBServiceConv(MongoDal):
    def __init__(self,
                 connection_string=os.getenv('MONGODB_URI'),
                 db_name=os.getenv('DB_NAME'),
                 collection_name=os.getenv('COLLECTION_NAME_CONVERSATION')) -> None:
        super().__init__(connection_string, db_name, collection_name)

class MongoDBServiceLoan(MongoDal):
    def __init__(self,
                 connection_string=os.getenv('MONGODB_URI'),
                 db_name=os.getenv('DB_NAME'),
                 collection_name=os.getenv('COLLECTION_NAME_LOAN')) -> None:
        super().__init__(connection_string, db_name, collection_name)
    
class MongoDBServiceDocs(MongoDal):
    def __init__(self,
                 connection_string=os.getenv('MONGODB_URI'),
                 db_name=os.getenv('DB_NAME'),
                 collection_name=os.getenv('COLLECTION_NAME_DOCS')) -> None:
        super().__init__(connection_string, db_name, collection_name)
