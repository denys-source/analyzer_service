# analyzer_service

FastAPI service for PII redaction, website scam analysis, and QR code URL analysis.

## APIs

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/redact` | Redact PII from text (Microsoft Presidio) |
| `POST` | `/api/v1/analyze` | Analyze website text for scam/phishing |
| `POST` | `/api/v1/analyze-qr` | Analyze URL from QR code for phishing indicators |

### POST /api/v1/redact

```json
// Request
{ "text": "My name is John Doe and my email is john@example.com" }

// Response
{ "redacted_text": "My name is <PERSON> and my email is <EMAIL_ADDRESS>" }
```

### POST /api/v1/analyze

```json
// Request
{ "text": "<webpage text to analyze>" }

// Response
{
  "risk": "HIGH",
  "score": 85,
  "reason": "Page impersonates a bank login form.",
  "actions": ["Do not enter credentials", "Report to your bank"]
}
```

Risk levels: `LOW` | `MEDIUM` | `HIGH` | `CRITICAL` | `UNKNOWN`

### POST /api/v1/analyze-qr

```json
// Request
{ "url": "http://bit.ly/login-verify" }

// Response
{
  "risk": "HIGH",
  "score": 95,
  "url": "http://bit.ly/login-verify",
  "reason": "The link does not use HTTPS. The QR code uses a shortened link. The link contains suspicious authentication words."
}
```

## Requirements

- Python 3.9+
- [uv](https://github.com/astral-sh/uv)

## Environment variables

Copy `.env.example` to `.env` and set:

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Required for `/api/v1/analyze` |
| `DEBUG` | Enable debug logging (default: `False`) |
| `SECRET_KEY` | App secret |

## Setup & run

```sh
make install   # create venv and install dependencies
make run       # start dev server at http://localhost:8080
```

## Docker

```sh
make deploy    # docker-compose build + up -d
make down      # docker-compose down
```

## Docs

- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

## Tests

```sh
make test
```

## Project structure

```
app/
├── api/routes/       # FastAPI route handlers
├── core/             # Config, logging
├── models/           # Pydantic request/response models
├── services/         # Business logic
└── main.py           # App entrypoint
```
