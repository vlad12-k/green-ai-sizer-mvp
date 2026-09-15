"""One offline verification entry point; release mode adds evidence freshness."""
import argparse
import ast
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    subprocess.run(args, cwd=ROOT, check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--release', action='store_true')
    args = parser.parse_args()
    for directory in ('app', 'scripts', 'tests', 'workbook'):
        for path in (ROOT / directory).rglob('*.py'):
            ast.parse(path.read_text(), filename=str(path))
    for path in list((ROOT / 'app').rglob('*.json')) + list((ROOT / 'docs/evidence').glob('*.json')):
        json.loads(path.read_text())
    for path in ROOT.glob('*.md'):
        if len(re.findall(r'^```', path.read_text(), re.MULTILINE)) % 2:
            raise ValueError(f'Unbalanced code fences: {path.name}')
    run('node', '--check', 'docs/app.js')
    run(sys.executable, '-m', 'unittest', 'discover', '-s', 'tests')
    run(sys.executable, 'scripts/smoke_check.py')
    run(sys.executable, 'workbook/evidence.py', '--check', *(['--fresh'] if args.release else []))
    run(sys.executable, 'workbook/calc_co2e.py', '200')
    print('PASS: release verification' if args.release else 'PASS: offline verification')


if __name__ == '__main__':
    main()
