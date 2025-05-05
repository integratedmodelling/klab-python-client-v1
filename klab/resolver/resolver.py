
from klab.commons.services import KLabServiceClient, KLabServiceType
from enum import Enum

class ResolverServiceClient(KLabServiceClient):
    '''
    Resolver Service Client inherits from KLabServiceClient class
    '''

    class API(Enum):
        RESOLVE_OBSERVATION = "/resolve"

    def __init__(self, url:str):
        super(serviceType = KLabServiceType.RESOLVER, url = url)
        self.logger.info("Init Resolver Service Client")

        if not self.online():
            self.logger.error("Resolver Service is not Online, Exiting")

        try:  
            self.logger.debug("Adding Service Details..")
            self.add_details()
            self.logger.info(f"Found ServiceId: {self.serviceDetails.serviceId}")

        except Exception as e:
            raise e