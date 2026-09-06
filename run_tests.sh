#!/bin/bash
export DATABASE_URL="postgresql://neobank_test:test123@localhost:5432/neobank_test"
venv/bin/python -m pytest test_smoke.py -v
