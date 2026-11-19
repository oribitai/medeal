# -*- coding: utf-8 -*-
"""Build the FINAL VPS Caddyfile for the Black Friday site (Task #7, Claude-approved).

- VPS paths: root /var/www/blackfriday, logs /var/log/caddy/blackfriday.
- Claude adjustments applied: auto_https off (global), site address http://127.0.0.1:38080,
  admin off, log filter (no IP / CF-* / User-Agent, keep Referer).
- 35 redir lines generated from site/deals.json (target = link_affiliate or link_goc).
Run: python3 gen_final_caddyfile.py > deploy/Caddyfile
"""
import json

SITE_DEALS = "/home/hatch/workspace/black-friday-deals/site/deals.json"

deals = json.load(open(SITE_DEALS, encoding="utf-8"))
assert len(deals) == 35, f"expected 35 deals, got {len(deals)}"

redir_lines = []
for d in sorted(deals, key=lambda x: x["deal_id"]):
    target = d.get("link_affiliate") or d["link_goc"]
    assert target, d["deal_id"]
    redir_lines.append(f"    redir /go/{d['deal_id']} {target} 302")

print("""{
    # Admin tat (tranh xung dot voi Caddy hien co tren :2019).
    admin off
    # Chi phuc vu HTTP sau tunnel — khong xin chung chi, khong chiem cong khac.
    auto_https off
    log {
        output file /var/log/caddy/blackfriday/caddy.log {
            roll_size 10MB
            roll_keep 7
        }
    }
}

# Chi nghe localhost:38080 (bind) va phuc vu ca 2 Host: ten mien cong khai (qua tunnel) + 127.0.0.1 (kiem tra truc tiep).
# LUU Y (bai hoc khi deploy): dia chi IP trong site address chi dung de khop Host, KHONG gioi han bind —
# Caddy van bind :38080 tren moi interface neu khong co `bind`. Bat buoc phai co `bind 127.0.0.1`.
# Neu khong co Host sandeal trong site address, request qua tunnel (Host: sandeal...) bi tra ve 200 rong.
http://sandeal.microbit.io.vn:38080, http://127.0.0.1:38080 {
    bind 127.0.0.1
    encode zstd gzip
    root * /var/www/blackfriday
    file_server

    # Khong cho Google index cho toi khi Claude duyet soft launch (24/11).
    header X-Robots-Tag "noindex"

    # Cache: HTML + deals.json cache ngan (~60s) de cap nhat deal hien nhanh.
    @static {
        path / /index.html /style.css /app.js /deals.json
    }
    header @static Cache-Control "public, max-age=60"

    # /go/* KHONG duoc cache — redirect phai di qua server de log click.
    @go {
        path /go/*
    }
    header @go Cache-Control "no-store"

    # Click log rieng cho site nay: chi ghi thoi gian, duong dan (/go/<deal_id>), referer.
    # Xoa toan bo nhom IP/header: remote_ip, client_ip, remote_port, CF-Connecting-IP, X-Forwarded-For, Cf-*, User-Agent.
    log {
        output file /var/log/caddy/blackfriday/access.log {
            roll_size 10MB
            roll_keep 7
        }
        format filter {
            wrap json
            fields {
                request>remote_ip delete
                request>client_ip delete
                request>remote_port delete
                request>headers>CF-Connecting-IP delete
                request>headers>X-Forwarded-For delete
                request>headers>Cf-Connecting-Ip delete
                request>headers>Cf-Ipcountry delete
                request>headers>Cf-Ray delete
                request>headers>Cf-Visitor delete
                request>headers>Cf-Warp-Tag-Id delete
                request>headers>User-Agent delete
            }
        }
    }

    # /go/<deal_id> -> 302 toi link affiliate (neu co) hoac link_goc.
    # Sinh tu dong tu deals.json (35 deal).""")
for line in redir_lines:
    print(line)
print("}")
