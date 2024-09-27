## order
apply -f postgres-storage-class.yaml
apply -f postgres-persistent-volume.yaml
apply -f postgres-persistent-volume-claim.yaml
apply -f postgres-configmap.yaml 
apply -f postgres-statefulset.yaml 
apply -f postgres-service.yaml 