ifneq (,$(wildcard ./.env))
    include .env
    export
endif

PY_VER=py310
PYTHON=$(VENV)/bin/python3
VENV=env
CODE_DIRS=audio_shader
LINE_LEN=120

build:
	docker build -t ${IMAGE_NAME} .


style: $(VENV)
	$(PYTHON) -m autoflake -r -i --remove-all-unused-imports --remove-unused-variables $(CODE_DIRS)
	$(PYTHON) -m isort $(CODE_DIRS) --line-length $(LINE_LEN) 
	$(PYTHON) -m autopep8 -a -r -i --max-line-length=$(LINE_LEN) $(CODE_DIRS) 
	$(PYTHON) -m black --line-length $(LINE_LEN) --target-version $(PY_VER) $(CODE_DIRS)

quality: $(VENV)
	$(PYTHON) -m black --check --line-length $(LINE_LEN) --target-version $(PY_VER) $(CODE_DIRS)
	$(PYTHON) -m flake8 --max-line-length $(LINE_LEN) $(CODE_DIRS)


check:
	$(MAKE) style
	$(MAKE) quality


$(VENV):
	git submodule update --init --recursive
	python3 -m virtualenv -p $(PY_VER) $(VENV)
	$(PYTHON) -m pip install --upgrade pip==23.1.2
	$(PYTHON) -m pip install --upgrade pip setuptools wheel
	$(PYTHON) -m pip install -r requirements.txt

clean:
	rm -rf */*/*.js */*/*.map node_modules env bower_components static/gen

reset:
	$(MAKE) clean
	$(MAKE) check

init:
	$(MAKE) $(VENV)

run:
	bash scripts/init.sh
	${PYTHON} audio_shader