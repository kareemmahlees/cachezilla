setup:
	@docker compose up -d benchmark_db
	@python ./db.py
	@python ./api.py
benchmark_no_cache:
	@k6 run benchmark_no_cache.ts
benchmark_cache:
	@k6 run benchmark_cache.ts
clean_up:
	@docker compose down
