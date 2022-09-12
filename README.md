# OpenDSS

Docker Interface for OpenDSS

## Requirements

* UNIX/WSL
* [Docker 20 or later](https://docs.docker.com/)

## Build
You can build the Docker container by going to the root folder and executing the following command.

```
docker build --rm -f Dockerfile -t "opendss" .
```

This will create a new Docker image with tag `opendss`. 

## Usage
You can run an OpenDSS simulation using the `opendss` Docker image by opening a terminal in the folder where your simulation file is present and then running it with a `.DSS` file as input. Optionally, a `.json` output path can be specified to log machine readable results to a file. 

```
docker run --rm -v <source_volume>:<target_volume> opendss <input_path> <output_path>
```

## Example

Running the following command with the given example from **UNIX/WSL** terminal after building the Docker image.

```
docker run --rm -v "$(pwd)":"$(pwd)" opendss "$(pwd)"/Main_GNF.DSS Main_GNF.json
```

Running on **Windows** requires manually setting the folder structure as follows.

```
docker run --rm -v "${PWD}":/usr/src/app/data opendss /usr/src/app/data/Main_GNF.DSS Main_GNF.json
```

This should generate a `./Main_GNF.json` file and output the following to the terminal:

```
Phase voltage magnitudes for each bus:
Bus 0.1 5917.8 V
Bus 0.2 5917.8 V
Bus 0.3 5917.8 V
Bus 4.1 233.52 V
Bus 4.2 233.52 V
Bus 4.3 233.52 V
Bus 1.1 232.41 V
Bus 1.2 232.41 V
Bus 1.3 232.41 V
Bus 2.1 233.1 V
Bus 2.2 233.1 V
Bus 2.3 233.1 V
Bus 3.1 230.92 V
Bus 3.2 230.92 V
Bus 3.3 230.92 V
Bus 7.1 232.15 V
Bus 7.2 232.15 V
Bus 7.3 232.15 V
Bus 8.1 232.9 V
Bus 8.2 232.9 V
Bus 8.3 232.9 V
Bus 9.1 230.75 V
Bus 9.2 230.75 V
Bus 9.3 230.75 V
Phase current magnitudes and angles for each line:
Line 1.1 17.23 A /_ -30.29
Line 1.2 17.23 A /_ -150.29
Line 1.3 17.23 A /_ 89.71
Line 2.1 12.88 A /_ -30.27
Line 2.2 12.88 A /_ -150.27
Line 2.3 12.88 A /_ 89.73
Line 3.1 11.56 A /_ -30.34
Line 3.2 11.56 A /_ -150.34
Line 3.3 11.56 A /_ 89.66
Line 4.1 17.23 A /_ -30.29
Line 4.2 17.23 A /_ -150.29
Line 4.3 17.23 A /_ 89.71
Line 5.1 12.88 A /_ -30.27
Line 5.2 12.88 A /_ -150.27
Line 5.3 12.88 A /_ 89.73
Line 6.1 11.56 A /_ -30.34
Line 6.2 11.56 A /_ -150.34
Line 6.3 11.56 A /_ 89.66
Output written to: Main_GNF.json
```
