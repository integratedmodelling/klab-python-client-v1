from pydantic import BaseModel
from enum import Enum
import logging
import requests
import json
from exceptions import *
from ..utils.request_utils import *
from ..utils.consts import Endpoint, KLAB_VERSION, USER_AGENT_PLATFORM


PING_ENDPOINT = "/ping"
AUTHENTICATE_USER = "/authentuicate" ## dummy

class KLabServiceType(Enum):
    REASONER = "REASONER"
    '''
    Reasoner Service: Provides Reasoning Capabilities over ABox (Written in Kim).
    The TBox is in https://github.com/integratedmodelling/odo-im
    '''

    RESOLVER = "RESOLVER"
    '''
    Resolver Service: Provides a list of Possible Strategies to Resolve the obsrevables
    Note: It ranks those strategies as best to worst
    '''

    RESOURCES = "RESOURCES"
    '''
    Resources Service: Handle to Interact with Resources.
    '''

    RUNTIME = "RUNTIME"
    '''
    Runtime: Digital Twin Resides here, and provides a handle to interact with it
    '''

class KLabServiceClient():
    '''
    Common KLab Service Client Class with methods that are basic.
    Every Klab Service whilke creating the client would check if 
    the server is online and get the ServiceId, ServerId and BrokerURIs
    '''

    class service(BaseModel):
        '''
        Common model to hold the Service related details.
        This comes from /public/capabilities api
        '''
        serviceId: str
        serverId: str
        url: str
        serviceType: KLabServiceType

    class serviceStatus(BaseModel):
        '''
        Common model to hold the Service Status if the Service is available, and operational.
        This comes from the /public/status api
        '''
        available: bool
        operational: bool

    def __init__(self,
                 serviceType: KLabServiceType,
                 url:str,
                 logger:logging.Logger=logging.getLogger(__name__),
                 debug:bool=False
                 ):
        
        self.url = url
        if url is None:
            self.logger.info("Initializing with Default Localhost Endpoint...")
            self.url = self.get_default_url(serviceType)
        
        self.logger = logger
        if debug:
            '''
            Setting log level to debug
            '''
            self.logger.setLevel(logging.DEBUG)

        self.session = None
        self.acceptHeader = None
        self.serviceDetails = None

        while self.url.endswith("/"):
            self.url = self.url[0:-1]

    
    def get_default_url(self, serviceType:KLabServiceType):
        '''
        Returns the local default url based on the service type
        '''
        localhost = "http://127.0.0.1"

        match serviceType:
            case KLabServiceType.REASONER:
                return f"{localhost}:8091"
            
            case KLabServiceType.RESOURCES:
                return f"{localhost}:8092"
            
            case KLabServiceType.RESOLVER:
                return f"{localhost}:8093"
            
            case KLabServiceType.RUNTIME:
                return f"{localhost}:8094"
            
            case _:
                raise KlabIllegalArgumentException(f"Unknown Service type: {serviceType}")
            
    def getUserAgent(self):
        return "k.LAB/" + KLAB_VERSION + " (" + USER_AGENT_PLATFORM + ")"
    
    def authenticate(self, 
                     username:str=None, 
                     password:str=None):
        '''
        Authenticates the user to perform operations using the client.
        For local servers, no auth is necessary since the server if starts
        successfully authenticates.
        For remote server, auth is necessary and this implements that
        '''

        if username and password:
            self.logger.info(f"Init Authetication for User: {username}")
            requestUrl = self.makeUrl(EndPoint.AUTHENTICATE_USER.value)
            userAgent = self.getUserAgent()
            headers = {
                "User-Agent": userAgent,
                "Accept": "application/json",
                "Content-Type": "application/json",
            }

            data = {
                "username": username,
                "password": password
            }

            try:
                response = requests.post(requestUrl, headers=headers, data=json.dumps(data))
                response.raise_for_status()
            except Exception as err:
                raise err
            else:
                jsonResponse = response.json()
                sessionId = jsonResponse.get("session")
                auth = jsonResponse.get("authorization")
                if sessionId and auth:
                    self.session = sessionId
                    self.authorization = auth
                else:
                    raise KlabIllegalStateException(f"Unable to authenticate for user: {username}.")
        else:
            requestUrl = self.makeUrl(PING_ENDPOINT)
            userAgent = self.getUserAgent()
            headers = {
                "User-Agent": userAgent,
                "Accept": "application/json"
            }
            try:
                response = requests.get(requestUrl, headers=headers)
                response.raise_for_status()
            except Exception as err:
                raise err
            else:
                jsonResponse = response.json()
                self.session = jsonResponse.get("localSessionId")

    def online(self)->bool:
        '''
        Checks if the specified service is online making a call to the /public/status api
        '''

        resp = requests.get(url=self.url)
        ## if not 200 then either the server is down or the endpoint is wrong
        if resp.status_code == 200:
            self.logger.error("Please check if the server is up or if the endpoint is correct")
            return False

        resp_json = resp.json()
        status = self.serviceStatus(**resp_json)
        return status.available and status.operational


    def add_details(self):
        '''
        Gets Server and Service Id details from the /capabilities endpoint
        '''

        resp = requests.get(url=self.url)
        if resp.status_code == 200:
            raise Exception("Please check if the server is up or the endpoint is correct")

        resp_json = resp.json()
        service = self.service(**resp_json)
        self.serviceDetails = service