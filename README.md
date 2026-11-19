# MeDeal — Hot Deal Black Friday 2026

Trang tổng hợp deal Black Friday 2026 (VPS, AI, Domain, Shopee, Alibaba, Lazada).
Site đang chạy: https://sandeal.microbit.io.vn (thử nghiệm nội bộ, chưa công khai đến 24/11).

## Dữ liệu

- `deals.json` — toàn bộ 90 deal đã thu thập, kèm mức xác minh `muc_xac_minh`
  (A = đã mở trang chính thức và thấy giá + hạn; B = nguồn phụ; C = chưa xác nhận)
  và `loai_deal` (BF2026 chính thức / Ưu đãi thường xuyên / Chương trình đang chạy).
- `deals-vps-domain.json`, `deals-ai.json`, `deals-ecommerce.json` — dữ liệu gốc theo nhóm.
- `site/deals.json` — 35 deal mức A đang hiển thị trên web (VPS 5, AI 8, Domain 13, Shopee 5, Lazada 4).

Quy tắc: chỉ deal mức A mới lên web. Deal hết hạn chỉ đổi trạng thái, không xóa.
Các cột affiliate (`chuong_trinh_affiliate`, `link_affiliate`, `hoa_hong_uoc_tinh`)
để trống — chỉ chủ dự án điền.

## Web tĩnh

- `site/` — `index.html`, `style.css`, `app.js`, `deals.json` + trang
  Chính sách Affiliate (`chinh-sach-affiliate.html`) và Liên hệ (`lien-he.html`).
- Nút "Xem deal" trỏ tới `/go/<deal_id>` — redirect 302 về link gốc (hoặc link
  affiliate khi đã điền), có log click nhưng không ghi IP.
- `deploy/Caddyfile` — cấu hình Caddy instance riêng, chỉ nghe 127.0.0.1:38080
  sau Cloudflare Tunnel; `gen_final_caddyfile.py` sinh file này từ `site/deals.json`.

## Cập nhật deal

1. Mở trang chính thức của nhà cung cấp, kiểm tra giá + hạn (không đoán).
2. Cập nhật `deals.json`, chạy `gen_final_caddyfile.py` nếu danh sách deal trên web đổi.
3. Deploy theo `DEPLOY-PLAN.md` (backup thư mục web trước, restart service, kiểm tra lại `/go/`).

Lịch kiểm tra: mỗi ngày 20–26/11, 2–3 giờ/lần vào 27/11 và 30/11.
