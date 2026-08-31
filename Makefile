.PHONY: install test download ingest clean

install:
	uv sync

test:
	uv run pytest -v

download:
	uv run python -m src.download

ingest:
	uv run python -m src.ingest

clean:
	rm -rf data/interim

score:
	uv run python -m src.evaluate
