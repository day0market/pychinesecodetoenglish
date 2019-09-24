import time

import requests

with open('all_domains.txt', 'r') as f:
    raw_domains = f.read().splitlines()

selected = []
for r in raw_domains:
    try:
        resp = requests.get(f'https://translate.{r}/')
    except:
        continue
    time.sleep(1)
    if resp.status_code == 200:
        selected.append(f'translate.{r}')

with open('domains.txt', 'w') as f:
    f.write('\n'.join(selected))
