COVERAGE=coverage
TEST=test.py

.PHONY: all
all: release

.PHONY: release
release: pylint mypy test clean build tag push upload

.PHONY: setup
setup:
	pip install -r requirements.txt

.PHONY: setup_test
setup_test: setup
	pip install -r requirements-test.txt

.PHONY: setup_analysis
setup_analysis: setup
	pip install -r requirements-analysis.txt

.PHONY: setup_release
setup_release:
	pip install -r requirements-release.txt

.PHONY: get_version
get_version: get_toml_version get_init_version get_sonar_version
	if [ "${TOML_VERSION}" != "${INIT_VERSION}" ] || [ "${TOML_VERSION}" != "${SONAR_VERSION}" ]; then \
		echo "Version mismatch"; \
		exit 1; \
	fi
	$(eval VERSION=$(TOML_VERSION))

.PHONY: get_init_version
get_init_version:
	$(eval INIT_VERSION=v$(shell grep __version__ bigboat/__init__.py | sed -E "s/__version__ = .([0-9.]+)./\\1/"))
	$(info Version in __init__.py: $(INIT_VERSION))
	if [ -z "${INIT_VERSION}" ]; then \
		echo "Could not parse version"; \
		exit 1; \
	fi

.PHONY: get_toml_version
get_toml_version:
	$(eval TOML_VERSION=v$(shell grep "^version" pyproject.toml | sed -E "s/version = .([0-9.]+)./\\1/"))
	$(info Version in pyproject.toml: $(TOML_VERSION))

.PHONY: get_sonar_version
get_sonar_version:
	$(eval SONAR_VERSION=v$(shell grep projectVersion sonar-project.properties | cut -d= -f2))
	$(info Version in sonar-project.properties: $(SONAR_VERSION))

.PHONY: pylint
pylint:
	pylint *.py bigboat/*.py tests/*.py

.PHONY: mypy
mypy:
	mypy *.py bigboat tests --html-report mypy-report --cobertura-xml-report mypy-report --junit-xml mypy-report/junit.xml --no-incremental --show-traceback

.PHONY: tag
tag: get_version
	git tag $(VERSION)

.PHONY: build
build:
	python -m build

.PHONY: push
push: get_version
	git push origin $(VERSION)

.PHONY: upload
upload:
	twine upload dist/*

.PHONY: test
test:
	python $(TEST)

.PHONY: coverage
coverage:
	$(COVERAGE) run --branch --source=bigboat,tests $(TEST)
	$(COVERAGE) report -m
	$(COVERAGE) xml -i

.PHONY: clean
clean:
	rm -rf build/ dist/ bigboat.egg-info .coverage
