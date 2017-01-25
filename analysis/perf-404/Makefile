NOTEBOOKS=$(wildcard *.ipynb)
RENDERS=$(NOTEBOOKS:%.ipynb=results/%.html)

default: ${RENDERS}

.PHONY: requirements
requirements:
	pip install -r requirements.txt

results/%.html: %.ipynb
	jupyter-nbconvert --to html --execute $<
	mv $(@:results/%=%) $@
