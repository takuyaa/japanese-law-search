# Japanese Law Search

## Setup

### Prerequisites

- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/)

### Install dependencies

```shell
poetry install
```

### Download data

Download `all.zip` from [e-Gov法令検索](https://elaws.e-gov.go.jp/download/) and `unzip` it into the `data` directory.

```shell
unzip all_xml.zip -d ./data
```

### Elasticsearch

Start Elasticsearch & Kibana:
```shell
make -C elasticsearch start
```

Create an index:
```shell
make -C elasticsearch create-index
```

### Index

```shell
make index
```

## Run app

```shell
make run
```

Then, visit http://localhost:8501/
