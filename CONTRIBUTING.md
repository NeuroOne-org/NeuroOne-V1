# NeuroONE Contributing Guide

Thank you for contributing to NeuroONE. This guide defines the expected
architecture, branch workflow, coding standards, migration process, and
definition of done for every contribution.

## Project Structure

Each team owns its assigned feature repository. All code should follow this
flow:

```text
Feature -> API -> Service -> Repository -> Model -> Schema
```

Keep business logic out of API routes and avoid direct database access from
endpoints.

## Branch Strategy

The protected main branch is:

```text
main
```

Create a feature branch for each change. Examples include:

- `feature/auth`
- `feature/patients`
- `feature/diagnosis`
- `feature/rag-reports`

Never commit directly to `main`. Open a pull request for every feature.

## Commit Message Convention

Use clear, focused commit messages. Start each message with the type of change:

```text
feat: add patient CRUD
fix: correct JWT expiration
refactor: move diagnosis logic to service
docs: update API documentation
test: add authentication tests
```

## Pull Request Checklist

Before opening a pull request, confirm that:

- [ ] The project builds successfully.
- [ ] The branch has no merge conflicts.
- [ ] The code is formatted.
- [ ] The API has been tested.
- [ ] New migrations have been reviewed.
- [ ] Documentation has been updated, if required.

## Coding Standards

- Use type hints.
- Keep functions small and focused.
- Follow PEP 8.
- Store business logic inside services.
- Access the database only through repositories.
- Validate requests and responses with Pydantic schemas.
- Use meaningful variable and function names.

## Alembic Migration Policy

Only the Platform & Authentication maintainer should generate Alembic
migrations for the shared integration branch.

### Workflow

1. Team members modify models in their feature branches.
2. Before merging, resolve model conflicts.
3. Generate one migration from the `backend` directory:

   ```bash
   alembic revision --autogenerate -m "description"
   ```

4. Review the generated migration carefully.
5. Apply it:

   ```bash
   alembic upgrade head
   ```

Avoid multiple independent migrations for the same schema changes.

## API Standards

Successful responses should follow this shape:

```json
{
  "success": true,
  "data": {}
}
```

Error responses should follow this shape:

```json
{
  "success": false,
  "message": "A clear description of the error.",
  "details": {}
}
```

Use appropriate HTTP status codes and version all routes under `/api/v1`.

## Repository Ownership

| Repository | Owner |
| --- | --- |
| Repository 1 | Platform & Authentication |
| Repository 2 | Patient Management |
| Repository 3 | Visits & AI Diagnosis |
| Repository 4 | RAG & Reports |

## Testing

Every feature should include:

- Unit tests for services.
- API endpoint tests.
- Manual verification using Swagger UI or Postman.

## Definition of Done

A feature is complete only when:

- [ ] The code is implemented.
- [ ] The API works.
- [ ] All tests pass.
- [ ] Documentation is updated.
- [ ] The migration is verified, if applicable.
- [ ] The pull request is approved.
