# Hot Deal Black Friday 2026 — Static Site

Trang deal tĩnh (không cần build, không có code phía server). Dữ liệu lấy từ
`deals.json` trong cùng thư mục, hiển thị bằng `app.js`.

## Files

- `index.html` — khung trang (tiếng Việt, mobile-friendly)
- `style.css` — giao diện, không phụ thuộc bên ngoài
- `app.js` — tải `deals.json`, lọc/sắp xếp, đếm ngược trực tiếp
- `deals.json` — chỉ 26 deal đã duyệt (mức xác minh A), xem danh sách bên dưới

## 26 deal được hiển thị

Chỉ deal có `muc_xac_minh == "A"` và `trang_thai` là "Đang chạy" hoặc
"Sắp diễn ra", trừ 4 deal Hostinger và Vietnix (hết hạn). Cộng thêm
`namecheap-bf26-co-87off` (mức A, trạng thái "Nghi ngờ") kèm cảnh báo.
Deal mức B/C, Hostinger, Vietnix và Lazada Techcombank "iPhone 18"
(đã loại khỏi dữ liệu công khai) KHÔNG hiển thị.

VPS (5):
- vultr-bf26-cloud-300credit
- hetzner-bf26-cloud-50credit
- namecheap-bf26-vps-pulsar-54off (Sắp diễn ra, bắt đầu 20/11 12:00 +07)
- namecheap-bf26-vps-quasar-41off (Sắp diễn ra)
- namecheap-bf26-vps-magnetar-40off (Sắp diễn ra)

Domain (13):
- namecheap-bf26-com-31off, namecheap-bf26-net-20off, namecheap-bf26-org-48off,
  namecheap-bf26-com-transfer-43off, namecheap-bf26-co-87off (kèm cảnh báo gia hạn)
- porkbun-bf26-xyz-91off, porkbun-bf26-bond-92off, porkbun-bf26-blog-90off,
  porkbun-bf26-shop-92off, porkbun-bf26-asia-91off
- pavietnam-bf26-com-95off, pavietnam-bf26-comvn-42off, pavietnam-bf26-xyz-92off

AI (8):
- adobe-bf26-firefly-pro-50off, adobe-bf26-firefly-proplus-60off
- elevenlabs-bf26-creator-55off, elevenlabs-bf26-pro-55off
- higgsfield-bf26-plus-45off, higgsfield-bf26-ultra-60off (sắp hết hạn ~20/11)
- prowritingaid-bf26-premium-yearly-50off,
  prowritingaid-bf26-premiumpro-lifetime-50off

Shopee / Alibaba / Lazada: 0 deal mức A — trang hiển thị ghi chú
"Đang cập nhật, voucher sẽ được kiểm tra trong app ngày 24–25/11".
Mục Alibaba đã tách sẵn hai nhóm "Alibaba.com (B2B)" và "AliExpress" để
dùng khi có deal được duyệt sau.

## Mục "Ưu đãi quanh năm" (tách riêng khỏi deal Black Friday)

5 deal có `loai_deal == "Ưu đãi thường xuyên"` không nằm trong danh sách
Black Friday chính mà hiển thị ở mục riêng "Ưu đãi quanh năm" cuối trang:
- vultr-bf26-cloud-300credit, hetzner-bf26-cloud-50credit
- pavietnam-bf26-com-95off, pavietnam-bf26-comvn-42off, pavietnam-bf26-xyz-92off

Thẻ trong mục này chỉ hiển thị nhãn "Ưu đãi thường xuyên", KHÔNG có sao
độ hot và KHÔNG có đếm ngược — hiển thị "Không rõ thời hạn". 5 deal này
vẫn tính vào số lượng của bộ lọc theo hạng mục (VPS/Domain).

## Countdown — ngày không parse được (không đoán)

`app.js` dùng bảng `COUNTDOWN` (ngày ISO ghi rõ theo deal_id) vì chuỗi ngày
gốc là văn bản tự do. 5 deal sau KHÔNG có ngày kết thúc xác định nên không
hiện đếm ngược:
- vultr-bf26-cloud-300credit (credit, "chưa xác nhận")
- hetzner-bf26-cloud-50credit ("chưa xác nhận ngày bắt đầu/kết thúc")
- pavietnam-bf26-com-95off, pavietnam-bf26-comvn-42off, pavietnam-bf26-xyz-92off
  (khuyến mãi thường trực, không ghi ngày kết thúc)

Lưu ý: ngày hết hạn của Adobe ("Ends Dec 6") không ghi múi giờ trên trang
nên lấy UTC; ngày hết hạn của Higgsfield (~20/11 00:00 UTC) là ước lượng từ
đồng hồ đếm ngược trên trang chính thức.

## Serve bằng Caddy (trên VPS)

Thư mục này chỉ chứa file tĩnh. Caddy phục vụ trực tiếp, ví dụ:

```
example.com {
    root * /var/www/black-friday-deals
    file_server
}
```

## Redirect /go/<deal_id> — do Caddy xử lý, KHÔNG phải file tĩnh

Nút "Xem deal" trên trang trỏ tới `/go/<deal_id>` (ví dụ
`/go/porkbun-bf26-xyz-91off`). Thuộc tính `rel` được tính động theo từng
deal trong `app.js`: `rel="sponsored nofollow"` chỉ khi deal có
`link_affiliate` khác rỗng, còn lại `rel="nofollow noopener"`. Hiện tại
cả 26 deal đều chưa có `link_affiliate` nên đều dùng "nofollow noopener";
khi user điền link affiliate sau, rel sẽ tự đổi thành "sponsored nofollow".
Caddy cần thêm quy tắc redirect 302 từ `/go/<deal_id>` sang link affiliate
(nếu có) hoặc `link_goc` trong `deals.json`, kèm ghi log click
(thời gian, deal_id, referrer). Ví dụ dùng `redir` trong Caddyfile cho từng
deal, hoặc một dịch vụ redirect nhỏ đọc `deals.json`. File tĩnh trong thư
mục này không tự xử lý được redirect.

## Cập nhật dữ liệu

Sửa `deals.json` trong thư mục này (giữ đúng schema, chỉ deal mức A được
hiển thị) rồi tải lại trang — không cần build lại. Nếu deal mới có ngày kết
thúc khác, bổ sung mục tương ứng vào bảng `COUNTDOWN` trong `app.js`.
