import requests
import json
import logging
from typing import Any
from dataclasses import asdict


class RequestUtils:
    '''
    Warps over the Requests (GET/ POST/ PATCH) with headers injected in the requests.
    '''

    def getUserAgent(self)->str:
        return "k.LAB/" + KLAB_VERSION + " (" + USER_AGENT_PLATFORM + ")"
    

    @staticmethod
    def makeUrl(endpoint, parameters=[]):
        '''
        Util to get the url, to make a call
        For GET call, we parse the params and add them to the req endpoint
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

        return f"{endpoint}{parms}"
    

    def addParams(endpoint, parameters=[]):
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
    
    @staticmethod
    def get(endpoint: str, parameters: list = None):
        '''
        Warps over the generic requests.get exposed by the requests library.
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
            

    @staticmethod
    def post(endpoint:str, data:Any, headers:dict={}):
        '''
        Warps over the generic requests.post method exposed by the requests library.
        '''

        requestUrl = RequestUtils.makeUrl(endpoint)

        try:
            headers["Accept"] = "application/json"
            response = requests.post(requestUrl, json=asdict(data))
            response.raise_for_status()
            jsonResponse = response.json()
            return jsonResponse
        
        except Exception as err:
            raise err
