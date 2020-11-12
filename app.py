from chalice import Chalice
from chalice import BadRequestError
from urllib.parse import urlparse
import boto3
#from src.app import app

# Intiate chalice app
# refer https://aws.github.io/chalice/quickstart.html 
app = Chalice(app_name='urlLookUp')
# app.debug=True enables debug option and it will throuw stack trace to the output 
app.debug = True 

# Creating the ddb table handler using boto3 resource module
# DDB table we are connecting to is malwareURL
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
# This table information can be added to environement varialble to Lambda instead of hardcoding it.
ddbTable = boto3.resource('dynamodb').Table('malwareURL') 



# Provides health check
@app.route('/')
def index():
    return  """
                Hello World I am up and running, can respond to your requests
                Send query as below example: 
                https://ciq51uqa3d.execute-api.us-east-2.amazonaws.com/api/urlLookUp?url=http://www.google.co.in/news 
            """
    
    
'''
Below function will check if the provided request can be allowed or denied 
It looks for the query paramaters and serch for the query key "url"

Sample query  can look like https://URLLookUpServiceDNSName/api/urlLookUp?url=http://www.google.co.in/news
So below function will check if www.google.co.in is allowed or denied

Reference for request metadata
https://aws.github.io/chalice/api.html#request
https://aws.github.io/chalice/tutorials/basicrestapi.html#request-metadata
'''

@app.route('/urlLookUp')
def urlLookup():
    request = app.current_request
    
    # Validate query parameter
    if(queryParametersValidation(request)) :
        urlToCheck = request.query_params["url"]
    
    # get domainName from url
    domainName = getDomainName(urlToCheck)
    
    '''
     Below logic will query for the items(urls) in ddb table malwareURL, 
     If the item (URL) is present, it will be considered as a malware and return 'Deny' else it will return 'Allow' , to make the http connection 
     
     Consideration : malwareURL table contains the list of domain names which should be denied connection, 
     so if a domin name is not present, it means it is safe to establish connection to that domain 
    '''
    try:
        response = ddbTable.get_item(
        Key = {
           'malwareURL' : domainName
        })
    
        if 'Item' not in response:
            return "Allow : Not Identified as malware allow the connection"
        else :
            return "Deny : Identified as malware deny the connection"
    except Exception as e :
        raise Exception("Exception received from DDB" + str(e))
    
    
'''
Checks if 'url' is passed as query paramater
else raise bad request exception
'''

def queryParametersValidation(current_request):
    queryParametersDict = current_request.query_params
    
    if (queryParametersDict==None):
        app.log.error("Query parameters not passed")
        #print("Query parameters not passed") 
        raise BadRequestError("""
                Query parameters are not passed 
                Send query as below example: 
                 https://ciq51uqa3d.execute-api.us-east-2.amazonaws.com/api/urlLookUp?url=http://www.google.co.in/news 
             """)
        
    else :
        if( ('url' not in queryParametersDict)):
            #print("Query parameters does not contain query key 'url' below is the dict of queryParameters")
            app.log.error("Query parameters does not contain query key 'url' below is the dict of queryParameters")
            #print(queryParametersDict)
            app.log.info(queryParametersDict)
            raise BadRequestError("""
                Query parameters does not contain query key 'url'
                Send query as below example: 
                 https://ciq51uqa3d.execute-api.us-east-2.amazonaws.com/api/urlLookUp?url=http://www.google.co.in/news 
             """)
        else : 
            return True
            
'''
return domain name if value of query parameter 'url' is valid 
else raise bad request exception
'''

def getDomainName(urlToCheck):
    
    # refer https://docs.python.org/3/library/urllib.parse.html to know more about urlparse
    parseURL = urlparse(urlToCheck)
    if (  parseURL.netloc == "" ):
        #print("Received URL is " + urlToCheck)
        app.log.error("Received URL is " + urlToCheck)
        raise BadRequestError("""
                'url'  query parameter value is not valid 
                Send query as below example: 
                 https://ciq51uqa3d.execute-api.us-east-2.amazonaws.com/api/urlLookUp?url=http://www.google.co.in/news 
             """)
    else :
        return parseURL.netloc
         