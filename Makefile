install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	#editing makefile
	#PYTHONPATH=. && pytest -vv --cov=paws --cov=spot-price-ml tests/*.py
	#PYTHONPATH=. && py.test --nbval-lax notebooks/*.ipynb

lint:
	pylint --disable=R,C,W1203 example_src/*.py

all: install lint test
