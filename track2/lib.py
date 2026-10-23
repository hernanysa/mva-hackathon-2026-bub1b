"""utilidades compartidas: HTTP con reintentos y rate-limit suave. Solo stdlib."""
import json, time, urllib.request, urllib.parse, urllib.error, sys, gzip

UA = "mva-hackathon-track2/1.0 (research; contact via github.com/hernanysa)"
_last = {"t": 0.0}

def _throttle(min_gap):
    dt = time.time() - _last["t"]
    if dt < min_gap:
        time.sleep(min_gap - dt)
    _last["t"] = time.time()

def get(url, headers=None, min_gap=0.34, timeout=30, tries=4, raw=False):
    h = {"User-Agent": UA, "Accept": "application/json"}
    if headers: h.update(headers)
    for i in range(tries):
        _throttle(min_gap)
        try:
            req = urllib.request.Request(url, headers=h)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                data = gzip.decompress(data)
            return data if raw else json.loads(data)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(2 + 3 * i); continue
            eprint(f"  HTTP {e.code} {url[:90]}")
            return None
        except Exception as ex:
            eprint(f"  retry ({ex}) {url[:80]}"); time.sleep(2 + 2 * i)
    return None

def post_json(url, payload, min_gap=0.5, timeout=45, tries=4):
    for i in range(tries):
        _throttle(min_gap)
        try:
            req = urllib.request.Request(
                url, data=json.dumps(payload).encode(),
                headers={"User-Agent": UA, "Content-Type": "application/json", "Accept": "application/json"},
                method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(3 + 3 * i); continue
            eprint(f"  POST HTTP {e.code}: {e.read()[:200]}"); return None
        except Exception as ex:
            eprint(f"  POST retry ({ex})"); time.sleep(3)
    return None

def eprint(*a): print(*a, file=sys.stderr, flush=True)

def save(path, obj):
    with open(path, "w") as f:
        if isinstance(obj, str): f.write(obj)
        else: json.dump(obj, f, indent=1, ensure_ascii=False)
    eprint(f"  -> {path}")
