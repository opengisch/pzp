![Unit tests](https://github.com/opengisch/pzp/actions/workflows/test.yml/badge.svg) [![Release](https://img.shields.io/github/v/release/opengisch/pzp.svg)](https://github.com/opengisch/pzp/releases)

# Plugin Piani Zone di Pericolo

Processing provider plugin.

## Documentation

The user manual (ita) is published here: https://opengisch.github.io/pzp/

## Development

### Run tests

To run unit tests locally, first install Docker and then run this docker command from the PZP repo's root folder:

```bash
docker run --rm -e PYTHONPATH=/usr/share/qgis/python/plugins -v $PWD:/usr/src -w /usr/src qgis/qgis:latest sh -c 'xvfb-run pytest'
```

### Layer Style definitions (.QML)

When exporting .QML files for integration in the plugin select these categories:

- LayerConfiguration
- Symbology
- Labeling
- Fields
- Forms
