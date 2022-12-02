.PHONY: start-db
start-db:
	docker run --name aoc -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres:latest

.PHONY: stop-db
stop-db:
	docker container stop aoc
	docker rm aoc

.PHONY: aoc
aoc:
	docker cp input aoc:/tmp/input
	cat ./solution.sql | docker exec -i aoc psql --echo-queries --username postgres -d postgres