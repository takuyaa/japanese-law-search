ELASTICSEARCH_URL="http://localhost:9200"
INDEX_NAME="ja_law"
INDEX_URL=$(ELASTICSEARCH_URL)/$(INDEX_NAME)

.PHONY: start
start:
	@docker compose up -d

.PHONY: stop
stop:
	@docker compose down

.PHONY: clear
clear: stop
	@docker volume rm elasticsearch_esdata01
	@docker volume rm elasticsearch_kibanadata

.PHONY: create-index
create-index:
	@curl -H "Content-Type: application/json" -X PUT -d "@index.jsonc" "$(INDEX_URL)?pretty"

.PHONY: delete-index
delete-index:
	@curl -X DELETE "$(INDEX_URL)?pretty"
