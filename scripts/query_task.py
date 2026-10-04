#!/usr/bin/env python3
import sys, json, urllib.request
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request
tid = sys.argv[1]
req = urllib.request.Request("https://www.runninghub.cn/openapi/v2/query",
    data=json.dumps({"taskId": tid}).encode(),
    headers={"Content-Type": "application/json"}, method="POST")
add_surrogate_to_request(req, "custom.runninghub", allowed_hosts=["www.runninghub.cn"])
with urllib.request.urlopen(req, timeout=30) as r:
    q = json.loads(r.read().decode())
d = q.get("data") or q
print("status:", d.get("status"))
err = d.get("errorMessage") or d.get("failedReason") or ""
print("error:", str(err)[:2000])
