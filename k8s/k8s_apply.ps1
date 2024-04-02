kubectl apply -f .\k8s\pg_deployment.yaml
kubectl apply -f .\k8s\pg_service.yaml
kubectl apply -f .\k8s\pg_job.yaml  

kubectl apply -f .\k8s\api_deployment.yaml
kubectl apply -f .\k8s\api_service.yaml  

kubectl apply -f .\k8s\rmq_deployment.yaml
kubectl apply -f .\k8s\rmq_service.yaml  

kubectl apply -f .\k8s\celery_deployment.yaml
kubectl apply -f .\k8s\celery_service.yaml
