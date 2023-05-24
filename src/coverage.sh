#!/bin/bash

PYTHONPATH=. coverage run --branch -p ../examples/pt-br/00-completo.py
coverage combine
coverage html