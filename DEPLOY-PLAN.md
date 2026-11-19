# Kế hoạch deploy web deal Black Friday — BẢN TUNNEL (Task #7, CLAUDE ĐÃ DUYỆT 19/11 ~16:22 +07, được chạy + 6 chỉnh sửa)

> Trạng thái: ĐÃ DUYỆT, được chạy. Điều kiện chặn đã gỡ (user xác nhận snapshot xong). Áp dụng đúng 6 chỉnh sửa của Claude trong lúc chạy (xem mục 2, 4, 5, 6).
> Nguyên tắc: KHÔNG đụng Caddyfile hiện có, KHÔNG đụng cloudflared/Docker/firewall/iptables; web chạy bằng một Caddy instance RIÊNG chỉ nghe trên 127.0.0.1:38080, tunnel Cloudflare lo phần domain/HTTPS công khai (sandeal.microbit.io.vn). Không dùng sslip.io nữa.
> Dừng và báo cáo ngay nếu: caddy validate lỗi, 38080 đã bị dùng, hoặc bất kỳ site cũ nào (emc-lab, orbitnote) trả khác trước deploy. Chụp trạng thái 2 site này TRƯỚC khi bắt đầu để so sánh.
> Báo cáo gửi Claude từ giờ chỉ tóm tắt, KHÔNG đưa IP, cổng, tên container hay đường dẫn nội bộ vào chat chia sẻ (ngoại trừ các thư mục của task này khi cần).

## 0. Điều kiện tiên quyết (user làm, Muse không làm thay)

