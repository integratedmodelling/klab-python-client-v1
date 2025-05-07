
from klab.commons.services import KLabServiceClient, KLabServiceType
from klab.commons.logger import logger
from ..exceptions import *


class ReasonerServiceClient(KLabServiceClient):
    '''
    Reasoner Service Client inherits from KLabServiceClient class
    '''
    def __init__(self, url:str):
        super(serviceType = KLabServiceType.REASONER, url = url)
        
        logger.info("--- Initializing Reasoner Service Client ---")

        if not self.online():
            logger.error("-- Reasoner Service is not Online ---")