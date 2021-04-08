# twitter-case

## Requisites:

    1- Create an application to collect the 100 last Twitter posts for a given hashtag.

    2- Collect and persist the information in a database for the following hashtags:
        #openbanking, #remediation, #devops, #sre, #microservices, #observability, #oauth, #metrics, #logmonitoring, #opentracing

    3- Sumarize and persist the data so you can retrieve the following information:
        Top 5 users from the collected sample with more followers
        Amount of posts grouped by hour disregarding the hashtag
        Amount of posts per hashtag and language/country

    4- Create an REST API that enables the conspumtion of the items mentioned above. The API should expose exection metrics.

    5- Create a Postman Collection for the created API.

    6- Send the app logs to a logging tool and create queries that shows real time events.

    7- Use a infrastructure monitoring tool and create dashboards that shows amount of executions, latency, and errors in real time.

    8- Publish the project on GitHub and use README.md to document the following:
        Project documentation
        API
        Architecture
        Deployment
        Logs 
        Dashboards
        
## APP:

   ![HolisticView](/img/Holistic.png)
   
   ###### RDS Tables
   ![Tables](/img/Tables.png)

   ###### Lambda:

        - twitter-case-scan: Called by an EventBridge rule (once every 12 hours) or by a POST request. It queries Twitter looking for the tags #openbanking, #remediation, #devops, #sre, #microservices, #observability, #oauth, #metrics, #logmonitoring, and #opentracing by default, this can be changed using Lambda environment variable "TAG". The result is persisted in a RDS instance overwriting the last result.
        - twitter-case-api: Queries the previous mentioned RDS instance, called by API Gateway.

        Both uses a Lambda Layer with requests, pymysql, logger, and dotenv packages.
        Both uses Secrets Manager to manage Twitter token and MySQL credentials.
        
   ###### Metrics:
   ![Metrics](/img/Metrics.png)

        Lambda and API Gateway execution metrics, and read/write for RDS instance. 
   ###### Logs:
   ![Logs](/img/Logs.png)
        Lambda and API Gateway logs using "Key=value" pattern to facilitate the ingestion on any kind of logging tool.

## API:
   
    A POST call with an empty body triggers the scan disregarding the EventBridge rule.
    GET calls are used with the following parameters:

   ###### query= :
        - followers :  Top 5 users from the collected sample with more followers
        - hour : Amount of posts grouped by hour disregarding the hashtag
        - posts : Amount of posts per hashtag and language/country
   ###### tag= :
        - Hashtag to filter. Use with '#' to be encoded by Postman.

   **Mandatory for 'query=posts'**
        
   ###### Example:
   https://uj9dxh1hgk.execute-api.us-east-1.amazonaws.com/api?query=posts&tag=%23sre   (INACTIVE)
   ###### Response:
   ```
   {
    "query": [
        {
            "count": 11,
            "lang": "en",
            "location": ""
        },
        {
            "count": 9,
            "lang": "es",
            "location": ""
        },
        {
            "count": 4,
            "lang": "en",
            "location": "San Francisco, London, Denver"
        },
        {
            "count": 3,
            "lang": "es",
            "location": "MEXICO"
        },
        {
            "count": 3,
            "lang": "en",
            "location": "Elgin, IL"
        },
        {
            "count": 2,
            "lang": "es",
            "location": "México "
        },
        {
            "count": 2,
            "lang": "en",
            "location": "Newbury Park, California, US"
        },
        {
            "count": 2,
            "lang": "en",
            "location": "Cloud"
        },
        {
            "count": 2,
            "lang": "ja",
            "location": "Tokyo-to, Japan"
        },
        {
            "count": 2,
            "lang": "en",
            "location": "127.0.0.1"
        },
        {
            "count": 1,
            "lang": "es",
            "location": "Ciudad de México"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "San Mateo, CA"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "Toronto, Ontario"
        },
        {
            "count": 1,
            "lang": "es",
            "location": "Cd. Juarez / Chih"
        },
        {
            "count": 1,
            "lang": "es",
            "location": "Chihuahua, México."
        },
        {
            "count": 1,
            "lang": "es",
            "location": "Saltillo, Coahuila de Zaragoza"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "Northern Ireland"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "New York, NY"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "Earth"
        },
        {
            "count": 1,
            "lang": "ja",
            "location": "note→"
        },
        {
            "count": 1,
            "lang": "es",
            "location": "Puebla, México"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "Los Angeles, New York, Boston"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "San Diego, CA"
        },
        {
            "count": 1,
            "lang": "es",
            "location": "Culiacán, Sinaloa"
        },
        {
            "count": 1,
            "lang": "es",
            "location": "Pachuca de Soto, Hidalgo"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "Internet"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "Global"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "Planet Earth"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "Las Vegas, NV"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "Minneapolis"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "Bangalore , India"
        },
        {
            "count": 1,
            "lang": "nl",
            "location": "netherlands"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "Anywhere I can gain knowledge"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "United Kingdom"
        },
        {
            "count": 1,
            "lang": "es",
            "location": "New York"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "Hawaii"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "Melbourne, Australia"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "West TX"
        },
        {
            "count": 1,
            "lang": "es",
            "location": "Puebla, Tlaxcala, México"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "Gogledd Cymru, UK"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "Gilead"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "Texas"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "New Zealand"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "Birmingham, UK"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "Paris"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "In the Ocean (of Data)"
        },
        {
            "count": 1,
            "lang": "ja",
            "location": "凡事徹底｜着眼大局着手小局｜人間万事塞翁が馬"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "London, UK"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "Dublin, Ireland"
        },
        {
            "count": 1,
            "lang": "pt",
            "location": "Belo Horizonte, Brazil"
        },
        {
            "count": 1,
            "lang": "pt",
            "location": "Sao Paulo, Brazil"
        },
        {
            "count": 1,
            "lang": "en",
            "location": "Boston, MA"
        }
      ]
      }
    ```


## Deployment:
###### Requisites:
    - Twitter API token
    - Programmatic AWS credentials with admin privileges.
    - Terraform
   **THIS DEPLOYMENT ADDS RULES TO YOUR DEFAULT SECURITY GROUP TO EXPOSE RDS AS PUBLIC**
    
###### Deploy:

    Execute Terraform inside "Deployment" directory
    It's possible to change values with a variables file:
        region - Default : us-east-1
        db_ser - Default : admin
        db_passw - Default : admin123
    
    It's mandatory to provide a 'bearer_token' value with the Twitter API token from your account

    Outputs ate set to expose some relevant deployment informations:
        account_id - Account ID from the account where the app was deployed
        caller_arn - User's ARN from who executed the deployment
        caller_user - User who executed the deployment
        RDS - Database address
        CloudWatch - Dashboard name
        API - API's URL
        SG-Modified - Security Group modified with the rule "INGRESS TCP port 3306 SOURCE '0.0.0.0/0'"

