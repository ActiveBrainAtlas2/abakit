UNAME = $(shell uname)
ifeq ($(UNAME),Darwin)
	OPEN = open
endif
ifeq ($(UNAME),Linux)
	OPEN = xdg-open
endif

.PHONY: init
init:
	# Create local dev conda env
	conda env create -f dev/environment.yml -p dev/env
	# Install this package in editable mode
	dev/env/bin/pip install -e .

.PHONY: up
up:
	# Update local dev conda env
	conda env update -f dev/environment.yml -p dev/env --prune

.PHONY: fmt
fmt:
	black .

.PHONY: lint
lint:
	pylint src/abakit tests

.PHONY: test
test:
	pytest tests

.PHONY: doc
doc:
	# Remove existing API docs to build from scratch
	rm -rf docs/{_build,api}
	# Build HTML output
	cd docs && make html

.PHONY: doc-preview
doc-preview:
	$(OPEN) docs/_build/html/index.html

.PHONY: clean
clean:
	rm -rf .pytest_cache
	rm -rf docs/{_build,api}
	rm -rf src/*.egg-info
	find {src,tests} -type d -name "__pycache__" -exec rm -rf "{}" \;
