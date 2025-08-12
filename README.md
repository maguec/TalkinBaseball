# Talkin Baseball


## Get Python setup and load the Data

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./load_data.py
```

## Run locally

```bash
export DATABASE_URL="postgresql+psycopg2://postgres:calripken@localhost:5432/statcast"
podman run  --rm --name talkinbaseball -e "POSTGRES_PASSWORD=calripken" -e "POSTGRES_DB=statcast" -p 5432:5432 docker.io/postgres:16
```
