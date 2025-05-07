from .reasoner.reasoner import ReasonerServiceClient
from .resolver.resolver import ResolverServiceClient
from .runtime.runtime import RuntimeServiceClient
from .resources.resources import ResourcesServiceClient
from .commons.logger import logger


class Client(ReasonerServiceClient, 
             ResolverServiceClient, 
             RuntimeServiceClient,
             ResourcesServiceClient):
    '''
    The main k.LAB client class. It inherits from individual service client
    like the ResonerServiceClient, ResolverServiceClient, RuntimeClient
    and Resources Client.

    A single Client contains in itself the corresponding clients for all the individual k.LAB
    services. A single client application to rule them all. :)
    '''

    def __init__(self,
                 reasonerServerEndpoint:str=None,
                 runtimeServerEndpoint:str=None,
                 resourcesServerEndpoint:str=None,
                 resolverServerEndpoint:str=None,
                 debug:bool=False,
                 username:str=None,
                 password:str=None
                ):

        logger.info("--- Authenticating Once for all the Individual Service Client ---")

        self.authenticate(username=username, password=password)

        if debug:
            logger.info("Setting Log Level to DEBUG")
            logger.setLevel("DEBUG")
       

        '''
        Inits Reasoner Service Client
        '''
        ReasonerServiceClient(url=reasonerServerEndpoint)
        
        '''
        Inits Runtime Service Client
        '''
        RuntimeServiceClient(url=runtimeServerEndpoint)
        
        '''
        Inits Resources Service Client
        '''
        ResourcesServiceClient(url=resourcesServerEndpoint)

        '''
        Inits Resolver Service Client
        '''
        ResolverServiceClient(url=resolverServerEndpoint)
        