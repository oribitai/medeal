# -*- coding: utf-8 -*-
"""Generate Caddy /go/<deal_id> redirect lines from site/deals.json.
Target = link_affiliate if set, else link_goc.
Run: python3 gen_caddy_redirects.py > blackfriday-redirects.caddy
"""
import json

PATH = "/home/hatch/workspace/black-friday-deals/site/deals.json"

deals = json.load(open(PATH, encoding="utf-8"))
assert len(deals) == 26, f"expected 26 deals, got {len(deals)}"

print("    # /go/<deal_id> redirects — generated from deals.json (26 deals).")
print("    # Target = link_affiliate if set, else link_goc.")
for d in sorted(deals, key=lambda x: x["deal_id"]):
    target = d.get("link_affiliate") or d["link_goc"]
    assert target, d["deal_id"]
    print(f"    redir /go/{d['deal_id']} {target} 302")
