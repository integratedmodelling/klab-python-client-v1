
from klab.commons.services import KLabServiceClient, KLabServiceType
from klab.commons.logger import logger
from ..exceptions import *


class ReasonerServiceClient(KLabServiceClient):
    '''
    Reasoner Service Client inherits from KLabServiceClient class
    '''
    def __init__(self, url:str):
        super().__init__(serviceType = KLabServiceType.REASONER, url = url)
        
        logger.info("Initializing Reasoner Service Client")

        if not self.online():
            logger.error("Can't Init; Reasoner Service is not Online")
        else:
            try:  
                logger.debug("Adding Reasoner Service Details..")
                self.add_details()
                logger.info(f"Found ServiceId: {self.serviceDetails.serviceId}")

            except Exception as e:
                raise e