| # | Việc | Ai làm | Trạng thái |
|---|------|--------|------------|
| 1 | Snapshot VPS trong Oracle Console (backup boot volume) — xác nhận rồi báo Muse | User | ✅ XONG (user xác nhận 19/11 ~16:19, Claude xác nhận "Snapshot đã xong nên điều kiện chặn đã gỡ") |
| 2 | Kiểm tra Oracle security list (ưu tiên cao nhất, ~5 phút): chỉ 22/80/443 mở ra internet; cổng database tuyệt đối không mở | User | ⏳ CHƯA XÁC NHẬN (Claude nhắc lại sau khi duyệt) |
| 3 | Kiểm tra Cloudflare cho hostname sandeal: không bật Access hay rule chặn; không có cache rule ép cache /go/* | User | ⏳ (Claude nhắc: test thật bằng cách mở một link /go/ hai lần liên tiếp rồi xem log có ghi 2 lượt) |
| 4 | Nộp đơn affiliate (Namecheap, DigitalOcean, Contabo, Vietnix, TinoHost, Shopee, AliExpress, GoDaddy) | User | ⏳ (mô tả cho chương trình là "trang tổng hợp deal đang trong giai đoạn thử nghiệm" vì trang đang noindex) |

## 1. Kiến trúc (tunnel)

- Domain công khai: sandeal.microbit.io.vn (Cloudflare Tunnel → 127.0.0.1:38080 trên VPS). Tunnel đã chạy, hiện trả 502 vì chưa có service trên 38080.
- Caddy instance RIÊNG (không phải Caddy đang chạy): chỉ nghe 127.0.0.1:38080, chạy dưới user không phải root, admin tắt hoặc dùng cổng admin khác (tránh xung đột với Caddy hiện có).
- Thư mục web: /var/www/blackfriday (không dùng /home/ubuntu — Caddy chạy dưới user riêng thường không đọc được trong home; không nới lỏng quyền /home/ubuntu).
- File trong thư mục (đã build sẵn trên máy Muse, ở ~/workspace/black-friday-deals/site/): index.html, style.css, app.js, deals.json (chỉ 26 deal đã duyệt, mức A).
- Config riêng của instance mới: /etc/caddy/blackfriday/ (thư mục riêng, không đụng /etc/caddy/Caddyfile).
- Log riêng: /var/log/caddy/blackfriday/ (access log + log filter, xem mục 3).
- Systemd service riêng: /etc/systemd/system/caddy-blackfriday.service (1 file, không đụng service Caddy hiện có).

## 2. Cấu hình Caddy instance riêng (file /etc/caddy/blackfriday/Caddyfile)

```caddy
{
    # Tắt admin mặc định (tránh xung đột với Caddy hiện có trên :2019).
    admin off
    # Chỉ phục vụ HTTP sau tunnel — không xin chứng chỉ, không chiếm cổng khác (chỉnh sửa #3 của Claude).
    auto_https off
    # Log chung của instance (đã có log riêng cho site ở dưới).
    log {
        output file /var/log/caddy/blackfriday/caddy.log {
            roll_size 10MB
            roll_keep 7
        }
    }
}

# Chỉ nghe localhost — không mở ra ngoài, tunnel sẽ forward vào đây.
http://127.0.0.1:38080 {
    encode zstd gzip
    root * /var/www/blackfriday
    file_server

    # Không cho Google index cho tới khi Claude duyệt soft launch (24/11).
    header X-Robots-Tag "noindex"

    # Cache: HTML + deals.json cache ngắn (~60s) để cập nhật deal hiện nhanh.
    @static {
        path / /index.html /style.css /app.js /deals.json
    }
    header @static Cache-Control "public, max-age=60"

    # /go/* KHÔNG được cache — redirect phải đi qua server để log click.
    @go {
        path /go/*
    }
    header @go Cache-Control "no-store"

    # Click log riêng cho site này: chỉ ghi thời gian, đường dẫn (/go/<deal_id>), referer.
    # Xóa toàn bộ nhóm IP/header: remote_ip, client_ip, remote_port, CF-Connecting-IP, X-Forwarded-For, Cf-*, User-Agent.
    # (Đã kiểm chứng trên máy test: dòng log mẫu không còn remote_ip/client_ip/CF-*/User-Agent; Referer được giữ khi client gửi.)
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

    # /go/<deal_id> -> 302 tới link affiliate (nếu có) hoặc link_goc.
    # 26 dòng redir dưới đây được SINH TỰ ĐỘNG từ deals.json (xem mục 3).
    # Ví dụ (giá trị thật sinh ra lúc deploy):
    # redir /go/porkbun-bf26-xyz-91off https://porkbun.com/event/blackfriday 302
    # ... (25 dòng còn lại)
}
```

> Lưu ý: cú pháp `format filter` sẽ được kiểm tra bằng `caddy validate` trước khi start service. Nếu Caddy báo lỗi cú pháp, sửa filter cho tới khi validate pass — không start service khi validate chưa pass. Sau khi deploy, kiểm tra một dòng log mẫu thật và báo cáo là đã sạch IP. Với admin off, `caddy validate` vẫn dùng được, nhưng KHÔNG dùng `caddy reload` cho instance này — đổi config thì restart service (chỉnh sửa #3 của Claude).
>
> File Caddy cuối đã sinh sẵn trên máy Muse: `~/workspace/black-friday-deals/deploy/Caddyfile` (sinh bằng `gen_final_caddyfile.py` từ `site/deals.json`, 26 dòng redir, có `auto_https off`).

## 3. Sinh redirect /go/<deal_id> từ deals.json (tự động, không gõ tay)

- Script ~/workspace/black-friday-deals/gen_caddy_redirects.py (đã có, chạy trên máy Muse) đọc site/deals.json (26 deal) và sinh 26 dòng `redir`:
  - Nếu `link_affiliate` khác rỗng → target = `link_affiliate`.
  - Nếu `link_affiliate` rỗng → target = `link_goc`.
  - (Hiện tại tất cả `link_affiliate` đều rỗng → tất cả /go/ trỏ về `link_goc`.)
- Script ghi các dòng `redir` vào file Caddy riêng (mục 2) trước khi upload.
- Khi user điền `link_affiliate` sau này: cập nhật deals.json → chạy lại script → upload lại file Caddy → `caddy validate` → reload service riêng. Không sửa tay từng dòng.
- Kiểm tra sau deploy: `curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" https://sandeal.microbit.io.vn/go/<deal_id>` cho từng deal — phải trả 302 về đúng target.

