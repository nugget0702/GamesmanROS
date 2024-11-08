VIRTUALENV ?= env
PYTHONVERSION ?= python3
PYTHON = $(VIRTUALENV)/bin/$(PYTHONVERSION)
VENV_FLAGS = -q --python=$(PYTHONVERSION)

all: dist

$(VIRTUALENV): requirements.txt
	$(PYTHONVERSION) -m venv $@
	$(PYTHON) -m pip install --upgrade pip setuptools wheel
	./$@/bin/pip install -r requirements.txt

.PHONY: dist
dist: $(VIRTUALENV)
	( \
		. $^/bin/activate; \
		pyinstaller src/main.py --onefile --name AbiDecoder; \
	)

.PHONY: clean
clean:
	$(RM) -r $(VIRTUALENV)
	$(RM) -r */*.egg-info */__pycache__ build  dist __pycache__ *.egg-info *.spec
	find . -name "*.py[co]" -delete