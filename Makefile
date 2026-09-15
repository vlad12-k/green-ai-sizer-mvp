PYTHON ?= python3
.PHONY: check verify verify-release
check: verify
verify:
	$(PYTHON) scripts/verify.py
verify-release:
	$(PYTHON) scripts/verify.py --release
