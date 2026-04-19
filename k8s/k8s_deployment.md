# Развертывание в Kubernetes

## Обзор

Проект SFMShop развертывается в Kubernetes с использованием Deployment и Service.

## Компоненты

- **Deployment**: 3 реплики приложения
- **Service**: LoadBalancer для внешнего доступа

## Развертывание
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

## Масштабирование
kubectl scale deployment sfmshop-deployment --replicas=5

