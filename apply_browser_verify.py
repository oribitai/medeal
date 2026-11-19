# -*- coding: utf-8 -*-
"""Task #4 — Apply normal-browser verification results (19/11/2026 ~15:15 +07)
to the 5 AI providers re-checked in a rendered browser.
Run: python3 apply_browser_verify.py
"""
import json
from collections import Counter

PATH = "/home/hatch/workspace/black-friday-deals/deals.json"
CHECK_TIME = "19/11/2026 15:15 +07"

UPDATES = {
    "elevenlabs-bf26-creator-55off": {
        "muc_xac_minh": "A",
        "bat_dau_het_han": "Đến 01/12/2026 (23:59 ET; ngày bắt đầu không ghi trên trang)",
        "nguon_xac_minh": "Trình duyệt thường 19/11/2026: trang pricing chính thức hiển thị Creator $8.25/tháng năm đầu, FAQ xác nhận 'Creator annual costs $99 for the year', sale 'Ends December 1', gia hạn 'Then $18.33/mo' (tương đương $220/năm).",
        "ngay_gio_kiem_tra": CHECK_TIME,
    },
    "elevenlabs-bf26-pro-55off": {
        "muc_xac_minh": "A",
        "gia_goc": "$82.50/tháng (gói annual, tương đương $825/năm)",
        "gia_deal": "$45/tháng năm đầu (gói annual, tương đương $450/năm)",
        "phan_tram_giam": 45,
        "gia_gia_han": "$82.50/tháng (tương đương $825/năm gói annual)",
        "bat_dau_het_han": "Đến 01/12/2026 (23:59 ET; ngày bắt đầu không ghi trên trang)",
        "nguon_xac_minh": "Trình duyệt thường 19/11/2026: trang pricing chính thức hiển thị Pro $45/tháng năm đầu, sau đó $82.50/tháng. Giá $445.50/năm theo nguồn thứ cấp là SAI (tính theo gói monthly x12); giá đúng theo gói annual là $450/năm.",
        "ngay_gio_kiem_tra": CHECK_TIME,
    },
    "higgsfield-bf26-plus-45off": {
        "muc_xac_minh": "A",
        "gia_goc": "$49/tháng (năm)",
        "gia_deal": "$27/tháng (năm)",
        "gia_gia_han": "$49/tháng (năm)",
        "bat_dau_het_han": "Đến ~20/11/2026 (đồng hồ đếm ngược trên trang chính thức, ~00:00 UTC 20/11; ngày 15/12/2026 theo nguồn thứ cấp là SAI)",
        "nguon_xac_minh": "Trình duyệt thường 19/11/2026: trang pricing chính thức hiển thị Plus $27/tháng (was $49, 45% OFF, SAVE $264), countdown 'Offer ends in 0d 15h 46m'. Giá $33/tháng (was $59) theo nguồn thứ cấp 17–18/11 là SAI so với trang live.",
        "ngay_gio_kiem_tra": CHECK_TIME,
    },
    "higgsfield-bf26-ultra-60off": {
        "muc_xac_minh": "A",
        "bat_dau_het_han": "Đến ~20/11/2026 (đồng hồ đếm ngược trên trang chính thức, ~00:00 UTC 20/11; ngày 15/12/2026 theo nguồn thứ cấp là SAI)",
        "nguon_xac_minh": "Trình duyệt thường 19/11/2026: trang pricing chính thức hiển thị Ultra $50/tháng (was $129, 60% OFF, SAVE $948), countdown 'Offer ends in 0d 15h 46m'. Khớp với dữ liệu đã ghi.",
        "ngay_gio_kiem_tra": CHECK_TIME,
    },
    "adobe-bf26-firefly-pro-50off": {
        "muc_xac_minh": "A",
        "gia_deal": "$9.98/tháng (6 tháng đầu, gói monthly; $8.48/tháng nếu trả theo năm)",
        "gia_gia_han": "$19.99/tháng (gói monthly) / $16.99/tháng (trả theo năm)",
        "bat_dau_het_han": "10/11/2026 – 06/12/2026",
        "nguon_xac_minh": "Trình duyệt thường 19/11/2026: trang plans chính thức hiển thị 'Save 50% for the first 6 months. Regularly at US$19.99/mo. Alternatively at US$9.98/mo. Ends Dec 6.' + điều khoản chính thức (offer-terms) xác nhận $8.48/tháng (annual) hoặc $9.98/tháng (monthly) 6 tháng đầu, sau đó $16.99/$19.99/tháng.",
        "ngay_gio_kiem_tra": CHECK_TIME,
    },
    "adobe-bf26-firefly-proplus-60off": {
        "muc_xac_minh": "A",
        "gia_deal": "$19.98/tháng (6 tháng đầu, gói monthly; $16.78/tháng nếu trả theo năm)",
        "gia_gia_han": "$49.99/tháng (gói monthly) / $41.99/tháng (trả theo năm)",
        "bat_dau_het_han": "10/11/2026 – 06/12/2026",
        "nguon_xac_minh": "Trình duyệt thường 19/11/2026: điều khoản chính thức Adobe (offer-terms) xác nhận Pro Plus $16.78/tháng (annual) hoặc $19.98/tháng (monthly) 6 tháng đầu, sau đó $41.99/$49.99/tháng. Khớp với dữ liệu đã ghi (chênh $0.01 do làm tròn).",
        "ngay_gio_kiem_tra": CHECK_TIME,
    },
    "prowritingaid-bf26-premium-yearly-50off": {
        "muc_xac_minh": "A",
        "gia_goc": "$120/năm",
        "gia_deal": "$60/năm",
        "gia_gia_han": "$120/năm",
        "bat_dau_het_han": "Đến 29/11/2026 23:59 PT (ngày bắt đầu không ghi trên trang)",
        "dieu_kien": "Gói yearly (không áp dụng monthly); khách mới; Premium Pro yearly cũng 50% off ($144→$72/năm); +25% Story Credits",
        "nguon_xac_minh": "Trình duyệt thường 19/11/2026: trang pricing chính thức hiển thị Premium 50% OFF, gốc $10.00/tháng, giảm còn $5.00/tháng, 'billed yearly $60'; 'Black Friday Sale Ends Soon — Get the discount before Sun 29 Nov 23:59 PT'. Giá $79/năm và hạn 01/12 theo nguồn thứ cấp là SAI.",
        "ngay_gio_kiem_tra": CHECK_TIME,
    },
    "prowritingaid-bf26-premiumpro-lifetime-50off": {
        "muc_xac_minh": "A",
        "bat_dau_het_han": "Đến 29/11/2026 23:59 PT (ngày bắt đầu không ghi trên trang)",
        "nguon_xac_minh": "Trình duyệt thường 19/11/2026: trang pricing chính thức hiển thị Premium Pro lifetime 50% off: $349.50 (was $699), trả một lần. Khớp với dữ liệu đã ghi. Sale kết thúc 29/11/2026 23:59 PT (không phải 01/12).",
        "ngay_gio_kiem_tra": CHECK_TIME,
    },
    "grammarly-bf26-pro-50off": {
        "ghi_chu_tuan_thu": "Trình duyệt thường 19/11/2026 xác nhận giảm 50% trên trang BF chính thức, nhưng KHÔNG thấy giá $72/năm hay ngày kết thúc trên trang (giá chỉ hiện sau khi bấm 'Claim offer'). Giữ mức B cho đến khi xác nhận được giá + hạn.",
        "nguon_xac_minh": "Trang Black Friday chính thức Grammarly (đã mở 19/11/2026, text fetch + trình duyệt thường): giảm 50% hiển thị, nhưng không có giá $ hay ngày kết thúc trên trang; giá $72/năm theo nguồn thứ cấp.",
        "ngay_gio_kiem_tra": CHECK_TIME,
    },
}

