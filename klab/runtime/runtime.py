from klab.commons.services import KLabServiceClient, KLabServiceType
from klab.commons.logger import logger
from ..exceptions import *

class RuntimeServiceClient(KLabServiceClient):
    
    def __init__(self, url:str):
        super().__init__(serviceType = KLabServiceType.RUNTIME, url = url)
        logger.info("Init Runtime Service Client")

        if not self.online():
            logger.error("Runtime Server is not Online")
            
        else:
            try:
                logger.debug("Adding Runtime Service Details...")
                self.add_details()
                logger.info(f"Found ServiceId: {self.serviceDetails.serviceId}")

            except Exception as e:
                raise KlabIllegalArgumentException(f"Error while adding service details: {e}")
