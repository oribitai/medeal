#!/usr/bin/env python3
"""Append Shopee/Lazada 19/11/2026 web-check deals to deals.json (71 -> 90).
9 level-A + 10 level-C (grouped 'chua xac nhan'). Site/deals.json untouched.
"""
import json, sys

PATH = "/home/hatch/workspace/black-friday-deals/deals.json"

def base(deal_id, ten, hang, cung, gia_deal, pct, dieu_kien, han, link, nguon,
         trang_thai, muc, hot, ghi_chu, coupon="Không cần nhập mã", gia_goc="chưa xác nhận"):
    return {
        "deal_id": deal_id,
        "ten_deal": ten,
        "hang_muc": hang,
        "nha_cung_cap": cung,
        "gia_goc": gia_goc,
        "gia_deal": gia_deal,
        "phan_tram_giam": pct,
        "gia_gia_han": "Không áp dụng",
        "ma_coupon": coupon,
        "dieu_kien": dieu_kien,
        "bat_dau_het_han": han,
        "link_goc": link,
        "nguon_xac_minh": nguon,
        "ngay_gio_kiem_tra": "19/11/2026 17:00 +07",
        "trang_thai": trang_thai,
        "loai_deal": "Chương trình đang chạy",
        "muc_xac_minh": muc,
        "diem_hot": hot,
        "chuong_trinh_affiliate": "",
        "link_affiliate": "",
        "hoa_hong_uoc_tinh": "",
        "ghi_chu_tuan_thu": ghi_chu,
        "link_dang_ky_affiliate": "https://affiliate.shopee.vn" if hang == "Shopee" else "chưa rõ",
    }

S = "Trang chính thức Shopee (trình duyệt, 19/11/2026)"
L = "Trang chính thức Lazada (trình duyệt, 19/11/2026)"

