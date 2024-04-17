.ONESHELL:
.PHONY: all configure install restart test

ENVIRONMENT ?= production

all:
	set -eu -o pipefail

configure:
	ansible-playbook site.yml --inventory inventory/$(ENVIRONMENT) --tags "configure"

test:
	cd ansible
	ansible-playbook site.yml -i inventory/$(ENVIRONMENT) --tags "test"