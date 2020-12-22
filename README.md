# twitter-case
##APP:

    <img>../img/Holistic</img>

    App consiste basicamente em 2 lambdas:
        twitter-case-scan: Que é executada através de uma regra do EventBridge a cada 5 minutos procurando pelas tags #openbanking, #remediation, #devops, #sre, #microservices, #observability, #oauth, #metrics, #logmonitoring, #opentracing e guardando em 2 tabelas em um RDS - MySQL.

        twitter-case-api: É a execução da API através do API Gateway que faz a query no RDS citado previamente.

        Ambas funçoes utilizam do Secrets Manager para gerenciar tanto o token do Twitter, quanto as credenciais do MySQL.
##Dashboard:


##API:
    Postman Collection: https://www.getpostman.com/collections/90483281af41ad868d7a
    Configurado com a URL da minha app.
    A API utiliza dos parametros passados através da URL sendo eles:

    query :
        - followers :  5 Usuários com mais seguidores.
        - hour : Total de postagens agrupadas por hora.
        - posts : Total de postagens por idioma/país filtrado por tag.
            tag :
                - Tag a ser filtrada com '#' a ser encodada pelo próprio postman, obrigatória quando usado 'posts'. (tags: #openbanking, #remediation, #devops, #sre, #microservices, #observability, #oauth, #metrics, #logmonitoring, #opentracing )



##Deploy:

    ###Requisitos:
    - Acesso programático a AWS com permissão para criar RDS Instance, Lambda Function, CloudWatch (Rules, Events, Log Groups, Dashboard), Secret Manager Secrets,  API Gateway, IAM (Roles, Policies)
    - Terraform

    Com usuário configurado com acesso programático via CLI execute o main.tf.

