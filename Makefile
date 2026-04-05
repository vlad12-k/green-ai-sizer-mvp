.PHONY: check

check:
	python -m unittest discover -s tests -p "test_*.py"
	python scripts/smoke_check.py
