refresh-env:
	docker compose down
	docker volume prune
	docker compose build
remove-env:
	docker compose down
	docker volume prune
