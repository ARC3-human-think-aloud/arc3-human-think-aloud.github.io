"""Bind a prepared static website to a public HF Dataset repository (offline)."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import quote


def configure(website, repo, revision='main'):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*', repo):
        raise ValueError('Expected Hugging Face repository: owner/dataset-name')
    if not revision or any(c in revision for c in '\r\n'):
        raise ValueError('A branch, tag, or commit revision is required')
    if not (website / 'index.html').is_file():
        raise ValueError(f'No static website at {website}')
    base = f'https://huggingface.co/datasets/{repo}/resolve/{quote(revision, safe="")}/'
    config = {'datasetBaseUrl': base, 'datasetRepo': repo, 'datasetRevision': revision}
    (website / 'site-config.js').write_text('window.SITE_CONFIG = ' + json.dumps(config) + ';\n')
    print(f'Configured {website / "site-config.js"}\nDataset: {base}')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('repo', help='owner/dataset-name; no token required')
    p.add_argument('--revision', default='main', help='Prefer a release tag or commit for reproducibility')
    p.add_argument('--website', type=Path, default=Path(__file__).resolve().parents[1])
    a = p.parse_args()
    configure(a.website, a.repo, a.revision)
