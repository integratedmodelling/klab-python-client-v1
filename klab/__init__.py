from reasoner.reasoner import ReasonerServiceClient
from resolver.resolver import ResolverServiceClient
from runtime.runtime import RuntimeServiceClient
from resources.resources import ResourcesServiceClient


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
        
        self.logger.info("--- Authenticating Once for all the Individual Service Client ---")

        self.authenticate(username=username, password=password)
       
        self.logger.info("--- Initiating k.LAB Service Clients ---")

        '''
        Inits Reasoner Service Client
        '''
        ReasonerServiceClient(url=reasonerServerEndpoint,debug=debug)
        
        '''
        Inits Runtime Service Client
        '''
        RuntimeServiceClient(url=runtimeServerEndpoint, debug=debug)
        
        '''
        Resources Service Client
        '''
        ResourcesServiceClient(url=resourcesServerEndpoint, debug=debug)

        '''
        Resolver Service Client
        '''
        ResolverServiceClient(url=resolverServerEndpoint, debug=debug)
        