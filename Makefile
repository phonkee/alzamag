.PHONY: deps
deps:
	pip-compile && pip-sync && rm requirements.txt

.PHONY: dev
dev:
	python alzamag.py --email phonkee@phonkee.eu --password 8GhNf8HP6ZUM.GqkL2TJB_A!