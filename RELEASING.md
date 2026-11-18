# Releasing

Run the full optional-adapter test suite, build both distribution formats, inspect package contents, and validate metadata:

```bash
python -m pip install -e '.[all,dev]'
python -m pytest -q
python -m build
python -m twine check --strict dist/*
```

Update the package version in `pyproject.toml` and `src/sdkbench/__init__.py`, build from the tested commit and tag the release. Upload credentials must remain outside the repository. A first release may be uploaded with a PyPI API token in the publishing process environment.

The bundled GitHub release workflow supports PyPI Trusted Publishing after manual account configuration:

- Owner: `sdkbench-org`
- Repository: `sdkbench`
- Workflow filename: `publish.yml`
- GitHub environment: `pypi`

Configure that publisher in PyPI and create the matching GitHub environment before publishing a GitHub release. The workflow does not configure trust itself. It tests, builds and checks distributions before uploading via OIDC. No token is stored in the workflow.

After upload, verify PyPI artifact hashes and install the published version into a fresh environment. PyPI release files cannot be overwritten.
