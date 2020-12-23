# twitter-case
## APP:

   ![HolisticView](/img/Holistic.png)

        twitter-case-scan: Que é executada através de uma regra do EventBridge a cada 12 horas procurando pelos ultimos 100 posts com as tags #openbanking, #remediation, #devops, #sre, #microservices, #observability, #oauth, #metrics, #logmonitoring, #opentracing e guardando em 2 tabelas em um RDS - MySQL.
   
   ###### Tabelas
   ![Tables](/img/Tables.png)

   ###### Lambdas:

        - twitter-case-scan: Que é executada através de uma regra do EventBridge a cada 12 horas, ou através do POST na API procurando pelas tags #openbanking, #remediation, #devops, #sre, #microservices, #observability, #oauth, #metrics, #logmonitoring, #opentracing e guardando em 2 tabelas em um RDS - MySQL. A cada scan, os dados anteriores são descartados e uma nova escrita é feita.

        - twitter-case-api: É a execução da API através do API Gateway que faz a query no RDS citado previamente.
        
        Ambas utilizam uma Lambda Layer com os pacotes requests, pymysql, logger e dotenv.
        Ambas funçoes utilizam do Secrets Manager para gerenciar tanto o token do Twitter, quanto as credenciais do MySQL.

## Dashboard:
    O Dashboard foi criado dentro do ClowdWatch, pode ser acessado publicamente.
**Importante**
    Deixei alguns schedules para chamar as APIs para que sejam geradas métricas no dashboard.
   https://cloudwatch.amazonaws.com/dashboard.html?dashboard=Twitter-Case&context=eyJSIjoidXMtZWFzdC0xIiwiRCI6ImN3LWRiLTI0OTYxNTQ5MTAyMSIsIlUiOiJ1cy1lYXN0LTFfVFhOdFg2eW55IiwiQyI6IjNxbzJnZmQwdnBqNmhlb2k2Z3E4aGRhYWo2IiwiSSI6InVzLWVhc3QtMTplOTgyMDY0MC1lMzA1LTRiNzctOTQ4YS04YjlmMTI1MzY2ZDkiLCJNIjoiUHVibGljIn0=

   ###### Metrics:
   ![Metrics](/img/Metrics.png)

        Métricas de execução das lambdas e da API Gateway. Além de métricas de leitura/escrita no RDS.
   ###### Logs:
   ![Logs](/img/Logs.png)
        Logs das lambdas e da API Gateway, são segmentadas com chave="valor" para facilitação de leitura por qualquer serviço de ingestão de logs.

## API:
   ###### Postman Collection:
   https://www.getpostman.com/collections/90483281af41ad868d7a

        Dentro da coleção existem 1 POST e 3 GETs configurados com a URL da minha app.
        O POST deve ser rodado para fazer o scan independente do schedule de 1 a cada 12 horas (Ex. logo após o deploy)
        As demais requisições GET são utilizadas conforme descrito abaixo:

   ###### query= :
        - followers :  5 Usuários com mais seguidores.
        - hour : Total de postagens agrupadas por hora.
        - posts : Total de postagens por idioma/país filtrado por tag.
   ###### tag= :
        - Tag a ser filtrada com '#' a ser encodada pelo próprio postman

   **Obrigatória quando usado 'posts'**
        
   ###### Exemplo:
   https://uj9dxh1hgk.execute-api.us-east-1.amazonaws.com/api?query=posts&tag=%23sre   
   ###### Resposta:
   `{
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
      }`


## Deploy:
###### Requisitos:
    - Acesso programático a AWS com permissão de administrador.
    - Terraform
   **ESTE DEPLOY ALTERA O SG PADRÃO EM QUE O RDS FOR PROVISIONADO PARA QUE O RDS SEJA PUBLICO**
    
###### Deploy:

    Com usuário configurado com acesso programático via CLI execute o terraform dentro do diretorio "Deployment"
    Opcionalmente pode-se alterar as variaveis através de um arquivo de variaveis para alterar:
    region - Default : us-east-1
    db_ser - Default : admin
    db_passw - Default : admin123
    bearer_token - Default : AAAAAAAAAAAAAAAAAAAAAHeYKwEAAAAAqtWmWFb%2BH3Rp1Yu0BW8YfM7yGKc%3Dof6VSt8LQua4KKEzEop6aI7TIOMXz8vLcsbwmA1NVsiJsChPXI
    Os Outputs estão configurados para expor algumas informações relevantes do deploy:
    account_id - Account ID onde foi feito o deploy
    caller_arn - ARN do user que executou o deploy
    caller_user - User que executou o deploy
    RDS - Endereço do banco de dados criado
    CloudWatch - Nome do Dashboard criado
    API - URL da API
    SG-Modified - Security Group que foi alterado com a inclusão da regra INGRESS TCP porta 3306 SOURCE "0.0.0.0/0"

