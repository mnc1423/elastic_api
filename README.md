## Elastic REST API

### Install and Deploy
```
# If elasticsearch is installed
docker compose build
docker compose -f docker-compose.yaml up -d
```

### Template file
```
/app/template/vectorDB_template.json

# Create Template in Elasticsearch
POST /insert/vectordb_template 

```

