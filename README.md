### Problem Statement
Sample webservice to check if given url is malware or not

#### FrameWork used 

Chalice : https://aws.github.io/chalice/quickstart.html 

Chalice is an AWS opensource framework to create python serverless apps. It automatically created Lambda, API Gateway and related IAM Roles , all you need to do is use the command 
"chalice deploy" :)

#### How this service works?

When some one makes a GET request to this service, it will check if the domain in URL (which is passed as query parameter) , can be allowed to make a http connection or not.

Eg : https://ciq51uqa3d.execute-api.us-east-2.amazonaws.com/api/urlLookUp?url=http://www.google.com/news  --> when you try to access this link,
it will tell us if www.google.com is malware or not ( I simply made www.google.com as malware :)


#### How data is arranged in DynamoDB
In DDB table, there is only 1 column and it contains rows of domain names. So this service checks if the domain name exists in this table,  if it exists it will return "Deny" 
else service will consider this domain can be allowed to make http connection.

#### Something about security
* Read access is provided to DDB, so if you have this link "https://ciq51uqa3d.execute-api.us-east-2.amazonaws.com/api/urlLookUp?url=<add url you want to check>" you can replace url 
value and test if urls domain is allowed or denied based on ddb info  
* When you access this link, API Gateway will automatically assume the role whcich has read access to DDB
* We can setup more granular level security, but as it is sample app I didn't consider much



#### testing: 
most probably this lambda will be removed by the time you access it :) ,  but can try below examples :)   (!!!! allow or deny is just based on what I set in DDb , noboday want to deny google :))

* https://ciq51uqa3d.execute-api.us-east-2.amazonaws.com/api/urlLookUp?url=http://www.google.com/news --> the response will be Allowed 
* https://ciq51uqa3d.execute-api.us-east-2.amazonaws.com/api/urlLookUp?url=http://www.google.co.in/news --> the response will be Denied
* https://ciq51uqa3d.execute-api.us-east-2.amazonaws.com/api/urlLookUp? --> Response will be BadRequest as the request doesnt have  query parameters
* https://ciq51uqa3d.execute-api.us-east-2.amazonaws.com/api/urlLookUp?query1=http://test.com/ -->  Response will be BadRequest as the request doesnt have query 
parameter 'url' as first 2 examples
* https://ciq51uqa3d.execute-api.us-east-2.amazonaws.com/api/urlLookUp?url=www.google.co.in/news --> the response will be BadRequest as the value of query parameter 'url' 
is not of the form *http://somedomain.in/index*




#### further improments :
* render output in html format
* use env variables instead of hardcoding the ddb table name
* user friendly dns name rather than ciq51uqa3d.execute-api.us-east-2.amazonaws.com