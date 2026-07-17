from pydantic import BaseModel
from enum import Enum
from dataclasses import dataclass
from typing import Tuple, List
import requests
import json
from .logger import logger
from .exceptions import *
from .utils.request import RequestUtils
from .utils.file import FileUtils
from .utils.string import strUtils
from .utils.json import JSONutils
from .utils.consts import KLAB_VERSION, USER_AGENT_PLATFORM

## Certificate Constants
CERT_KEY_USERNAME = "klab.username"
CERT_KEY_SIGNATURE = "klab.signature"
CERT_KEY_CERTIFICATE_TYPE = "klab.certificate.type"
CERT_KEY_CERTIFICATE = "klab.certificate"
CERT_KEY_LEVEL = "klab.certificate.level"
CERT_KEY_AGREEMENT = "klab.agreement"
CERT_KEY_USER_EMAIL = "klab.user.email"
CERT_PARTNER_HUB = "klab.partner.hub"

## Federation Keys
FEDERATION_BROKER_URL_KEY = "federation.broker.url"
FEDERATION_ID_KEY = "federation.id"

## Hub Stuff
HUB_AUTH_ENDPOINT = "/api/v2/engines/auth-cert"
DEFAULT_HUB_URL = "https://integratedmodelling.org/hub"
ANONYMOUS_USER = "anonymous"

## Status and Details related Endpoints common to all services
AUTHENTICATE_USER = "/authentuicate" ## dummy
PING_ENDPOINT = "/ping"
STATUS_ENDPOINT = "/public/status"
CAPABILITIES_ENDPOINT = "/public/capabilities"
CREATE_SESSION_ENDPOINT = "/createSession"

