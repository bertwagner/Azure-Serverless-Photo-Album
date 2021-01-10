.PHONY: requirements dev-environment resource new-functionapp new-function deploy-functionapp

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PYTHON_INTERPRETER = python3

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python Dependencies
requirements: 
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

dev-environment: requirements
	sudo apt install python3-venv
	$(PYTHON_INTERPRETER) -m venv .venv

resources:
	bash 01-Create Azure Infrastructure.sh

new-functionapp:
	func init --python

new-function:
	func new --name "photos" --template "HTTP trigger" --authlevel "anonymous"

deploy-functionapp:
	func azure functionapp publish serverless-photo-album-app

