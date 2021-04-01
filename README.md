# Nanome - Electrostatic Potential

A Nanome Plugin to calculate electrostatic potential map.

## Dependencies

[Docker](https://docs.docker.com/get-docker/)

When running outside of Docker:

This plugin requires `APBS-PDB2PQR` installed and add execution path to one of the following
1) environment variables `APBS` and `PDB2PQR`
2) environment variable `PATH`
3) in `esp_config.py`

Installation instructions for `APBS-PDB2PQR` can be found [here](https://apbs-pdb2pqr.readthedocs.io/)

## Usage

To run Electrostatic Potential in a Docker container:

```sh
$ cd docker
$ ./build.sh
$ ./deploy.sh -a <plugin_server_address> [optional args]
```

## Development

To run Electrostatic Potential with autoreload:

```sh
$ python3 -m pip install -r requirements.txt
$ python3 run.py -r -a <plugin_server_address> [optional args]
```

## License

MIT
