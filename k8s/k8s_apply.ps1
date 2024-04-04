kubectl apply -f .\k8s\namespace.yaml

kubectl apply -f .\k8s\pg_deployment.yaml
kubectl apply -f .\k8s\pg_service.yaml

kubectl apply -f .\k8s\api_deployment.yaml
kubectl apply -f .\k8s\api_service.yaml  

kubectl apply -f .\k8s\rmq_deployment.yaml
kubectl apply -f .\k8s\rmq_service.yaml  

kubectl apply -f .\k8s\celery_deployment.yaml
kubectl apply -f .\k8s\celery_service.yaml

kubectl apply -f .\k8s\flower_deployment.yaml
kubectl apply -f .\k8s\flower_service.yaml

kubectl apply -f .\k8s\nginx_configmap.yaml
kubectl apply -f .\k8s\nginx_deployment.yaml
kubectl apply -f .\k8s\nginx_services.yaml
kubectl apply -f .\k8s\ingress.yaml

sleep 10
kubectl apply -f .\k8s\pg_job.yaml  