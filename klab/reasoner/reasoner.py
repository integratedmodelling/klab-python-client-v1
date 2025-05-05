
from klab.commons.services import KLabServiceClient, KLabServiceType
from exceptions import *


class ReasonerServiceClient(KLabServiceClient):
    '''
    Reasoner Service Client inherits from KLabServiceClient class
    '''
    def __init__(self, url:str,
                debug: bool=False
                ):
        super(serviceType = KLabServiceType.REASONER, url = url, debug = debug)
        
        self.logger.info("--- Initializing Reasoner Service Client ---")

        if not self.online():
            self.logger.error("-- Reasoner Service is not Online ---")