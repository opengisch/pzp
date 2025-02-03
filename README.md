# Plugin Piani Zone di Pericolo

Processing provider plugin.

## Documentation

The user manual (ita) is published here: https://opengisch.github.io/pzp/

## Run tests

To run unit tests locally, first install Docker and then run this docker command from the PZP repo's root folder:

```bash
docker run --rm -e PYTHONPATH=/usr/share/qgis/python/plugins -v $PWD:/usr/src -w /usr/src qgis/qgis:latest sh -c 'xvfb-run pytest'
```
