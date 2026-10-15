# Docker Cheat Sheet

The stack in `docker-compose.yml` has four services: `db` (Postgres), `migrate` (runs once), `api`, and `frontend`. Run every command from the repo root.

## Start / stop

| What | Command |
|---|---|
| Start everything (build images, run in background) | `docker compose up -d --build` |
| Start without rebuilding | `docker compose up -d` |
| Start in the foreground with logs (Ctrl+C stops it) | `docker compose up --build` |
| Stop containers (keeps data) | `docker compose stop` |
| Stop and remove containers (keeps data) | `docker compose down` |
| ⚠️ Remove everything, **including the DB and scan data** | `docker compose down -v` |
| Restart one service | `docker compose restart api` |
| Rebuild one service after code changes | `docker compose up -d --build api` (or `frontend`) |

Once it's running:

- Frontend: http://localhost:3000
- API: http://localhost:8000 (health check at `/health`)

## First account and demo data

A fresh stack has no accounts, and there is no sign-up page. The scripts in `scripts/` aren't in the API image, so mount them into a one-off API container (it shares the stack's database and scan volume):

```powershell
# First administrator. Leave out the -e lines to be prompted instead.
docker compose run --rm -v "${PWD}/scripts:/scripts:ro" -e PYTHONPATH=/app `
  -e NEUROONE_ADMIN_EMAIL=admin@example.com -e NEUROONE_ADMIN_USERNAME=admin `
  -e NEUROONE_ADMIN_PASSWORD="choose-a-password" `
  -e NEUROONE_ADMIN_FIRST_NAME=Ada -e NEUROONE_ADMIN_LAST_NAME=Admin `
  api python /scripts/bootstrap_admin.py

# Synthetic demo clinicians and patients (synthetic data only).
docker compose run --rm -v "${PWD}/scripts:/scripts:ro" -e PYTHONPATH=/app `
  api python /scripts/seed_demo_case.py
```

The seed prints the logins (`demo-clinician` and `demo-clinician-2`, password `DemoClinician!2026` unless you add `-e DEMO_PASSWORD=...`). ⚠️ Re-running it **deletes and recreates** everything those two demo accounts own, including their scan files. In Git Bash, prefix each command with `MSYS_NO_PATHCONV=1` and put a `\` at the end of each continued line instead of a backtick.

## OTP codes

OTP codes aren't emailed. By default (`OTP_DELIVERY=console`) they're printed to the API logs:

```powershell
docker compose logs -f api                              # follow live, then trigger the OTP
docker compose logs api | Select-String -Pattern otp    # search past output (PowerShell)
docker compose logs api | grep -i otp                   # same thing in bash
```

Codes live in memory, so restarting or rebuilding `api` wipes them. After a restart, sign in again to get a fresh code.

To send real emails, set `OTP_DELIVERY=email` and both `GMAIL_ADDRESS` and `GMAIL_APP_PASSWORD` in your environment or a `.env` file, then run `docker compose up -d`. The API won't start in email mode unless both are set.

## Reading logs and status

| What | Command |
|---|---|
| Show what's running and health status | `docker compose ps` |
| All logs, followed live | `docker compose logs -f` |
| One service | `docker compose logs -f frontend` |
| Last 100 lines only | `docker compose logs --tail 100 api` |
| Check whether migrations failed | `docker compose logs migrate` |

## Getting inside

| What | Command |
|---|---|
| Open a shell in the API container | `docker compose exec api sh` |
| Open a Postgres prompt | `docker compose exec db psql -U neuroone -d neuroone` |
| Run migrations again | `docker compose run --rm migrate` |
| Run any alembic command | `docker compose run --rm migrate alembic current` |

Inside `psql`, use `\dt` to list tables and `\q` to quit.

## Ports and config

- If a port is already taken: `$env:API_PORT=8001; $env:WEB_PORT=3001; docker compose up -d`
- A `.env` file in the repo root is picked up automatically, which is useful for `JWT_SECRET_KEY` and the Gmail settings.

## Cleanup and troubleshooting

| What | Command |
|---|---|
| Rebuild from scratch, ignoring the cache | `docker compose build --no-cache` |
| Remove unused images and build cache | `docker system prune` |
| See disk usage | `docker system df` |
| List volumes | `docker volume ls` |

If `api` keeps restarting or `frontend` never starts, check `docker compose logs migrate` first. The frontend waits for the API to be healthy, and the API waits for the migration to finish.
