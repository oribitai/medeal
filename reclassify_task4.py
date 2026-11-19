# -*- coding: utf-8 -*-
"""Task #4 (lượt 2) — Re-classify all 71 deals in deals.json.
Adds loai_deal + muc_xac_minh per Claude's review of round 1, plus
renewal-price fills, hot-score corrections, and exclusion flags.
Run: python3 reclassify_task4.py
"""
import json
from collections import Counter

PATH = "/home/hatch/workspace/black-friday-deals/deals.json"

CLASS = {
    # VPS (16)
    "vultr-bf26-cloud-100match": {"loai_deal": "Ưu đãi thường xuyên", "muc_xac_minh": "B", "gia_gia_han": "Không áp dụng (credit dùng một lần)"},
    "vultr-bf26-cloud-300credit": {"loai_deal": "Ưu đãi thường xuyên", "muc_xac_minh": "A", "gia_gia_han": "Không áp dụng (credit dùng một lần)"},
    "digitalocean-bf26-droplet-200credit": {"loai_deal": "Ưu đãi thường xuyên", "muc_xac_minh": "B"},
    "hetzner-bf26-cloud-50credit": {"loai_deal": "Ưu đãi thường xuyên", "muc_xac_minh": "A", "gia_gia_han": "Không áp dụng (credit dùng một lần)"},
    "contabo-bf26-vps4-440eur": {"loai_deal": "Teaser", "muc_xac_minh": "B", "gia_gia_han": "€4.40/tháng (giá thường, không đổi)"},
    "contabo-bf26-vps6-600eur": {"loai_deal": "Teaser", "muc_xac_minh": "B", "gia_gia_han": "€6.00/tháng (giá thường, không đổi)"},
    "contabo-bf26-vps8-1120eur": {"loai_deal": "Teaser", "muc_xac_minh": "B", "gia_gia_han": "€11.20/tháng (giá thường, không đổi)"},
    "hostinger-bf26-vps-kvm1-67off": {"loai_deal": "Ưu đãi thường xuyên", "muc_xac_minh": "A", "diem_hot": 1, "ghi_chu_tuan_thu": "KHÔNG đưa lên web — giá $6.49/tháng bằng giá thường từ tháng 8/2026 (Findstack/VPSscouter), không phải giảm giá BF thật. Giữ trong dữ liệu với trạng thái Nghi ngờ."},
    "hostinger-bf26-vps-kvm2": {"loai_deal": "Ưu đãi thường xuyên", "muc_xac_minh": "A", "diem_hot": 1, "ghi_chu_tuan_thu": "KHÔNG đưa lên web — giá bằng giá thường, không phải giảm giá BF thật. Giữ trong dữ liệu với trạng thái Nghi ngờ."},
    "hostinger-bf26-vps-kvm4": {"loai_deal": "Ưu đãi thường xuyên", "muc_xac_minh": "A", "diem_hot": 1, "ghi_chu_tuan_thu": "KHÔNG đưa lên web — giá bằng giá thường, không phải giảm giá BF thật. Giữ trong dữ liệu với trạng thái Nghi ngờ."},
    "hostinger-bf26-vps-kvm8": {"loai_deal": "Ưu đãi thường xuyên", "muc_xac_minh": "A", "diem_hot": 1, "ghi_chu_tuan_thu": "KHÔNG đưa lên web — giá bằng giá thường, không phải giảm giá BF thật. Giữ trong dữ liệu với trạng thái Nghi ngờ."},
    "namecheap-bf26-vps-pulsar-54off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "A"},
    "namecheap-bf26-vps-quasar-41off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "A"},
    "namecheap-bf26-vps-magnetar-40off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "A"},
    "vietnix-bf26-vps-ssd4-40off": {"loai_deal": "Teaser", "muc_xac_minh": "A"},
    "tinohost-bf26-vps-20gb": {"loai_deal": "Teaser", "muc_xac_minh": "B", "gia_gia_han": "199.000đ/tháng (giá thường)"},
    # Domain (15)
    "namecheap-bf26-com-31off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "A"},
    "namecheap-bf26-net-20off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "A"},
    "namecheap-bf26-org-48off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "A"},
    "namecheap-bf26-co-87off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "A", "ghi_chu_tuan_thu": "CẢNH BÁO khi hiển thị trên web: gia hạn $45.48/năm, gấp 9,1 lần giá năm đầu. Không đưa vào Top."},
    "namecheap-bf26-com-transfer-43off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "A"},
    "porkbun-bf26-xyz-91off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "A"},
    "porkbun-bf26-bond-92off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "A"},
    "porkbun-bf26-blog-90off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "A"},
    "porkbun-bf26-shop-92off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "A"},
    "porkbun-bf26-asia-91off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "A"},
    "godaddy-bf26-com-99off": {"loai_deal": "Ưu đãi thường xuyên", "muc_xac_minh": "B", "ghi_chu_tuan_thu": "CẢNH BÁO khi hiển thị trên web: bắt buộc mua 3 năm, trả trước $45.99 + phí ICANN. Không đưa vào Top."},
    "namecom-bf26-com-36off": {"loai_deal": "Ưu đãi thường xuyên", "muc_xac_minh": "B"},
    "pavietnam-bf26-com-95off": {"loai_deal": "Ưu đãi thường xuyên", "muc_xac_minh": "A"},
    "pavietnam-bf26-comvn-42off": {"loai_deal": "Ưu đãi thường xuyên", "muc_xac_minh": "A"},
    "pavietnam-bf26-xyz-92off": {"loai_deal": "Ưu đãi thường xuyên", "muc_xac_minh": "A"},
    # AI (16)
    "grammarly-bf26-pro-50off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "B"},
    "pictory-bf26-starter-50off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "B", "gia_gia_han": "$25/tháng (năm) — giá thường sau năm đầu"},
    "pictory-bf26-professional-50off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "B", "gia_gia_han": "$35/tháng (năm) — giá thường sau năm đầu"},
    "pictory-bf26-teams-50off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "B", "gia_gia_han": "$119/tháng (năm) — giá thường sau năm đầu"},
    "adobe-bf26-firefly-pro-50off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "B"},
    "adobe-bf26-firefly-proplus-60off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "B"},
    "elevenlabs-bf26-creator-55off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "B"},
    "elevenlabs-bf26-pro-55off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "B"},
    "higgsfield-bf26-plus-45off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "B"},
    "higgsfield-bf26-ultra-60off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "B"},
    "mindpal-bf26-pro-60off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "B"},
    "mindpal-bf26-advanced-60off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "B"},
    "mindpal-bf26-ultra-60off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "B"},
    "decktopus-bf26-pro-66off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "B"},
    "prowritingaid-bf26-premium-yearly-50off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "B"},
    "prowritingaid-bf26-premiumpro-lifetime-50off": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "B"},
    # Shopee (8)
    "shopee-bf26-voucher-xtra-1trieu": {"loai_deal": "Teaser", "muc_xac_minh": "C"},
    "shopee-bf26-freeship-0d": {"loai_deal": "Teaser", "muc_xac_minh": "C"},
    "shopee-bf26-live-50pct": {"loai_deal": "Teaser", "muc_xac_minh": "C"},
    "shopee-bf26-compliment-116k": {"loai_deal": "Teaser", "muc_xac_minh": "B"},
    "shopee-bf26-carslan-259k": {"loai_deal": "Teaser", "muc_xac_minh": "B"},
    "shopee-bf26-renhouse-89k": {"loai_deal": "Teaser", "muc_xac_minh": "B", "diem_hot": 3},
    "shopee-bf26-tingoan-150k": {"loai_deal": "Teaser", "muc_xac_minh": "B"},
    "shopee-bf26-may-hut-am-2990k": {"loai_deal": "Teaser", "muc_xac_minh": "B"},
    # Lazada (8)
    "lazada-bf26-vib-1trieu": {"loai_deal": "Ưu đãi thường xuyên", "muc_xac_minh": "B"},
    "lazada-bf26-techcombank-1trieu": {"loai_deal": "Ưu đãi thường xuyên", "muc_xac_minh": "C", "ghi_chu_tuan_thu": "ĐÃ LOẠI KHỎI DỮ LIỆU CÔNG KHAI theo review lượt 1 — tên sản phẩm 'iPhone 18' không khớp dòng iPhone đang bán tháng 11/2026. Chỉ đưa lại khi có screenshot trang gốc hoặc voucher thật."},
    "lazada-bf26-vpbank-200k": {"loai_deal": "Ưu đãi thường xuyên", "muc_xac_minh": "B"},
    "lazada-bf26-vpbank-18pct": {"loai_deal": "Ưu đãi thường xuyên", "muc_xac_minh": "B"},
    "lazada-bf26-vpbank-80k": {"loai_deal": "Ưu đãi thường xuyên", "muc_xac_minh": "B"},
    "lazada-bf26-cuoi-thang-25-29": {"loai_deal": "Teaser", "muc_xac_minh": "B"},
    "lazada-bf26-freeship-max": {"loai_deal": "Ưu đãi thường xuyên", "muc_xac_minh": "B"},
    "lazada-bf26-tmall-35pct": {"loai_deal": "Teaser", "muc_xac_minh": "B"},
    # Alibaba (8)
    "alibaba-bf26-led-backpack-28": {"loai_deal": "Teaser", "muc_xac_minh": "B"},
    "alibaba-bf26-gaming-chair-17": {"loai_deal": "Teaser", "muc_xac_minh": "B"},
    "alibaba-bf26-scooter-700": {"loai_deal": "Teaser", "muc_xac_minh": "B"},
    "alibaba-bf26-leather-jacket-30": {"loai_deal": "Teaser", "muc_xac_minh": "B"},
    "alibaba-bf26-hair-bundle-15": {"loai_deal": "Teaser", "muc_xac_minh": "B"},
    "alibaba-bf26-ae-code-otsbf03": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "B"},
    "alibaba-bf26-ae-code-otsbf08": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "B"},
    "alibaba-bf26-ae-code-otsbf19": {"loai_deal": "BF2026 chính thức", "muc_xac_minh": "B"},
}

