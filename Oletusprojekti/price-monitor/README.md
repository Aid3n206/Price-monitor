# Price monitor (AI-powered)

Daily public-price monitor for resellers. Fetches public product pages, extracts fields with an LLM, saves CSV + emits alerts.

## Setup (Windows)
```powershell
cd C:\Users\YOURNAME\... \price-monitor
py -m pip install -r requirements.txt
copy .env.example .env
# edit .env and add GROQ_API_KEY (optional; mock mode otherwise)
```

## Run
```powershell
py -m src.pipeline
```

## Dry run / no AI keys
```powershell
$env:USE_MOCK_EXTRACTOR="1"
py -m src.pipeline
```