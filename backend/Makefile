help: 
	@grep -E '^[.a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

test:
	rye run pytest

mypy:
	rye run mypy .

fmt:
	rye run ruff format .

lint:
	rye run ruff check . --fix

mdformat:
	rye run mdformat . --number

spell:
	rye run codespell --skip=logs/**,data/**,*.ipynb

nbstrip:
	rye run nbstripout notebooks/*.ipynb --drop-empty-cells

format: lint fmt mypy mdformat spell nbstrip 
