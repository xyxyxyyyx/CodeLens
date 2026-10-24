import json
import os
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import google.auth
from google.auth.transport.requests import AuthorizedSession

ROOT = Path(__file__).resolve().parent
MODEL = 'gemma-4-26b-a4b-it-maas'
PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT', '')

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_POST(self):
        if self.path != '/api/explain':
            self.send_error(404)
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if length <= 0 or length > 30000:
                raise ValueError('Request is empty or too large.')
            data = json.loads(self.rfile.read(length))
            code = str(data.get('code', '')).strip()
            language = str(data.get('language', 'Unknown'))[:40]
            if not code:
                raise ValueError('Please paste code first.')
            if not PROJECT_ID:
                raise ValueError('Set GOOGLE_CLOUD_PROJECT first.')
            credentials, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
            session = AuthorizedSession(credentials)
            url = (f'https://aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/global/'
                   f'publishers/google/models/{MODEL}:generateContent')
            prompt = (f'Explain this {language} code to a beginner. Explain what it does, '
                      'key concepts, and one possible improvement. Do not execute the code. '
                      f'Be concise.\n\nCODE:\n{code[:12000]}')
            response = session.post(url, json={'contents': [{'role': 'user', 'parts': [{'text': prompt}]}]}, timeout=65)
            if not response.ok:
                raise ValueError(f'Vertex AI HTTP {response.status_code}: {response.text[:600]}')
            result = response.json()
            explanation = '\n'.join(part['text'] for candidate in result.get('candidates', [])
                                    for part in candidate.get('content', {}).get('parts', []) if 'text' in part)
            payload, status = {'explanation': explanation or 'The model returned no text.'}, 200
        except Exception as exc:
            payload, status = {'error': str(exc)}, 400
        body = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

if __name__ == '__main__':
    print('CodeLens at http://localhost:8000')
    ThreadingHTTPServer(('0.0.0.0', 8000), Handler).serve_forever()
