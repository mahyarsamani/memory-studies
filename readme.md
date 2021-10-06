# Memory Studies in gem5

This repo contains scripts to run experiments to check the accuracy of
statistics provided by models in gem5 that relate to the memory subsystem.

## Note

Please make sure you have created a virtual environment with gem5art installed.
You can run launch_memory_studies.py using the python in your venv.

## Installation guide

If you do not already have virtualenv installed please install virtualenv. You
can do that using:

```
sudo apt update
sudo apt install virtualenv
```

Create a virtual environment with python3 like below:

```
virtualenv -p python3 venv
```

Activate your virtual environment like below (tested for bash and zsh):

```
source venv/bin/activate
```

Install gem5art:

```
pip install gem5art.run gem5art.artifact gem5art.tasks
```

Then just simply do:

```
python launch_memory_studies.py
```