with open(PATH, encoding="utf-8") as f:
    deals = json.load(f)

assert len(deals) == 71
for d in deals:
    if d["deal_id"] in UPDATES:
        d.update(UPDATES[d["deal_id"]])

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(deals, f, ensure_ascii=False, indent=1)
    f.write("\n")

print("OK — browser verification applied to", len(UPDATES), "deals")
print("By level (muc_xac_minh):", dict(Counter(d["muc_xac_minh"] for d in deals)))
print("By level x category:")
for cat in ("VPS", "AI", "Domain", "Shopee", "Alibaba", "Lazada"):
    sub = [d for d in deals if d["hang_muc"] == cat]
    print(" ", cat, dict(Counter(d["muc_xac_minh"] for d in sub)))
web = [d for d in deals if d["muc_xac_minh"] == "A" and d["trang_thai"] in ("Đang chạy", "Sắp diễn ra")]
print("Web-publishable active (A + not Nghi ngờ/Hết hạn):", len(web), dict(Counter(d["hang_muc"] for d in web)))
# Level-A Top 5 candidates (hot score desc, then discount desc)
cands = [d for d in web if d.get("gia_gia_han") and d["gia_gia_han"] != "chưa xác nhận"]
def pct(d):
    v = d.get("phan_tram_giam")
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, str) and v.rstrip("%").replace(".", "", 1).isdigit():
        return float(v.rstrip("%"))
    return 0
cands.sort(key=lambda d: (d["diem_hot"], pct(d)), reverse=True)
print("Top 5 level-A (with renewal price):")
for d in cands[:5]:
    print("  -", d["deal_id"], "| hot", d["diem_hot"], "| -" + str(d["phan_tram_giam"]), "|", d["gia_deal"], "| renewal:", d["gia_gia_han"])