## 4. Lệnh deploy dự kiến (chạy trên VPS qua SSH, sau khi Claude duyệt + user xác nhận snapshot)

```bash
# 0. Kiểm tra cổng 38080 còn trống và tunnel đang chạy (chỉ đọc)
ss -tlnp | grep ":38080" && echo "38080 DANG DUNG - DUNG LAI" || echo "38080 trong"
systemctl is-active cloudflared
# 0b. Kiểm tra user caddy (chỉnh sửa #1 của Claude): Caddy hiện có có thể đang chạy bằng user caddy.
# Dùng chung user là chấp nhận được, nhưng service mới phải có config và log riêng,
# và không được đọc hay ghi vào thư mục dữ liệu của Caddy cũ.
# NẾU user caddy KHÔNG tồn tại -> DỪNG LẠI, báo user trước khi fallback sang ubuntu (ubuntu có quyền rộng hơn).
id caddy && systemctl cat caddy 2>/dev/null | grep -E "^(User|Group)=" ; ps aux | grep -E "[c]addy run" | head -3
# 0c. Chụp trạng thái 2 site cũ TRƯỚC deploy để so sánh sau (theo yêu cầu của Claude):
curl -s -o /dev/null -w "emc-lab truoc: %{http_code}\n" https://emc-lab.microbit.io.vn/
curl -s -o /dev/null -w "orbitnote truoc: %{http_code}\n" https://orbitnote.microbit.io.vn/

# 1. Tạo thư mục web + config + log + dữ liệu riêng của instance mới (user ubuntu, sudo chỉ cho mkdir/chown)
sudo mkdir -p /var/www/blackfriday /etc/caddy/blackfriday /var/log/caddy/blackfriday /var/lib/caddy-blackfriday /var/lib/caddy-blackfriday-config
sudo chown -R ubuntu:ubuntu /var/www/blackfriday
sudo chown -R caddy:caddy /etc/caddy/blackfriday /var/log/caddy/blackfriday /var/lib/caddy-blackfriday /var/lib/caddy-blackfriday-config

# 2. Upload file site (từ máy Muse, tar pipe, md5 verify) vào /var/www/blackfriday/
#    (lệnh upload chạy từ máy Muse, không chạy trên VPS)
#    Backup bản cũ nếu đã có: cp -a /var/www/blackfriday /var/www/blackfriday.bak-<thời gian>

# 3. Upload file Caddy riêng (đã sinh redirect, mục 2+3) vào /etc/caddy/blackfriday/Caddyfile

# 4. Tạo systemd service riêng cho instance mới (hardening theo chỉnh sửa #2 của Claude:
#    NoNewPrivileges, ProtectSystem=strict, ProtectHome, PrivateTmp, ReadWritePaths chỉ thư mục
#    log + dữ liệu của instance mới; XDG_DATA_HOME/XDG_CONFIG_HOME riêng, không dùng chung
#    thư mục autosave/chứng chỉ với Caddy hiện có. KHÔNG có ExecReload — đổi config thì restart service.)
sudo tee /etc/systemd/system/caddy-blackfriday.service > /dev/null <<'EOF'
[Unit]
Description=Caddy for Black Friday deals site (127.0.0.1:38080 only)
After=network.target

[Service]
User=caddy
Group=caddy
Environment=XDG_DATA_HOME=/var/lib/caddy-blackfriday
Environment=XDG_CONFIG_HOME=/var/lib/caddy-blackfriday-config
ExecStart=/usr/bin/caddy run --environ --config /etc/caddy/blackfriday/Caddyfile
Restart=on-failure
RestartSec=5s
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
ReadWritePaths=/var/log/caddy/blackfriday /var/lib/caddy-blackfriday /var/lib/caddy-blackfriday-config

[Install]
WantedBy=multi-user.target
EOF

# 5. Validate config rồi mới start (KHÔNG start khi validate chưa pass)
sudo caddy validate --config /etc/caddy/blackfriday/Caddyfile
sudo systemctl daemon-reload
sudo systemctl enable --now caddy-blackfriday

# 6. Thêm cron backup deals.json hằng ngày (user ubuntu, crontab -e; chạy bằng user không phải root,
#    ghi vào thư mục riêng; kiểm tra thực tế một lần restore thử trước khi báo xong — chỉnh sửa #6 của Claude)
# 0 3 * * * cp /var/www/blackfriday/deals.json /var/www/blackfriday/deals-backup/deals-$(date +\%Y\%m\%d).json && find /var/www/blackfriday/deals-backup -name 'deals-*.json' -mtime +7 -delete
```

