# Publish Checklist

1. Verify local run:
   - `python -m uvicorn app:app --host 0.0.0.0 --port 8000`
2. Verify endpoints:
   - `GET /health`
   - `POST /shortcut`
3. Confirm shortcut URLs point to `:8000/shortcut`
4. Remove secrets:
   - no `.env`
   - no API keys
5. Add screenshots (optional) of `Assistant Start Core` and `Assistant Loop Core`
6. Commit and push to GitHub
