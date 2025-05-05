import requests

class RequestUtils:
    '''
    Class warps over the Requests (GET/ POST/ PATCH) with headers injected in the requests.
    Sort of works like a middleware.
    '''

    def __init__(self, url:str= None, acceptHeader:str = None):
        self.url = url
        self.acceptHeader = acceptHeader

    def accept(self, mediaType:str):
        self.acceptHeader = mediaType
        return self
    
    def get(self, endpoint: str, parameters: list = None):
        '''
        Warps over the generic requests.get exposed by the requests library.
        We could have overridden the implementation of get however not doing this now.
        '''

        mediaType = "application/json"
        if self.acceptHeader:
            mediaType = self.acceptHeader
            self.acceptHeader = None
        
        requestUrl = self.makeUrl(endpoint, parameters)
        userAgent = self.getUserAgent()
        headers = {
            "User-Agent": userAgent,
            "Accept": mediaType,
            "klab-authorization": self.session,
            "Authentication": self.authorization
        }
        try:
            response = requests.get(requestUrl, headers=headers)
            response.raise_for_status()
        except Exception as err:
            raise err
        else:
            if mediaType == 'application/json':
                jsonResponse = response.json()
                return jsonResponse
            elif mediaType == 'text/plain':
                return response.text
            else:
                return response.content
            

    def post(self, endpoint:str, request: any, pathVariables:list = None):
        '''
        Warps over the generic requests.post method exposed by the requests library.
        '''
        mediaType = "application/json"
        if self.acceptHeader:
            mediaType = self.acceptHeader
            self.acceptHeader = None
        
        # TODO
        # if (pathVariables != null) {
        # 	for (int i = 0; i < pathVariables.length; i++) {
        # 		endpoint = endpoint.replace(pathVariables[i].toString(), pathVariables[++i].toString());
        # 	}
        # }

        requestUrl = self.makeUrl(endpoint)
        userAgent = self.getUserAgent()
        headers = {
            "User-Agent": userAgent,
            "Content-Type": "application/json",
            "Accept": mediaType,
            "klab-authorization": self.session,
            "Authentication": self.authorization
        }

        try:
            response = requests.post(requestUrl, headers=headers, data=request.toJson())
            response.raise_for_status()
        except Exception as err:
            raise err
        else:
            jsonResponse = response.json()
            return jsonResponse

    def makeUrl(self, endpoint, parameters=[]):
        '''
        Util to get the url, to make a GET call
        '''
        parms = ""
        if parameters:
            for i in range(0, len(parameters)):
                if parms == "":
                    parms += "?"
                else:
                    parms += "&"
                parms += str(parameters[i])
                i += 1
                parms += "=" + str(parameters[i])

        return f"{self.url}{endpoint}{parms}"
    
    def addParams(self, endpoint, parameters=[]):
        '''
        Util to add params to the GET call
        '''
        parms = ""
        if parameters:
            i = 0
            while i < len(parameters):
                if parms == "":
                    parms += "?"
                else:
                    parms += "&"
                parms += str(parameters[i])
                i += 1
                parms += "=" + str(parameters[i])
                i += 1

        return f"{endpoint}{parms}"