class KLabServiceType(Enum):
    '''
    The 4 fundamental types of services that are part of the k.LAB system.
    Each service or node in the system is essentially one of these types.
    '''

    REASONER = "REASONER"
    '''
    Reasoner Service: Provides Reasoning Capabilities i.e. to find if Concept A IS Concept B, or Concept A Is Compatible with Concept B
    The system internally uses HERMIT Reasoner
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

@dataclass
class ServiceDetails:
    '''
    Common model to hold the Service related details.
    This comes from /public/capabilities api
    '''
    serviceId: str
    serverId: str
    url: str
    brokerURI: str
    serviceType: KLabServiceType = None


@dataclass
class ServiceStatus:
    '''
    Common model to hold the Service Status if the Service is available, and operational.
    This comes from the /public/status api
    '''
    available: bool
    operational: bool

@dataclass
class UserAuthData:
    '''
    Common model to hold the User Auth Request details.
    This is used to make a call to hub api to get the User Scope
    '''
    name: str
    key: str
    userType: str
    level: str
    certificate: str
    idAgreement: str
    email: str



class KLabServiceClient():
    '''
    Common KLab Service Client Class with methods that are basic.
    Every Klab Service whilke creating the client would check if 
    the server is online and get the ServiceId, ServerId.

    Every Individual Service Client would inherit from this class
    '''

    @dataclass
    class federation():
        '''
        Dataclass to hold the AMQP Broker URL and ID for the Federation
        The central component to make the Digital Twin system work like a 
        Shared Computer.
        '''

        id: str = None
        broker_url: str = None

    def __init__(self,
                 serviceType: KLabServiceType,
                 url:str):
        
        self.url = url
        if url is None:
            logger.info("Initializing with Default Localhost Endpoint...")
            self.url = self.get_default_url(serviceType)

        self.session = None
        self.acceptHeader = None
        self.serviceDetails = None

        while self.url.endswith("/"):
            self.url = self.url[0:-1]


    
    def get_default_url(self, serviceType:KLabServiceType)->str:
        '''
        Returns the local default url based on the service type
        '''

        localhost = "http://127.0.0.1"

        match serviceType:
            case KLabServiceType.REASONER:
                return f"{localhost}:8091/reasoner"
            
            case KLabServiceType.RESOURCES:
                return f"{localhost}:8092/resources"
            
            case KLabServiceType.RESOLVER:
                return f"{localhost}:8093/resolver"
            
            case KLabServiceType.RUNTIME:
                return f"{localhost}:8094/runtime"
            
            case _:
                raise KlabIllegalArgumentException(f"Unknown Service type: {serviceType}")
    
    def authenticate(self, 
                     username:str=None, 
                     password:str=None)->Tuple[federation, str]:
        '''
        Authenticates the user to perform operations using the client.
        For local servers, no auth is necessary since the server if starts
        successfully authenticates.
        For remote server, auth is necessary and this implements that.

        Returns an UserScope
        '''

        ## TODO: At the moment, we are just considering Auth only with Hub, and not 
        ## with UserName and Password. Possibly auth with username and password would need some 
        ## understanding of keycloak
        
        parsedCert = FileUtils.parseCertFile()
        logger.info(f"Attempting to Authenticate User {parsedCert.get(CERT_KEY_USERNAME, "")} with Hub")
        try:
            hubAuthResponse = RequestUtils.post(
                endpoint = parsedCert.get("dummy", DEFAULT_HUB_URL) + HUB_AUTH_ENDPOINT, 
                data = UserAuthData(
                    name = parsedCert.get(CERT_KEY_USERNAME, None),
                    key = parsedCert.get(CERT_KEY_SIGNATURE, None),
                    userType = parsedCert.get(CERT_KEY_CERTIFICATE_TYPE, None),
                    certificate = strUtils.remove_escape_char(parsedCert.get(CERT_KEY_CERTIFICATE, None)),
                    level = parsedCert.get(CERT_KEY_LEVEL, None),
                    idAgreement = parsedCert.get(CERT_KEY_AGREEMENT, None),
                    email = parsedCert.get(CERT_KEY_USER_EMAIL, None),
                )
            )

            userData = hubAuthResponse["userData"]
            #logger.info(hubAuthResponse["userData"].keys())
            #print(json.dumps(hubAuthResponse, indent=2))
            #logger.info(hubAuthResponse["userData"]["token"])
            logger.info(f"User {userData.get("identity", {}).get("id", "anonymous")} Authenticated Successfully with Hub")

            federationID, federationBrokerURL = None, None

            for group in hubAuthResponse["userData"].get("groups", []):
                customProperties = group.get("customProperties", [])
                for item in customProperties:
                    if item.get("key", None) == FEDERATION_ID_KEY and item.get("value", None) == True:
                        logger.info(f"Found User: {userData.get("identity", {}).get("id", ANONYMOUS_USER)} part of Federation: {key}")
                        federationID = group.get("id")
                    
                    if item.get("key", None) == FEDERATION_BROKER_URL_KEY:
                        federationBrokerURL = item.get("value")
                    
                    if federationID is not None and federationBrokerURL is not None:
                        break
                    
            if len(hubAuthResponse.get("services", [])) > 0:
                logger.info(f"The following Services are available to {userData.get("identity", {}).get("id", "anonymous")}")
                for service in hubAuthResponse.get("services", []):
                    logger.info(f"{service.get("id")}") 

            return self.federation(
                broker_url=federationBrokerURL,
                id=federationID
            ), userData.get("token")

        except Exception as e:
            raise KlabAuthException(f"Error while authenticating with Hub: {e}") 


    def online(self)->bool:
        '''
        Checks if the specified service is online making a call to the /public/status api
        '''
        try:
            resp = requests.get(url=self.url+STATUS_ENDPOINT)
            ## if not 200 then either the server is down or the endpoint is wrong
            if resp.status_code != 200:
                logger.error("Please check if the server is up or if the endpoint is correct")
                return False
            resp_json = resp.json()
            status = JSONutils.JSON2Class(resp_json, ServiceStatus)
            return  status.available and status.operational
        
        except Exception as e:
            logger.error(f"Service at {self.url} is not online or not reachable, error: {e}")


    def add_details(self):
        '''
        Gets Server and Service Id details from the /capabilities endpoint
        '''

        resp = requests.get(url=self.url+CAPABILITIES_ENDPOINT)
        if resp.status_code != 200:
            raise Exception("Failed to get Service Details") ## This state should not happen since it should have failed in isOnline check

        resp_json = resp.json()
        serviceDetails = JSONutils.JSON2Class(resp_json, ServiceDetails)
        self.serviceDetails = serviceDetails