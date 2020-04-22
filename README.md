# Nanome - Electrostatic Potential

A Nanome plugin to calculate electrostatic potential map

### Preparation

Install the latest version of [Python 3](https://www.python.org/downloads/)

| NOTE for Windows: replace `python3` in the following commands with `python` |
| --------------------------------------------------------------------------- |


Install the latest `nanome` lib:

```sh
$ python3 -m pip install nanome --upgrade
```

### Dependencies

This plugin requires `APBS-PDB2PQR` installed and add execution path to one of the following
1) environment variables `APBS` and `PDB2PQR`
2) environment variable `PATH`
3) in `esp_config.py`

Installation instructions for `APBS-PDB2PQR` can be found [here](https://apbs-pdb2pqr.readthedocs.io/)

### Installation

To install Electrostatic Potential:

```sh
$ python3 -m pip install nanome-electrostatic-potential
```

### Usage

To start Electrostatic Potential:

```sh
$ nanome-electrostatic-potential -a <plugin_server_address> [optional args]
```

### Docker Usage

To run Electrostatic Potential in a Docker container:

```sh
$ cd docker
$ ./build.sh
$ ./deploy.sh -a <plugin_server_address> [optional args]
```

### Development

To run Electrostatic Potential with autoreload:

```sh
$ python3 run.py -r -a <plugin_server_address> [optional args]
```

### License

MIT
