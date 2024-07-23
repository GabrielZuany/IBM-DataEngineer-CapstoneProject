from datetime import datetime
import json
import pymongo 
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from urllib.parse import quote_plus
from loguru import logger
    
class MongoDB:
    
    @staticmethod
    def __solve_auth_mechanism(auth:str) -> str:
        """Static method to solve the authentication mechanism
        
        Args:
            auth (str): The authentication mechanism to be validated
        
        Raises:
            ValueError: If the authentication mechanism is not one of the supported mechanisms
        
        Returns:
            str: The authentication mechanism to use 
        """
        if (auth is not None) and (auth not in ['SCRAM-SHA-256', 'SCRAM-SHA-1', 'MONGODB-CR']): 
            logger.error(f"Invalid authentication mechanism: {auth}")
            raise ValueError(f"Invalid authentication mechanism: {auth}")
        return auth
    
    @staticmethod
    def __prettify_json(source:str|dict, indent:int=4) -> str:
        """Static method to prettify a JSON string
        
        Args:
            json_str (str): The JSON string to prettify
            indent (int): The number of spaces to indent the JSON string
        
        Returns:
            str: The prettified JSON string
        """
        if isinstance(source, str):
            return json.dumps(json.loads(source), indent=indent)
        elif isinstance(source, dict):
            return json.dumps(source, indent=indent)
    
    def __init__(self, host:str="localhost", port:int=27017, user:str=None, password:str=None, auth_db:str="admin", auth_mechanism:str='SCRAM-SHA-256', config_dict:dict=None) -> None:
        """Initializes the MongoDB client with the given parameters
        
        Args:
            - host (str): The hostname or IP address of the MongoDB server
            - port (int): The port number of the MongoDB server
            - user (str): The username to authenticate with
            - password (str): The password to authenticate with
            - auth_db (str): The database to authenticate against
            - auth_mechanism (str): The authentication mechanism to use
            - config_dict (dict): A dictionary containing the configuration parameters
        
        Observations:
            - If the config_dict is not None, the values of the parameters are taken from the dictionary
            - Dictionary keys are: 'host', 'port', 'user', 'password', 'auth_db', 'auth_mechanism'
            - The auth_mechanism is set to 'SCRAM-SHA-256' by default
            - The auth_mechanism is validated to ensure it is one of the supported mechanisms
            
        Exceptions:
            - ValueError: If the auth_mechanism is not one of the supported mechanisms
        """
        self.host:str = host
        self.port:int = port
        self.user:str = user
        self.password:str = password
        self.auth_db:str = auth_db
        self.auth_mechnism:str = self.__solve_auth_mechanism(auth_mechanism)
        self.client : MongoClient = None
        self.db = None
        self.collection = None
        if config_dict is not None:
            self.host = config_dict["host"]
            self.port = config_dict["port"]
            self.user = config_dict["user"]
            self.password = config_dict["password"]
            self.auth_db = config_dict["auth_db"]
            self.auth_mechnism = self.__solve_auth_mechanism(config_dict["auth_mechanism"])
            
    def __enter__(self) -> MongoClient: 
        """Connects to the MongoDB server using the parameters provided in the constructor
        
        Returns:
            - MongoClient: The MongoDB client object
        """
        return self.connect()
    
    def __set_db__(self, db:str) -> None:
        """Sets the database to use
        
        Args:
            - db (str): The database to use
        """
        self.db = db
        
    def __set_collection__(self, collection:str) -> None:
        """Sets the collection to use
        
        Args:
            - collection (str): The collection to use
        """
        self.collection = collection
    
    def __exit__(self) -> None:
        """Closes the connection to the MongoDB server"""
        self.close()
            
    def connect(self) -> MongoClient:
        """Connects to the MongoDB server using the parameters provided in the constructor   
        
        Returns:
            MongoClient: The MongoDB client object
        
        Observations:
            - Uses ping to check if the connection is successful     
        """
        self.client = MongoClient(host=self.host, port=self.port, username=self.user, password=self.password, authSource=self.auth_db, authMechanism=self.auth_mechnism)
        try:
            self.client.admin.command('ping')
            logger.info(f"Connected to MongoDB -> {self.host}:{self.port}")
        except ConnectionFailure as cf:
            logger.error(f"Connection to MongoDB failed: {cf}")
            raise cf
        return self.client
            
    def close(self) -> None:
        """Closes the connection to the MongoDB server
        
        Raises:
            - cf (ConnectionFailure): If the connection to the MongoDB server cannot be closed
            - e (Exception): If an error occurs while closing the connection
        """
        try:
            self.client.close()
            logger.debug("Connection to MongoDB closed")
        except ConnectionFailure as cf:
            logger.error(f"Failed to close connection to MongoDB: {cf}")
            raise cf
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise e
            
    def info(self, mode:object=str()) -> str | dict:
        """Returns the server information of the MongoDB server
        
        Args:
            - mode (object): The mode to return the server information. If str, returns the information as a JSON string. If dict, returns the information as a dictionary
        
        Returns:
            - str: The server information of the MongoDB server in JSON format
        
        Raises:
            - ValueError: If the mode is not str or dict            
        """
        if not isinstance(mode, (str, dict)):
            logger.error(f"Invalid mode: {mode}. Must be either str or dict")
            raise ValueError(f"Invalid mode: {mode}. Must be either str or dict")
        
        if isinstance(mode, str):
            return self.__prettify_json(self.client.server_info())
        return self.client.server_info()
        
    
    def insert_one(self, db:str=None, collection:str=None, document:dict=None) -> dict:
        """Inserts a document into the specified collection in the specified database
        
        Args:
            - db (str): The database to insert the document into
            - collection (str): The collection to insert the document into
            - document (dict): The document to insert
        
        Raises:
            - ValueError: If the document is not a dictionary
        """
        db = db if db is not None else self.db
        collection = collection if collection is not None else self.collection
        try:
            self.client[db][collection].insert_one(document)
            logger.debug(f"Document inserted into {db}.{collection}")
        except Exception as e:
            logger.error(f"An error occurred trying to insert {document} into {db}:{collection}: {e}")
            raise e   
        return document
        
    def insert_many(self, db:str=None, collection:str=None, documents:list[dict]=None) -> None:
        """Inserts multiple documents into the specified collection in the specified database
        
        Args:
            - db (str): The database to insert the documents into
            - collection (str): The collection to insert the documents into
            - documents (list[dict]): The documents to insert
        
        """
        db = db if db is not None else self.db
        collection = collection if collection is not None else self.collection        
        try:
            #[self.client[db][collection].insert_one(document) for document in documents]
            self.client[db][collection].insert_many(documents)
            logger.debug(f"{len(documents)} documents inserted in {db}.{collection}")
        except Exception as e:
            logger.error(f"An error occurred trying to insert {documents} into {db}:{collection}: {e}")
            raise e
        
    def find_one(self, db:str=None, collection:str=None, query:dict={}, prettify:bool=False) -> dict | str | None:
        """Finds a document in the specified collection in the specified database
        
        Args:
            - db (str): The database to find the document in
            - collection (str): The collection to find the document in
            - query (dict): The query to find the document
            - prettify (bool): If True, the document is prettified (returns a string)
        
        Returns:
            - dict: The document found
        
        Raises:
            - ValueError: If the query is not a dictionary
        """
        db = db if db is not None else self.db
        collection = collection if collection is not None else self.collection
        try:
            document = self.client[db][collection].find_one(query)
            if document is None:
                logger.debug(f"No document found in {db}.{collection}")
                return None
            logger.debug(f"Document found in {db}.{collection}")
            if prettify:
                return self.__prettify_json(document)
            return document
        except Exception as e:
            logger.error(f"An error occurred trying to find a document in {db}:{collection}: {e}")
            raise e
        
    def find_all(self, db:str=None, collection:str=None, query:dict={}, prettify:bool=False) -> list[dict] | str | None:
        """Finds multiple documents in the specified collection in the specified database
        
        Args:
            - db (str): The database to find the documents in
            - collection (str): The collection to find the documents in
            - query (dict): The query to find the documents
        
        Returns:
            - list[dict]: The documents found
        
        Raises:
            - ValueError: If the query is not a dictionary
        """
        db = db if db is not None else self.db
        collection = collection if collection is not None else self.collection
        try:
            documents:list[dict] =  list(self.client[db][collection].find(query))
            logger.debug(f"{len(documents)} documents found in {db}.{collection}")
            if prettify:
                documents_str:str = [documents_str+self.__prettify_json(json_dict) for json_dict in documents]
                return documents_str
            return documents
        except Exception as e:
            logger.error(f"An error occurred trying to find documents in {db}:{collection}: {e}")
            raise e
    
    def find_limit(self, db:str=None, collection:str=None, query:dict={}, limit:int=0, skip:int=0, prettify:bool=False) -> list[dict]:
        """Finds multiple documents in the specified collection in the specified database with a limit and skip
        
        Args:
            - db (str): The database to find the documents in
            - collection (str): The collection to find the documents in
            - query (dict): The query to find the documents
            - limit (int): The number of documents to return
            - skip (int): The number of documents to skip
        
        Returns:
            - list[dict]: The documents found
        
        Raises:
            - ValueError: If the query is not a dictionary
        """
        db = db if db is not None else self.db
        collection = collection if collection is not None else self.collection        
        try:
            documents:list[dict] = list(self.client[db][collection].find(query).limit(limit).skip(skip))
            logger.debug(f"{len(documents)} documents found in {db}.{collection}")
            if prettify:
                documents_str:str = [documents_str+self.__prettify_json(json_dict) for json_dict in documents]
                return documents_str
            return documents
        except Exception as e:
            logger.error(f"An error occurred trying to find documents in {db}:{collection}: {e}")
            raise e
        
    def find_by_date(self, db:str=None, collection:str=None, date_field:str=None, start_date:str=None, end_date:str=None, limit:int=100, sort:bool=False, sort_label:str="", prettify:bool=False) -> list[dict] | str:
        """Finds multiple documents in the specified collection in the specified database with a date range
        
        Args:
            - db (str): The database to find the documents in
            - collection (str): The collection to find the documents in
            - date_field (str): The field containing the date
            - start_date (str): The start date
            - end_date (str): The end date
            - prettify (bool): If True, the document is prettified (returns a string)   
        
        Returns:
            - list[dict]: The documents found
        
        Raises:
            - ValueError: If the date_field, start_date or end_date are not strings
        """
        
        # TODO: check date interval
        
        db = db if db is not None else self.db
        collection = collection if collection is not None else self.collection
        
        if not all(isinstance(date, str) for date in [date_field, start_date, end_date]):
            logger.error(f"Invalid date: {date_field}, {start_date}, {end_date}. Must be strings")
            raise ValueError(f"Invalid date: {date_field}, {start_date}, {end_date}. Must be strings")
        
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            query:dict = {date_field: {"$gt": start, "$lte": end}}
            documents:list[dict] = []
            if sort:
                documents = list(self.client[db][collection].find(query).sort(sort_label, pymongo.DESCENDING).limit(limit))
            else:
                documents = list(self.client[db][collection].find(query).limit(limit))
            logger.debug(f"{len(documents)} documents found in {db}.{collection}")
            if prettify:
                documents_str:str = [documents_str+self.__prettify_json(json_dict) for json_dict in documents]
                return documents_str
            return documents
        except Exception as e:
            logger.error(f"An error occurred trying to find documents in {db}:{collection}: {e}")
            raise e
        
    def update_one(self, db:str=None, collection:str=None, query:dict={}, update:dict={}) -> None:
        """Updates a document in the specified collection in the specified database
        
        Args:
            - db (str): The database to update the document in
            - collection (str): The collection to update the document in
            - query (dict): The query to update the document
            - update (dict): The update to apply
        
        Raises:
            - ValueError: If the query or update are not dictionaries
        """
        db = db if db is not None else self.db
        collection = collection if collection is not None else self.collection
        try:
            self.client[db][collection].update_one(query, update)
            logger.debug(f"Document updated in {db}.{collection}")
        except Exception as e:
            logger.error(f"An error occurred trying to update a document in {db}:{collection}: {e}")
            raise e
        
    def delete_one(self, db:str=None, collection:str=None, query:dict={}) -> None:
        """Deletes a document in the specified collection in the specified database
        
        Args:
            - db (str): The database to delete the document from
            - collection (str): The collection to delete the document from
            - query (dict): The query to delete the document
        
        Raises:
            - ValueError: If the query is not a dictionary
        """
        db = db if db is not None else self.db
        collection = collection if collection is not None else self.collection        
        try:
            self.client[db][collection].delete_one(query)
            logger.debug(f"Document deleted from {db}.{collection}")
        except Exception as e:
            logger.error(f"An error occurred trying to delete a document from {db}:{collection}: {e}")
            raise e
        
    def delete_many(self, db:str=None, collection:str=None, query:dict={}) -> None:
        """Deletes multiple documents in the specified collection in the specified database
        
        Args:
            - db (str): The database to delete the documents from
            - collection (str): The collection to delete the documents from
            - query (dict): The query to delete the documents
        
        Raises:
            - ValueError: If the query is not a dictionary
        """
        db = db if db is not None else self.db
        try:
            documents = self.client[db][collection].delete_many(query)
            logger.debug(f"{documents.deleted_count} documents deleted from {db}.{collection}")
        except Exception as e:
            logger.error(f"An error occurred trying to delete documents from {db}:{collection}: {e}")
            raise e
        
    def create_label(self, db:str=None, collection:str=None, doc={}, label:str=None, values:str|int|float|list=[]) -> None:
        """Creates a label in the specified collection in the specified database
        
        Args:
            - db (str): The database to create the label in
            - collection (str): The collection to create the label in
            - label (str): The label to create
        
        Raises:
            - ValueError: If the label is not a string
        """
        db = db if db is not None else self.db
        collection = collection if collection is not None else self.collection        
        try:
            self.client[db][collection].update_one(doc, {"$set": {label: values}})
            logger.debug(f"Label {label} created in {db}.{collection}")
        except Exception as e:
            logger.error(f"An error occurred trying to create a label in {db}:{collection}: {e}")
            raise e