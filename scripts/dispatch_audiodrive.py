#!/usr/bin/env python3
"""H3YQ-onlyno999 - audio-drive dispatcher (field-proven 2026-10-04).

Purpose: dispatch "drive audio (original sound) + character reference
image(s) + Ref2VA six-part prompt" to the RunningHub workflow
2106642679642812418 (H3 official-flow, single-sample express drama
version), so the characters perform / lip-sync driven by the ORIGINAL
audio. Drive audio must be extracted from the user's source video and
used unprocessed - never regenerated, never TTS (hard rule, 2026-09-29).

Node mapping (pinned by zero-charge census 2026-10-04, see
references/workflow_census.md):
  138.value        prompt
  132.value        duration in seconds (MUST equal drive audio length)
  115.aspect_ratio default "9:16 (Portrait Widescreen)"
  129.noise_seed   seed
  137.image        person 1 reference (speaker S1)
  139.image        person 2 reference (speaker S2, optional arg)
  148.audio        DRIVE AUDIO - the workflow's only audio input,
                   drive-type. Always fed in this skill (--audio).

Credentials: environment-injected only (dynamic_credentials surrogate
for custom.runninghub). No key material in this file.

Closing rule (empirical, SKILL.md section 6): the returned file has NO
audio track - the performance is driven, the sound is not muxed in.
Before delivery, re-attach the drive audio verbatim as the output
track and verify correlation ~= 1.

Usage:
  python3 dispatch_audiodrive.py --prompt-file prompt.txt \
      --duration 6.0 --ref0 person1.jpg --ref1 person2.png \
      --audio148 drive_audio.wav \
      --out raw.mp4 --taskfile taskid.txt --dump dump.json
(task 2106697779907878913, King of Comedy case, ran exactly this way.)
"""
import sys, os, json, time, argparse, urllib.request, urllib.error
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request

BASE = "https://www.runninghub.cn"
WF = "2106642679642812418"
ap = argparse.ArgumentParser()
ap.add_argument("--prompt-file", required=True)
ap.add_argument("--duration", type=float, required=True)
ap.add_argument("--seed", type=int, default=20261004)
ap.add_argument("--aspect", default="9:16 (Portrait Widescreen)")
ap.add_argument("--ref0", default=""); ap.add_argument("--ref1", default="")
ap.add_argument("--audio148", default="", help="drive audio file fed to node 148 field 'audio' (REQUIRED for H3YQ: the original sound extracted from the source video, unprocessed)")
ap.add_argument("--out", required=True)
ap.add_argument("--taskfile", required=True)
ap.add_argument("--dump", required=True)
ap.add_argument("--max-poll", type=int, default=1800)
a = ap.parse_args()

def post_json(path, payload, timeout=30):
    req = urllib.request.Request(BASE + path, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "h3yq-audiodrive-dispatch/1.0"}, method="POST")
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
                 "User-Agent": "h3yq-audiodrive-dispatch/1.0"}, method="POST")
    add_surrogate_to_request(req, "custom.runninghub", allowed_hosts=["www.runninghub.cn"])
    with urllib.request.urlopen(req, timeout=180) as resp:
        r = json.loads(resp.read().decode("utf-8"))
    fn = (r.get("data") or {}).get("fileName")
    if not fn:
        print("UPLOAD FAILED:", json.dumps(r, ensure_ascii=False)[:300]); sys.exit(11)
    return fn

prompt = open(os.path.expanduser(a.prompt_file), encoding="utf-8").read().strip()
nodes = [
    {"nodeId": "138", "fieldName": "value", "fieldValue": prompt},
    {"nodeId": "132", "fieldName": "value", "fieldValue": a.duration},
    {"nodeId": "115", "fieldName": "aspect_ratio", "fieldValue": a.aspect},
    {"nodeId": "129", "fieldName": "noise_seed", "fieldValue": a.seed},
]
uploaded = {}
for slot, node in [(a.ref0, "137"), (a.ref1, "139")]:
    if slot:
        fn = upload_media(slot)
        uploaded[node] = fn
        print(f"uploaded node {node}: {slot} -> {fn}", flush=True)
        nodes.append({"nodeId": node, "fieldName": "image", "fieldValue": fn})
if a.audio148:
    fn = upload_media(a.audio148)
    uploaded["148"] = fn
    print(f"uploaded node 148 (drive audio): {a.audio148} -> {fn}", flush=True)
    nodes.append({"nodeId": "148", "fieldName": "audio", "fieldValue": fn})

payload = {"workflowId": WF, "nodeInfoList": nodes,
           "instanceType": "default", "usePersonalQueue": False}
dump = {"uploaded": uploaded, "mapping": "138/132/115/129 + 137/139 + 148 drive audio (census 2026-10-04)"}
tid = None
for ep in ["/task/openapi/create", f"/openapi/v2/run/workflow/{WF}"]:
    r = post_json(ep, payload)
    dump[f"create@{ep}"] = r
    tid = r.get("taskId") or (r.get("data") or {}).get("taskId")
    print(f"create via {ep}: errorCode={r.get('errorCode')} code={r.get('code')} taskId={tid}", flush=True)
    if tid: break
if not tid:
    json.dump(dump, open(a.dump, "w"), ensure_ascii=False, indent=1)
    print("DISPATCH FAILED (no taskId on either endpoint)", flush=True)
    sys.exit(10)
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
        url = (res[0].get("url") if isinstance(res[0], dict) else res[0]) if res else None
        dump["final_query"] = q
        if url:
            urllib.request.urlretrieve(url, a.out)
            print("saved:", a.out, flush=True)
        final = q; break
    if st in ("FAILED", "CANCELLED"):
        dump["final_query"] = q
        json.dump(dump, open(a.dump, "w"), ensure_ascii=False, indent=1)
        print("TASK FAILED:", json.dumps(q.get("failedReason") or q, ensure_ascii=False)[:500], flush=True)
        sys.exit(12)
json.dump(dump, open(a.dump, "w"), ensure_ascii=False, indent=1)
if not final:
    print("POLL TIMEOUT, taskId:", tid, flush=True); sys.exit(13)
print("DONE", tid)
print("REMINDER: returned file has NO audio track - re-attach the drive audio verbatim before delivery (SKILL.md section 6).")
