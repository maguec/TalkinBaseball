# Talkin Baseball

![map](./docs/diagram.png)

## Prerequisites
[uv](https://docs.astral.sh/uv/getting-started/installation/)


## Get Python setup and load the Data


## Load data

### Create database

```bash
export DATABASE_URL="postgresql+psycopg2://postgres:PASSWORD@HOSTNAME:5432/postgres"
psql ${DATABASE_URL=} 
> create database statcast
```

### Load data

```bash
export DATABASE_URL="postgresql+psycopg2://postgres:PASSWORD@HOSTNAME:5432/statcast"
cd data
uv run load_pitches.py
uv run load_players.py
uv run load_players.py
```

### Load Bigtable data
```bash
vim Makefile
#replace project name with your own
make btsetup

```


### Configure toolbox

```bash
cd Agent
echo "GOOGLE_GENAI_USE_VERTEXAI=1" > .env
echo "GOOGLE_CLOUD_PROJECT=MYPROJECTNAME" >> .env
echo "GOOGLE_CLOUD_LOCATION=us-west1" >> .env
make
# edit the sources in tools.yaml to match your environment
# download the version for your os
make runtoolbox
```

### Run the ADK in another window

```bash
cd Agent
uv run adk web
```
