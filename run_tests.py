import requests

URL = 'http://localhost:8000'
AGENT_API_KEY = '099a9hll5MhuH1McBeYbiEBUG8xlGWHoXo0tiGW9o-Y'

with open('curl_output.txt', 'w', encoding='utf-8') as f:
    f.write('# 1. Liveness\n')
    r = requests.get(f'{URL}/health')
    ct = r.headers.get("Content-Type", "")
    f.write(f'HTTP/1.1 {r.status_code} {r.reason}\nContent-Type: {ct}\n\n{r.text}\n\n')

    f.write('# 2. Readiness\n')
    r = requests.get(f'{URL}/ready')
    ct = r.headers.get("Content-Type", "")
    f.write(f'HTTP/1.1 {r.status_code} {r.reason}\nContent-Type: {ct}\n\n{r.text}\n\n')

    f.write('# 3. Khong co API key\n')
    r = requests.post(f'{URL}/ask', json={'question': 'Hello'})
    ct = r.headers.get("Content-Type", "")
    f.write(f'HTTP/1.1 {r.status_code} {r.reason}\nContent-Type: {ct}\n\n{r.text}\n\n')

    f.write('# 4. Co API key\n')
    r = requests.post(f'{URL}/ask', json={'question': 'Deploy là gì?'}, headers={'X-API-Key': AGENT_API_KEY, 'X-User-Id': 'sv-test'})
    ct = r.headers.get("Content-Type", "")
    f.write(f'HTTP/1.1 {r.status_code} {r.reason}\nContent-Type: {ct}\n\n{r.text}\n\n')

    f.write('# 5. Rate limit\n')
    codes = []
    for _ in range(15):
        r = requests.post(f'{URL}/ask', json={'question': 'test'}, headers={'X-API-Key': AGENT_API_KEY, 'X-User-Id': 'sv-test'})
        codes.append(str(r.status_code))
    f.write(' '.join(codes) + '\n')