> Lưu ý user chạy service: nếu user `caddy` không tồn tại trên VPS, dùng user `ubuntu` (không phải root) trong file service. Kiểm tra trước khi tạo service.

## 5. Kiểm tra sau deploy (phải đạt hết mới coi là xong)

- `curl -s -o /dev/null -w "%{http_code}\n" https://sandeal.microbit.io.vn/` → 200.
- Trang hiển thị đủ 26 deal (21 deal Black Friday + 5 deal "Ưu đãi quanh năm"), lọc theo hạng mục hoạt động, đếm ngược chạy, mục Shopee/Lazada/Alibaba có ghi chú "Đang cập nhật, voucher sẽ được kiểm tra trong app ngày 24-25/11".
- Mỗi `/go/<deal_id>` → 302 về đúng target (link_goc hiện tại); header `Cache-Control: no-store` trên /go/*; header `Cache-Control: public, max-age=60` trên HTML/deals.json; header `X-Robots-Tag: noindex` còn hiện.
- Click log: `tail /var/log/caddy/blackfriday/access.log` — một dòng log mẫu KHÔNG chứa IP hay header CF-* (chỉ thời gian, đường dẫn, referer). Báo cáo dòng mẫu đã sạch.
- Kiểm tra trên điện thoại (mobile): trang load tốt, nút bấm được.
- 2 site cũ vẫn chạy: emc-lab và orbitnote trả về như trước (không thay đổi) — kiểm tra sau deploy.
- Caddy hiện có không bị ảnh hưởng (không reload/restart service Caddy cũ).

## 6. Backup + log rotation

- Backup deals.json hằng ngày bằng cron (mục 4 bước 6), giữ 7 ngày, thư mục /var/www/blackfriday/deals-backup/.
- Log rotation: Caddy tự roll log khi đạt 10MB, giữ 7 bản (cấu hình trong file Caddy, mục 2).

## 7. Rollback (khi deploy lỗi hoặc cần gỡ)

- **Gỡ site deal:** `sudo systemctl stop caddy-blackfriday && sudo systemctl disable caddy-blackfriday && sudo rm -rf /var/www/blackfriday /etc/caddy/blackfriday /etc/systemd/system/caddy-blackfriday.service && sudo systemctl daemon-reload` — tunnel sẽ trả về 502 như hiện tại.
- **Rollback nội dung web:** khôi phục thư mục backup /var/www/blackfriday.bak-<thời gian> (không cần restart service vì chỉ đổi file tĩnh).
- **Rollback khi Caddy validate lỗi:** không start service; sửa file Caddy rồi validate lại cho tới khi pass.
- Caddy hiện có, cloudflared, Docker và firewall không bị ảnh hưởng trong mọi trường hợp rollback (không đụng tới chúng).

## 8. Những việc KHÔNG làm trong đợt deploy này

- Không sửa /etc/caddy/Caddyfile (file Caddy hiện có), không đụng cloudflared, Docker, firewall/iptables.
- Không mở thêm cổng nào ra internet (site chỉ nghe 127.0.0.1:38080, tunnel lo phần công khai).
- Không điền `link_affiliate` (user tự điền sau khi duyệt đơn affiliate).
- Không đưa deal mức B/C lên web (chỉ 26 deal mức A đã duyệt).
- Không gỡ `X-Robots-Tag: noindex` cho tới khi Claude duyệt soft launch (24/11).
