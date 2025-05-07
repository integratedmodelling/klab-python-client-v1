
from klab.commons.services import KLabServiceClient, KLabServiceType
from enum import Enum
from klab.commons.logger import logger


class ResourcesServiceClient(KLabServiceClient):
    '''
    Resources Service Client inherits from KLabServiceClient class
    '''

    class API(Enum):
        '''
        Resource Service Implements the following APIs
        '''
        RETRIEVE_PROJECT = "/retrieveProject/{projectName}"
        QUERY_RESOURCES = "/queryResources"
        PRECURSORS = "/precursors/{namespaceId}"
        PROJECTS = "/projects"
        PROJECT = "/project/{projectName}"
        RESOLVE_MODEL = "/model/{modelName}"
        RESOLVE_URN = "/resolve/{urn}"
        RETRIEVE_NAMESPACE = "/retrieveNamespace/{urn}"
        RETRIEVE_ONTOLOGY = "/retrieveOntology/{urn}"
        RESOLVE_RESOURCE = "/resolveResource"
        RETRIEVE_OBSERVATION_STRATEGY_DOCUMENT = "/retrieveObservationStrategyDocument/{urn}";
        LIST_WORKSPACES = "/listWorkspaces"
        RETRIEVE_BEHAVIOR = "/retrieveBehavior/{urn}"
        RETRIEVE_RESOURCE = "/retrieveResource"
        RETRIEVE_WORKSPACE = "/retrieveWorkspace/{urn}"
        RESOLVE_SERVICE_CALL = "/resolveServiceCall/{name}"
        RESOURCE_STATUS = "/resourceStatus/{urn}"
        RETRIEVE_OBSERVABLE = "/retrieveObservable"
        DESCRIBE_CONCEPT = "/describeConcept/{conceptUrn}"
        RETRIEVE_CONCEPT = "/retrieveConcept/{definition}"
        CONTEXTUALIZE = "/contextualize"
        CONTEXTUALIZE_RESOURCE = "/contextualizeResource"
        RETRIEVE_DATAFLOW = "/retrieveDataflow/{urn}"
        RETRIEVE_WORLDVIEW = "/getWorldview"
        DEPENDENTS = "/dependents/{namespaceId}"
        RESOLVE_MODELS = "/retrieveModels"
        MODEL_GEOMETRY = "/modelGeometry/{modelUrn}"
        READ_BEHAVIOR = "/readBehavior"
        LIST_PROJECTS = "/listProjects"
        LIST_RESOURCE_URNS = "/listResourceUrns"
        RESOURCE_RIGHTS = "/rights/{urn}"


    def __init__(self, url:str):
        super(serviceType = KLabServiceType.RESOLVER, url = url)
        logger.info("Init Resources Service Client")

        if not self.online():
            logger.error("Resources Server is not Online, Exiting")