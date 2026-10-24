# CodeLens — Gemma 4 Code Explainer

A hackathon prototype to help beginners understand Python, Java, C++, and JavaScript code. Paste a snippet, select the language, and ask Gemma 4 for a concise explanation, key concepts, and one improvement idea.

## Stack
HTML, CSS, JavaScript, Python HTTP server, Google Cloud Vertex AI managed API, Gemma 4 26B A4B IT (`google/gemma-4-26b-a4b-it-maas`). Apache 2.0 applies to the model; the CodeLens application is MIT licensed.

## Run in Google Cloud Shell

Vertex AI API must be enabled in your project. Managed model inference may incur charges; check pricing and trial eligibility before using it.

```bash
python3 -m pip install -r requirements.txt
export GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
python3 server.py
```

In Cloud Shell, use **Web Preview → Preview on port 8000** to open the app. Cloud Shell normally provides application default credentials; if authentication fails, follow Google Cloud's Application Default Credentials setup instructions. On a local computer, install gcloud and run `gcloud auth application-default login` before starting the server.

## How it works
The frontend POSTs code to `/api/explain`. The Python backend authenticates with Google Cloud Application Default Credentials and sends the prompt to Gemma 4 on Vertex AI. The response is shown on the page. User code is never executed.

## Status and limitations
Prototype integration; a successful model request must be verified in your own Google Cloud project. Responses may be inaccurate. No authentication or rate limiting is provided; do not publicly deploy this demo without security improvements. Do not commit secrets or tokens.

## License
MIT — see LICENSE.
