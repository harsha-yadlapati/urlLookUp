from chalice import Chalice
from chalice import BadRequestError
from urllib.parse import urlparse
import boto3


# Creating the DynamoDB Table Resource
ddbResource = boto3.resource('dynamodb')
# Creating ddbTable
ddbTable = ddbResource.Table('malwareURL') 


app = Chalice(app_name='urlLookUp')
# app.debug=True enables debug option and it will throuw stack trace to the output 
app.debug = True 


@app.route('/')
def index():
    return {'Availability': 'Hello World I am available and I can respond'}
    
    
'''
Below function will check if the provided request can be allowed or denied 
It looks for the query paramaters and serch for the query key "url"

Sample query link can look like http://<urlLookUpService_dnsName>/urlLookUp?url=http://www.google.co.in/news
So below function will check if www.google.co.in is allowed or denied
'''

@app.route('/urlLookUp')
def urlLookup():
    request = app.current_request
    
    if(queryParametersValidation(request)) :
        urlToCheck = request.query_params["url"]
    
    domainName = getDomainName(urlToCheck)

    response = ddbTable.get_item(
        Key = {
           'malwareURL' : domainName
        })
    
    print(response);
    return response
    
'''
Checks if 'url' is passed as query paramater
else raise bad request exception
'''

def queryParametersValidation(current_request):
    queryParametersDict = current_request.query_params
    
    if (queryParametersDict==None):
        print("query parameters not passed") 
        raise BadRequestError( """query parameters are not passed. 
                      Send query as below example
                      http://urlLookUpService_dnsName/urlLookUp?url=http://www.google.co.in/news""")
        
    else :
        if( ('url' not in queryParametersDict)):
            print(queryParametersDict)
            raise BadRequestError( """query parameters does not contain query key 'url'. 
                      Send query as below example
                      http://urlLookUpService_dnsName/urlLookUp?url=http://www.google.co.in/news""")
        else : 
            return True
            
'''
return domain name if value of query parameter 'url' is valid 
else raise bad request exception
'''

def getDomainName(urlToCheck):
    
    parseURL = urlparse(urlToCheck)
    if (  parseURL.netloc == "" ):
        print("Received URL is " + urlToCheck)
        raise BadRequestError( """url parameter value is not valid'. 
                      Send query as below example
                      http://urlLookUpService_dnsName/urlLookUp?url=http://www.google.co.in/news""")
    else :
        return parseURL.netloc
         