with open(PATH, encoding="utf-8") as f:
    deals = json.load(f)

assert len(deals) == 71, f"expected 71 deals, got {len(deals)}"
assert len(CLASS) == 71, f"classification covers {len(CLASS)} deals, expected 71"

ids = [d["deal_id"] for d in deals]
assert len(set(ids)) == 71, "duplicate deal_id found"
missing = [d for d in ids if d not in CLASS]
assert not missing, f"deals missing classification: {missing}"

out = []
for deal in deals:
    c = CLASS[deal["deal_id"]]
    new = {}
    for k, v in deal.items():
        new[k] = v
        if k == "trang_thai":
            new["loai_deal"] = c["loai_deal"]
            new["muc_xac_minh"] = c["muc_xac_minh"]
    for key in ("gia_gia_han", "diem_hot", "ghi_chu_tuan_thu"):
        if key in c:
            new[key] = c[key]
    out.append(new)

# Validation
for d in out:
    assert d["loai_deal"] in ("BF2026 chính thức", "Ưu đãi thường xuyên", "Teaser"), d["deal_id"]
    assert d["muc_xac_minh"] in ("A", "B", "C"), d["deal_id"]
    assert d["deal_id"] and d["link_goc"], d["deal_id"]
    assert d["chuong_trinh_affiliate"] == "" and d["link_affiliate"] == "" and d["hoa_hong_uoc_tinh"] == "", d["deal_id"]

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
    f.write("\n")

print("OK — 71 deals re-classified")
print("By level (muc_xac_minh):", dict(Counter(d["muc_xac_minh"] for d in out)))
print("By type (loai_deal):", dict(Counter(d["loai_deal"] for d in out)))
print("By category:", dict(Counter(d["hang_muc"] for d in out)))
print("By status:", dict(Counter(d["trang_thai"] for d in out)))
# Web-publishable: level A, active (not Nghi ngờ, not Hết hạn)
web = [d for d in out if d["muc_xac_minh"] == "A" and d["trang_thai"] in ("Đang chạy", "Sắp diễn ra")]
print("Web-publishable active (A + not Nghi ngờ/Hết hạn):", len(web))
print("Web-publishable by category:", dict(Counter(d["hang_muc"] for d in web)))
# Level A but excluded from web (Nghi ngờ / Hết hạn)
excluded_a = [d["deal_id"] for d in out if d["muc_xac_minh"] == "A" and d["trang_thai"] not in ("Đang chạy", "Sắp diễn ra")]
print("Level A excluded from web (Nghi ngờ/Hết hạn):", excluded_a)
