refresh-env:
	docker-compose down
	docker volume prune
	docker-compose build --no-cache
remove-env:
	docker-compose down
	docker volume prune
relaunch-env:
	docker-compose down
	docker volume prune
	docker-compose build --no-cache
	docker-compose up -d