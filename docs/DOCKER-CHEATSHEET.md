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
