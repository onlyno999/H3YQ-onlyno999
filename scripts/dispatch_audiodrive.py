#!/usr/bin/env python3
"""H3YQ-onlyno999 音频驱动派发器 — workflow 2101416149702504449（2026-10-04 用户拍板替换旧 2106642 线）.

Graph-pinned mapping (from executed-graph metadata + two paid tests, see
references/workflow_2101416_map.md):
  prompt   -> node 79  field "prompt"  (CR Prompt Text -> node76.prompt; the ONLY real prompt slot)
  duration -> node 73  field "value"   (PrimitiveFloat seconds -> frame-count formula)
  aspect   -> node 78  field "aspect_ratio"
  seed     -> node 62  field "noise_seed"
  image 1  -> node 72  field "image"   (-> node76 ref_image_0)
  image 2  -> node 101 field "image"   (-> node76 ref_image_1; omit for single-person)
  drive    -> node 74  field "audio"   (-> node76 drive_audio; TRUE drive input)

NEVER send node 84 (VHS_VideoCombine): its audio input must stay at the author's
default wiring, otherwise the output mp4 loses its audio track (test 1 proved it).
NEVER send nodes 123/124/125: they belong to an unrelated anima image side-branch.

Output: mp4 WITH an AAC audio track (drive audio remixed in, corr ~0.998 vs source).
Results order is unstable (a zip may come first) — always pick outputType == "mp4".
Credentials: environment-injected only (dynamic_credentials surrogate); no keys in code.
"""
import sys, os, json, time, argparse, urllib.request, urllib.error
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request

BASE = "https://www.runninghub.cn"
WF = "2101416149702504449"
ap = argparse.ArgumentParser()
ap.add_argument("--duration", type=float, required=True, help="seconds, must equal drive audio length")
ap.add_argument("--seed", type=int, default=20261004)
ap.add_argument("--aspect", default="9:16 (Portrait Widescreen)")
ap.add_argument("--ref0", required=True)
ap.add_argument("--ref1", default="")
ap.add_argument("--audio", required=True, help="drive audio: source original, zero processing")
ap.add_argument("--prompt-file", required=True, help="Ref2VA six-section prompt text (goes to node 79 'prompt')")
ap.add_argument("--out", required=True)
ap.add_argument("--taskfile", required=True)
ap.add_argument("--dump", required=True)
ap.add_argument("--max-poll", type=int, default=1800)
a = ap.parse_args()

def post_json(path, payload, timeout=30):
    req = urllib.request.Request(BASE + path, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "h3yq-dispatch/2.0"}, method="POST")
    add_surrogate_to_request(req, "custom.runninghub", allowed_hosts=["www.runninghub.cn"])
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        try: return json.loads(body)
        except Exception: return {"_http": e.code, "_body": body[:500]}

def upload_media(path):
    boundary = "----MUSEBOUNDARY1234"
    with open(os.path.expanduser(path), "rb") as f: data = f.read()
    name = os.path.basename(path)
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{name}\"\r\n"
            f"Content-Type: application/octet-stream\r\n\r\n").encode() + data + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(BASE + "/openapi/v2/media/upload/binary", data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}",
                 "User-Agent": "h3yq-dispatch/2.0"}, method="POST")
    add_surrogate_to_request(req, "custom.runninghub", allowed_hosts=["www.runninghub.cn"])
    with urllib.request.urlopen(req, timeout=180) as resp:
        r = json.loads(resp.read().decode("utf-8"))
    fn = (r.get("data") or {}).get("fileName")
    if not fn:
        print("UPLOAD FAILED:", json.dumps(r, ensure_ascii=False)[:300]); sys.exit(11)
    return fn

prompt_text = open(os.path.expanduser(a.prompt_file), encoding="utf-8").read()
nodes = [
    {"nodeId": "62", "fieldName": "noise_seed", "fieldValue": a.seed},
    {"nodeId": "73", "fieldName": "value", "fieldValue": a.duration},
    {"nodeId": "78", "fieldName": "aspect_ratio", "fieldValue": a.aspect},
    {"nodeId": "79", "fieldName": "prompt", "fieldValue": prompt_text},
]
uploaded = {}
for path, node, field in [(a.ref0, "72", "image"), (a.ref1, "101", "image"), (a.audio, "74", "audio")]:
    if path:
        fn = upload_media(path)
        uploaded[node] = fn
        print(f"uploaded node {node} ({field}): {path} -> {fn}", flush=True)
        nodes.append({"nodeId": node, "fieldName": field, "fieldValue": fn})

payload = {"workflowId": WF, "nodeInfoList": nodes, "instanceType": "default", "usePersonalQueue": False}
dump = {"uploaded": uploaded, "mapping": "2101416149702504449 graph-pinned 2026-10-04 (79.prompt/73/78/62/72/101/74; 84 untouched)"}
tid = None
for ep in ["/task/openapi/create", f"/openapi/v2/run/workflow/{WF}"]:
    r = post_json(ep, payload)
    dump[f"create@{ep}"] = r
    tid = r.get("taskId") or (r.get("data") or {}).get("taskId")
    print(f"create via {ep}: errorCode={r.get('errorCode')} code={r.get('code')} taskId={tid}", flush=True)
    if tid: break
if not tid:
    json.dump(dump, open(a.dump, "w"), ensure_ascii=False, indent=1)
    print("DISPATCH FAILED (no taskId)"); sys.exit(10)
open(a.taskfile, "w").write(tid)
print("taskId:", tid, flush=True)

start = time.time(); final = None
while time.time() - start < a.max_poll:
    time.sleep(20)
    q = post_json("/openapi/v2/query", {"taskId": tid}, timeout=25)
    st = q.get("status")
    print(f"[{int(time.time()-start)}s] status={st}", flush=True)
    if st == "SUCCESS":
        res = q.get("results") or []
        dump["final_query"] = q
        mp4 = next((r for r in res if isinstance(r, dict) and r.get("outputType") == "mp4"), None)
        print("results:", json.dumps(res, ensure_ascii=False)[:400], flush=True)
        if mp4 and mp4.get("url"):
            urllib.request.urlretrieve(mp4["url"], a.out)
            print("saved:", a.out, flush=True)
        else:
            print("NO MP4 RESULT FOUND"); sys.exit(14)
        final = q; break
    if st in ("FAILED", "CANCELLED"):
        dump["final_query"] = q
        json.dump(dump, open(a.dump, "w"), ensure_ascii=False, indent=1)
        print("TASK FAILED:", json.dumps(q.get("failedReason") or q, ensure_ascii=False)[:800], flush=True)
        sys.exit(12)
json.dump(dump, open(a.dump, "w"), ensure_ascii=False, indent=1)
if not final:
    print("POLL TIMEOUT, taskId:", tid, flush=True); sys.exit(13)
print("DONE", tid)
