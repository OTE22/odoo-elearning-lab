# Shortcuts for the most common tasks. Run `make help` to list them.
-include .env
export

DB      ?= $(ODOO_DB)
MODULES := nova_course_proposal_writing,nova_course_digital_safety
COMPOSE := docker compose
ODOO    := $(COMPOSE) run --rm odoo odoo

.PHONY: help up down logs init update test shell psql backup restore prod-up clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

up: ## Build the image and start Odoo + Postgres in the background
	$(COMPOSE) up -d --build

down: ## Stop the stack (data is kept in volumes)
	$(COMPOSE) down

logs: ## Follow Odoo logs
	$(COMPOSE) logs -f odoo

init: ## Create the database with Arabic and install both courses
	$(ODOO) -d $(DB) -i $(MODULES) --load-language=ar_001 --without-demo=all --stop-after-init
	@echo "Open http://localhost:$(ODOO_PORT) and log in with admin / admin (change it!)"

update: ## Re-load course data after you edit the XML
	$(ODOO) -d $(DB) -u $(MODULES) --stop-after-init

test: ## Run the module tests in a throwaway database
	$(ODOO) -d test_$(DB) -i $(MODULES) --test-enable --test-tags=/nova_course_proposal_writing,/nova_course_digital_safety --without-demo=all --stop-after-init --log-level=test
	$(COMPOSE) exec db dropdb -U $(POSTGRES_USER) --if-exists test_$(DB)

shell: ## Open an Odoo Python shell on the database
	$(ODOO) shell -d $(DB)

psql: ## Open a psql prompt on the database
	$(COMPOSE) exec db psql -U $(POSTGRES_USER) $(DB)

backup: ## Back up the database and filestore to ./backups
	./ops/scripts/backup.sh

restore: ## Restore a backup: make restore FILE=backups/xxx.tar.gz
	./ops/scripts/restore.sh $(FILE)

prod-up: ## Start the production stack behind Nginx
	$(COMPOSE) -f docker-compose.yml -f ops/docker-compose.prod.yml up -d --build

clean: ## Stop everything and DELETE all data volumes
	$(COMPOSE) down -v
