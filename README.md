# RAG using Haystack and Elasticsearch

## Goal 

## Installation 

We will create a docker network because we have two apps running inside of a container, elasticsearch and streamlit

```
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.14.3
```
```
docker network create mynetwork
```
```
docker run -d --name elasticsearch --network mynetwork -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "xpack.security.transport.ssl.enabled=false" -e "ELASTIC_PASSWORD=testpassword" docker.elastic.co/elasticsearch/elasticsearch:8.14.3

```
```
cd Docker
```
```
docker build -t streamlit-app . --network host
```
```
docker run -d -p 8501:8501 --name streamlit-app --network mynetwork -e ELASTIC_PASSWORD=testpassword streamlit-app
```


