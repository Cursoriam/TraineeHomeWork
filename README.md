# Pitter Sync

### Sync service for Pitter project


### Usage

- `make up` - Run in docker-compose
- `make down` - Stop and remove docker-compose services
- `make lint` - Run linter
- `make format` - Run auto-formatter for src/
- `make test` - Run tests

Add your private key path to encode by `RS256` in `JWT_PRIVATE_KEY_PATH = os.path.abspath()` into `pitter/settings.py`

