kubectl delete --all deployments -n seo 
kubectl delete --all services -n seo 


kubectl delete -f .\k8s\nginx_configmap.yaml
kubectl delete -f .\k8s\ingress.yaml