new = [
    # ---- Shopee level A (5) ----
    base("shopee-bf26-newuser-ship-500k", "Voucher freeship đơn đầu tiên giảm tối đa 500.000đ",
         "Shopee", "Shopee", "Giảm tối đa 500.000đ phí vận chuyển", "chưa xác nhận",
         "Đơn đầu tiên, tối thiểu 0đ; mỗi đơn đầu chỉ dùng 1 voucher vận chuyển + 1 voucher giảm giá; nhận voucher cần đăng nhập",
         "30/11/2026", "https://shopee.vn/m/don-dau-tien-mien-phi", S,
         "Đang chạy", "A", 2, "Nhận voucher cần đăng nhập (chưa thử)."),
    base("shopee-bf26-newuser-ship-300k", "Voucher freeship đơn đầu tiên giảm tối đa 300.000đ",
         "Shopee", "Shopee", "Giảm tối đa 300.000đ phí vận chuyển", "chưa xác nhận",
         "Đơn đầu tiên, tối thiểu 0đ; nhận voucher cần đăng nhập",
         "30/11/2026", "https://shopee.vn/m/don-dau-tien-mien-phi", S,
         "Đang chạy", "A", 2, "Nhận voucher cần đăng nhập (chưa thử)."),
    base("shopee-bf26-newuser-30k-off", "Voucher khách mới giảm 30.000đ đơn đầu tiên",
         "Shopee", "Shopee", "Giảm 30.000đ", "chưa xác nhận",
         "Đơn đầu tiên, tối thiểu 0đ; nhận voucher cần đăng nhập",
         "30/11/2026", "https://shopee.vn/m/don-dau-tien-mien-phi", S,
         "Đang chạy", "A", 2, "Nhận voucher cần đăng nhập (chưa thử)."),
    base("shopee-bf26-teachersday-50off", "Sale ngày nhà giáo giảm đến 50%, giá từ 1.000đ",
         "Shopee", "Shopee", "Giảm đến 50%, giá từ 1.000đ", "50",
         "Freeship nhanh nội thành Hà Nội và TP.HCM, số lượng có hạn",
         "20/11/2026", "https://shopee.vn/m/teacherday-1126", S,
         "Đang chạy", "A", 3, "Sale kết thúc 20/11/2026."),
    base("shopee-bf26-torriden-15k-off", "Voucher Torriden Official Store giảm 15.000đ",
         "Shopee", "Shopee", "Giảm 15.000đ", "chưa xác nhận",
         "Đơn tối thiểu 350.000đ; voucher Mall; nhận voucher cần đăng nhập",
         "30/11/2026", "https://shopee.vn/m/teacherday-1126", S,
         "Đang chạy", "A", 1, "Voucher gian hàng Torriden trên trang Teachers' Day."),
    # ---- Lazada level A (4) ----
    base("lazada-bf26-lazmall-brandday-35off", "LazMall Brand Day voucher đến 35%, trợ giá đến 1.000.000đ, freeship 0đ",
         "Lazada", "Lazada", "Voucher đến 35%, trợ giá đến 1.000.000đ, freeship 0đ", "35",
         "Áp dụng gian hàng LazMall chính hãng",
         "19/11/2026", "https://pages.lazada.vn/wow/gcp/route/lazada/vn/upr_1000345_lazada/channel/vn/upr-router/vn?wx_navbar_transparent=true&hybrid=1&data_prefetch=true&at_iframe=1&disable_bounces=true&lzd_navbar_hidden=true&pha=true&disable_pull_refresh=true&prefetch_replace=1&wh_pid=/lazada/superseries/vn/tmall-brand-day-18-19Nov/nha-cua", L,
         "Đang chạy", "A", 3, "Tiêu đề trang ghi 'Tmall Brand Day 18-19.10' nhưng banner và đường dẫn ghi 18-19.11 — đã lấy theo banner/đường dẫn. Hết hạn trong ngày 19/11."),
    base("lazada-bf26-tmall-super88-50off", "TMALL SUPER88 Sale giảm đến 50%, freeship 0đ",
         "Lazada", "Lazada", "Giảm đến 50%, freeship 0đ, hơn 10.000 cửa hàng quốc tế", "50",
         "Áp dụng cửa hàng quốc tế TMALL",
         "19/11/2026", "https://pages.lazada.vn/wow/gcp/route/lazada/vn/upr_1000345_lazada/channel/vn/upr-router/vn?hybrid=1&data_prefetch=true&prefetch_replace=1&at_iframe=1&wh_pid=%2Flazada%2Fchannel%2Fvn%2Flazmall-channel%2Fthuong-hieu-trung-chinh-hang&spm=a2o4n.homepage.platformCampaignBanner.d_0", L,
         "Đang chạy", "A", 3, "Hết hạn trong ngày 19/11."),
    base("lazada-bf26-lazbeauty-50off", "LazBeauty voucher tối đa 400.000đ, mua 3 giảm thêm 10%, giảm đến 50%",
         "Lazada", "Lazada", "Voucher tối đa 400.000đ, mua 3 giảm thêm 10%, giảm đến 50%, freeship 0đ", "50",
         "Áp dụng ngành hàng làm đẹp LazBeauty",
         "20/11/2026", "https://pages.lazada.vn/wow/gcp/route/lazada/vn/upr_1000345_lazada/channel/vn/upr-router/vn?wx_navbar_transparent=true&hybrid=1&data_prefetch=true&at_iframe=1&disable_bounces=true&lzd_navbar_hidden=true&pha=true&disable_pull_refresh=true&prefetch_replace=1&wh_pid=%2Flazada%2Fmegascenario%2Fvn%2Flazbeauty-11-2026%2FJ38XsyQrCW&spm=a2o4n.homepage.bannerSliderDesktop.d_2", L,
         "Đang chạy", "A", 3, "Hết hạn 20/11/2026."),
    base("lazada-bf26-palmers-50k-off", "Voucher gian hàng PALMERS giảm 50.000đ",
         "Lazada", "Lazada", "Giảm 50.000đ", "chưa xác nhận",
         "Đơn tối thiểu 100.000đ; nhận voucher cần đăng nhập",
         "01/11/2026 – 30/11/2026", "https://pages.lazada.vn/wow/gcp/route/lazada/vn/upr_1000345_lazada/channel/vn/upr-router/vn?wx_navbar_transparent=true&hybrid=1&data_prefetch=true&at_iframe=1&disable_bounces=true&lzd_navbar_hidden=true&pha=true&disable_pull_refresh=true&prefetch_replace=1&wh_pid=%2Flazada%2Fmegascenario%2Fvn%2Flazbeauty-11-2026%2FJ38XsyQrCW&spm=a2o4n.homepage.bannerSliderDesktop.d_2", L,
         "Đang chạy", "A", 2, "Voucher gian hàng PALMERS trên trang LazBeauty."),
    # ---- Shopee level C — chua xac nhan (4) ----
    base("shopee-bf26-voucher-xtra-hien-tai", "Voucher Xtra tiệc cuối năm (chưa xác nhận)",
         "Shopee", "Shopee", "chưa xác nhận", "chưa xác nhận",
         "Giảm 25% tối đa 100.000đ (tối thiểu 100.000đ); 20% tối đa 300.000đ (tối thiểu 500.000đ); 20% tối đa 2.000.000đ (tối thiểu 2.000.000đ)",
         "chưa xác nhận", "https://shopee.vn/m/VoucherXtra", S,
         "Đang chạy", "C", 1, "Chưa xác nhận: không thấy ngày hết hạn trên trang; phần lớn voucher đã hết lượt; bấm xem điều khoản chuyển sang trang đăng nhập. Cần đăng nhập/app để xác minh."),
    base("shopee-bf26-voucher-hub", "Kho voucher Shopee (chưa xác nhận)",
         "Shopee", "Shopee", "chưa xác nhận", "chưa xác nhận",
         "ShopeeVIP giảm 25% tối đa 200.000đ; toàn ngành 25% tối đa 100.000đ; 20% tối đa 300.000đ/2.000.000đ; khách mới giảm 80.000đ/60.000đ/50.000đ/40.000đ",
         "chưa xác nhận", "https://shopee.vn/m/ma-giam-gia", S,
         "Đang chạy", "C", 1, "Chưa xác nhận: tất cả đều hiển thị 'Đã hết lượt', không thấy ngày hết hạn. Cần đăng nhập/app để xác minh."),
    base("shopee-bf26-flash-deals", "Flash Deals theo giờ (chưa xác nhận)",
         "Shopee", "Shopee", "chưa xác nhận", "chưa xác nhận",
         "Giảm giá theo từng sản phẩm, theo khung giờ trong ngày",
         "chưa xác nhận", "https://shopee.vn/flash_sale", S,
         "Đang chạy", "C", 1, "Chưa xác nhận: chỉ thấy khung giờ 19/11 (17:00, 19:00, 21:00), không có giá trị giảm hay hạn chung cho cả chương trình."),
    base("shopee-bf26-shopeepay", "Ưu đãi ShopeePay / ví / ngân hàng (chưa xác nhận)",
         "Shopee", "Shopee", "chưa xác nhận", "chưa xác nhận",
         "Ưu đãi thanh toán qua ShopeePay, ví và ngân hàng",
         "chưa xác nhận", "https://shopee.vn/", S,
         "Đang chạy", "C", 1, "Chưa xác nhận: không xem được trên web khi chưa đăng nhập; chi tiết freeship ghi 'xem trên Ứng dụng Shopee'. Cần kiểm tra trong app."),
    # ---- Lazada level C — chua xac nhan (6) ----
    base("lazada-bf26-voucher-hub", "Kho voucher Lazada (chưa xác nhận)",
         "Lazada", "Lazada", "chưa xác nhận", "chưa xác nhận",
         "Kho mã giảm giá Lazada",
         "chưa xác nhận", "https://www.lazada.vn/wow/i/vn/catalog/coupon/home", L,
         "Đang chạy", "C", 1, "Chưa xác nhận: trang kho voucher báo 'Page Not Found' trên web; bấm 'Mã Giảm Giá' bị chuyển về trang chủ. Có vẻ chỉ lấy được trong app."),
    base("lazada-bf26-vib-lazcard", "Thẻ VIB LazCard hoàn đến 500.000đ (chưa xác nhận)",
         "Lazada", "Lazada", "chưa xác nhận", "chưa xác nhận",
         "Hoàn đến 500.000đ ngày đặc biệt / 100.000đ ngày thường",
         "chưa xác nhận", "https://www.lazada.vn/", L,
         "Đang chạy", "C", 1, "Chưa xác nhận: % hoàn không rõ, không có một hạn chung; ảnh điều khoản ghi ngày đặc biệt 10–13/11 (đã qua) và 11–14/12, lẫn mốc Tết 03/2025 — nội dung cũ/lẫn lộn."),
    base("lazada-bf26-uob-citi", "Mở thẻ UOB / Lazada Citi tích điểm x10 (chưa xác nhận)",
         "Lazada", "Lazada", "chưa xác nhận", "chưa xác nhận",
         "Mở thẻ tín dụng mới để tích điểm thưởng",
         "chưa xác nhận", "https://pages.lazada.vn/wow/gcp/lazada/channel/vn/partnership/lazada-citi-mo-the", L,
         "Đang chạy", "C", 1, "Chưa xác nhận: chỉ thấy 'X10 điểm thưởng', không có hạn hay giá trị tiền mặt; mở thẻ là đăng ký mới."),
    base("lazada-bf26-nestle-spotlight", "Nestlé LazMall Brand Spotlight mua 1 được 2, quà đến 3 triệu (chưa xác nhận)",
         "Lazada", "Lazada", "chưa xác nhận", "chưa xác nhận",
         "Mua 1 được 2, quà đến 3.000.000đ",
         "19/11/2026", "https://www.lazada.vn/", L,
         "Đang chạy", "C", 1, "Chưa xác nhận: chỉ thấy banner trên trang chủ, bấm vào lại mở sang trang khác nên chưa mở được trang riêng của chương trình."),
    base("lazada-bf26-vention-brandday", "Vention Brand Day giảm đến 40%, freeship 0đ (chưa xác nhận)",
         "Lazada", "Lazada", "Giảm đến 40%, freeship 0đ", "40",
         "Áp dụng gian hàng Vention",
         "19/11/2026", "https://www.lazada.vn/", L,
         "Đang chạy", "C", 1, "Chưa xác nhận: chỉ thấy banner trên trang chủ, bấm vào lại mở sang trang khác nên chưa mở được trang riêng của chương trình."),
    base("lazada-bf26-lazbeauty-store-vouchers", "Voucher các gian hàng LazBeauty (chưa xác nhận)",
         "Lazada", "Lazada", "chưa xác nhận", "chưa xác nhận",
         "Anessa giảm 29% (tối thiểu 450.000đ, 18/11–24/11); Yves Rocher giảm 12% (tối thiểu 250.000đ, 01/11–30/11); CARSLAN giảm 10% (18/11–30/11); Laneige giảm 11% (tối thiểu 599.000đ, 15/11–20/11)",
         "chưa xác nhận", "https://pages.lazada.vn/wow/gcp/route/lazada/vn/upr_1000345_lazada/channel/vn/upr-router/vn?wx_navbar_transparent=true&hybrid=1&data_prefetch=true&at_iframe=1&disable_bounces=true&lzd_navbar_hidden=true&pha=true&disable_pull_refresh=true&prefetch_replace=1&wh_pid=%2Flazada%2Fmegascenario%2Fvn%2Flazbeauty-11-2026%2FJ38XsyQrCW&spm=a2o4n.homepage.bannerSliderDesktop.d_2", L,
         "Đang chạy", "C", 1, "Chưa xác nhận: giá trị và hạn đọc được trên trang LazBeauty nhưng nhận voucher cần đăng nhập; không tách thành từng deal mức A riêng."),
]

d = json.load(open(PATH))
ids = {x["deal_id"] for x in d}
dup = [x["deal_id"] for x in new if x["deal_id"] in ids]
if dup:
    print("TRUNG deal_id:", dup); sys.exit(1)
d.extend(new)
json.dump(d, open(PATH, "w"), ensure_ascii=False, indent=2)
from collections import Counter
print("total:", len(d))
print("A/B/C:", Counter(x["muc_xac_minh"] for x in d))
print("Shopee/Lazada:", Counter(x["hang_muc"] for x in d if x["hang_muc"] in ("Shopee", "Lazada")))
print("new ids ok:", len(new))
