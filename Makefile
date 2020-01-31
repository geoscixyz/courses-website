PORT=9088
ADMIN_PORT=8018

.PHONY: build symlinks run

symlinks:
	cd lib && python _symlinks.py

build: symlinks

run:
	python /Users/lindseyjh/google-cloud-sdk/bin/dev_appserver.py --host=0.0.0.0 --port=$(PORT) --admin_port=$(ADMIN_PORT) .

