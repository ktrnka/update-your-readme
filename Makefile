install-uv:
	curl -LsSf https://astral.sh/uv/install.sh | sh

install:
	uv sync --all-extras --dev

test:
	uv run pytest
	