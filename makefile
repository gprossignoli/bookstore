refresh-env:
	docker-compose down --remove-orphans
	docker volume prune
	docker-compose build --no-cache
remove-env:
	docker-compose down
	docker volume prune
relaunch-env:
	docker-compose down
	docker volume prune
	docker-compose build --no-cache
	docker-compose -f docker-compose.yml -f docker-compose-kafka.yml up -d
launch-env:
	docker-compose -f docker-compose.yml -f docker-compose-kafka.yml up -d
