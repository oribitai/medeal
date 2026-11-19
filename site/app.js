/* Hot Deal Black Friday 2026 — app.js
 * Loads deals.json (same folder), renders filters, sorting, cards and live countdowns.
 * No external dependencies. Countdown dates are explicit ISO strings per deal_id
 * because the source date strings are free-form Vietnamese text.
 * Timezones: EST = UTC-5, PT (PST, November) = UTC-8, UTC as stated.
 */
"use strict";

/* Countdown targets, verified from the official pages on 19/11/2026.
 * start/end are ISO 8601 with explicit offset. Deals NOT listed here have no
 * parseable end date — no countdown is shown for them (see UNPARSEABLE below).
 * Adobe "Ends Dec 6": no timezone on the page, UTC assumed.
 * Higgsfield end (~20/11 00:00 UTC) is approximate, read from the on-page countdown.
 */
const COUNTDOWN = {
  "namecheap-bf26-vps-pulsar-54off":   { start: "2026-11-20T00:00:00-05:00", end: "2026-12-04T23:59:59-05:00" },
  "namecheap-bf26-vps-quasar-41off":   { start: "2026-11-20T00:00:00-05:00", end: "2026-12-04T23:59:59-05:00" },
  "namecheap-bf26-vps-magnetar-40off": { start: "2026-11-20T00:00:00-05:00", end: "2026-12-04T23:59:59-05:00" },
  "namecheap-bf26-com-31off":          { end: "2026-11-19T23:59:59-05:00" },
  "namecheap-bf26-net-20off":          { end: "2026-11-19T23:59:59-05:00" },
  "namecheap-bf26-org-48off":          { end: "2026-11-19T23:59:59-05:00" },
  "namecheap-bf26-com-transfer-43off": { end: "2026-11-19T23:59:59-05:00" },
  "namecheap-bf26-co-87off":           { end: "2026-11-19T23:59:59-05:00" },
  "porkbun-bf26-xyz-91off":            { end: "2026-12-04T23:59:59Z" },
  "porkbun-bf26-bond-92off":           { end: "2026-12-04T23:59:59Z" },
  "porkbun-bf26-blog-90off":           { end: "2026-12-04T23:59:59Z" },
  "porkbun-bf26-shop-92off":           { end: "2026-12-04T23:59:59Z" },
  "porkbun-bf26-asia-91off":           { end: "2026-12-04T23:59:59Z" },
  "adobe-bf26-firefly-pro-50off":      { end: "2026-12-06T23:59:59Z" },
  "adobe-bf26-firefly-proplus-60off":  { end: "2026-12-06T23:59:59Z" },
  "elevenlabs-bf26-creator-55off":     { end: "2026-12-01T23:59:59-05:00" },
  "elevenlabs-bf26-pro-55off":         { end: "2026-12-01T23:59:59-05:00" },
  "higgsfield-bf26-plus-45off":        { end: "2026-11-20T00:00:00Z" },
  "higgsfield-bf26-ultra-60off":       { end: "2026-11-20T00:00:00Z" },
  "prowritingaid-bf26-premium-yearly-50off":       { end: "2026-11-29T23:59:59-08:00" },
  "prowritingaid-bf26-premiumpro-lifetime-50off":  { end: "2026-11-29T23:59:59-08:00" },
  /* Shopee/Lazada, verified from the official pages 19/11/2026 ~17:00.
   * Vietnam time (+07:00). LazMall Brand Day + TMALL SUPER88 end 19/11. */
  "shopee-bf26-newuser-ship-500k":   { end: "2026-11-30T23:59:59+07:00" },
  "shopee-bf26-newuser-ship-300k":   { end: "2026-11-30T23:59:59+07:00" },
  "shopee-bf26-newuser-30k-off":     { end: "2026-11-30T23:59:59+07:00" },
  "shopee-bf26-teachersday-50off":   { end: "2026-11-20T23:59:59+07:00" },
  "shopee-bf26-torriden-15k-off":    { end: "2026-11-30T23:59:59+07:00" },
  "lazada-bf26-lazmall-brandday-35off": { end: "2026-11-19T23:59:59+07:00" },
  "lazada-bf26-tmall-super88-50off":   { end: "2026-11-19T23:59:59+07:00" },
  "lazada-bf26-lazbeauty-50off":       { end: "2026-11-20T23:59:59+07:00" },
  "lazada-bf26-palmers-50k-off":       { end: "2026-11-30T23:59:59+07:00" }
};

/* Deals whose end date could NOT be parsed from the source data (no guessing):
 * vultr-bf26-cloud-300credit, hetzner-bf26-cloud-50credit,
 * pavietnam-bf26-com-95off, pavietnam-bf26-comvn-42off, pavietnam-bf26-xyz-92off.
 * These show no countdown. */

const CATEGORIES = ["VPS", "AI", "Domain", "Shopee", "Alibaba", "Lazada"];
/* Year-round offers: shown in a separate "Ưu đãi quanh năm" section, not in the
 * main Black Friday list. They still count toward their category filter counts. */
const YEAR_ROUND_IDS = new Set([
  "vultr-bf26-cloud-300credit",
  "hetzner-bf26-cloud-50credit",
  "pavietnam-bf26-com-95off",
  "pavietnam-bf26-comvn-42off",
  "pavietnam-bf26-xyz-92off"
]);
const EMPTY_NOTE = "Đang cập nhật, voucher sẽ được kiểm tra trong app ngày 24–25/11.";
const NO_DEAL_NOTE = "Chưa có deal đã xác minh mức A.";

let deals = [];
let currentCat = "all";
let currentSort = "hot";

const $ = (sel) => document.querySelector(sel);

function esc(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

function pctValue(d) {
  const v = d.phan_tram_giam;
  if (typeof v === "number") return v;
  if (typeof v === "string") {
    const m = v.match(/(\d+(?:[.,]\d+)?)/);
    if (m) return parseFloat(m[1].replace(",", "."));
  }
  return null;
}

/* Next relevant date for sorting: start for upcoming deals, end for running ones. */
function nextDate(d) {
  const c = COUNTDOWN[d.deal_id];
  if (!c) return null;
  if (d.trang_thai === "Sắp diễn ra" && c.start) return new Date(c.start).getTime();
  if (c.end) return new Date(c.end).getTime();
  return null;
}

function sortDeals(list) {
  const arr = list.slice();
  if (currentSort === "expiry") {
    arr.sort((a, b) => {
      const da = nextDate(a), db = nextDate(b);
      if (da == null && db == null) return b.diem_hot - a.diem_hot;
      if (da == null) return 1;
      if (db == null) return -1;
      if (da !== db) return da - db;
      return b.diem_hot - a.diem_hot;
    });
  } else {
    arr.sort((a, b) => (b.diem_hot - a.diem_hot) || (String(a.deal_id).localeCompare(String(b.deal_id))));
  }
  return arr;
}

function typeBadgeClass(loai) {
  if (loai === "BF2026 chính thức") return "badge-type-bf";
  if (loai === "Chương trình đang chạy") return "badge-type-bf";
  if (loai === "Ưu đãi thường xuyên") return "badge-type-regular";
  return "badge-type-teaser";
}

function statusBadge(d) {
  if (d.trang_thai === "Sắp diễn ra") return '<span class="badge badge-status-upcoming">Sắp diễn ra</span>';
  if (d.trang_thai === "Nghi ngờ") return '<span class="badge badge-status-suspect">Nghi ngờ</span>';
  if (d.trang_thai === "Hết hạn") return '<span class="badge badge-status-suspect">Hết hạn</span>';
  return '<span class="badge badge-status-running">Đang chạy</span>';
}

function endingSoonBadge(d) {
  const c = COUNTDOWN[d.deal_id];
  if (!c || !c.end) return "";
  const ms = new Date(c.end).getTime() - Date.now();
  if (ms > 0 && ms <= 48 * 3600 * 1000) return '<span class="badge badge-ending">Sắp hết hạn</span>';
  return "";
}

/* % off is vs the renewal price for Porkbun, ElevenLabs and Namecheap VPS. */
function offNote(d) {
  if (d.nha_cung_cap === "Porkbun" || d.nha_cung_cap === "ElevenLabs") return true;
  if (d.nha_cung_cap === "Namecheap" && d.hang_muc === "VPS") return true;
  return false;
}

function warningsFor(d) {
  const out = [];
  if (d.deal_id === "namecheap-bf26-co-87off") {
    out.push('<div class="warning">CẢNH BÁO: gia hạn $45.48/năm, gấp 9,1 lần giá năm đầu.</div>');
  }
  if (d.deal_id === "adobe-bf26-firefly-pro-50off" || d.deal_id === "adobe-bf26-firefly-proplus-60off") {
    out.push('<div class="notice">Chỉ 6 tháng đầu, sau đó về giá thường.</div>');
  }
  return out.join("");
}

function couponRow(d) {
  const c = (d.ma_coupon || "").trim();
  if (!c || c === "chưa xác nhận") return "";
  return '<div class="coupon">Mã coupon: <code>' + esc(c) + "</code></div>";
}

function renewalRow(d) {
  const r = (d.gia_gia_han || "").trim();
  if (!r || r === "chưa xác nhận") return "";
  return '<div class="renewal">Giá gia hạn: <strong>' + esc(r) + "</strong></div>";
}

function countdownHtml(d, yearRound) {
  if (yearRound) {
    return '<div class="countdown" data-cd="none">Không rõ thời hạn</div>';
  }
  if (!COUNTDOWN[d.deal_id]) {
    return '<div class="countdown" data-cd="none">Không có ngày kết thúc xác định.</div>';
  }
  return '<div class="countdown" data-cd="' + esc(d.deal_id) + '">Đang tính&hellip;</div>';
}

function stars(d) {
  const n = Math.max(0, Math.min(5, d.diem_hot || 0));
  return '<span class="stars" aria-label="Độ hot ' + n + '/5">' +
    "★".repeat(n) + "☆".repeat(5 - n) +
    '<span class="hot-label">Độ hot ' + n + "/5</span></span>";
}

function cardHtml(d, opts) {
  const yearRound = !!(opts && opts.yearRound);
  /* rel: "sponsored nofollow" only when an affiliate link exists;
   * otherwise "nofollow noopener". Computed per deal so it flips
   * automatically if link_affiliate is filled in later. */
  const rel = (d.link_affiliate || "").trim() ? "sponsored nofollow" : "nofollow noopener";
  const pct = pctValue(d);
  const cls = ["deal-card"];
  if (d.trang_thai === "Nghi ngờ") cls.push("suspect");
  if (endingSoonBadge(d)) cls.push("ending-soon");
  const offHtml = pct != null
    ? '<span class="price-off">−' + pct + "%</span>" +
      (offNote(d) ? '<span class="off-note">giảm so với giá gia hạn</span>' : "")
    : "";
  const origHtml = d.gia_goc && d.gia_goc !== "chưa xác nhận"
    ? '<span class="price-orig">' + esc(d.gia_goc) + "</span>" : "";
  return '<article class="' + cls.join(" ") + '">' +
    '<div class="deal-top">' +
      '<span class="badge badge-cat">' + esc(d.hang_muc) + "</span>" +
      '<span class="badge ' + typeBadgeClass(d.loai_deal) + '">' + esc(d.loai_deal) + "</span>" +
      (d.muc_xac_minh === "A" ? '<span class="badge badge-verified">Đã xác minh</span>' : "") +
      statusBadge(d) + endingSoonBadge(d) +
    "</div>" +
    '<h3 class="deal-name">' + esc(d.ten_deal) + "</h3>" +
    '<p class="deal-provider">Nhà cung cấp: <strong>' + esc(d.nha_cung_cap) + "</strong></p>" +
    '<div class="price-row">' +
      '<span class="price-deal">' + esc(d.gia_deal) + "</span>" + origHtml + offHtml +
    "</div>" +
    renewalRow(d) +
    couponRow(d) +
    '<dl class="deal-meta">' +
      "<dt>Điều kiện</dt><dd>" + esc(d.dieu_kien) + "</dd>" +
      "<dt>Thời gian</dt><dd>" + esc(d.bat_dau_het_han) + "</dd>" +
    "</dl>" +
    countdownHtml(d, yearRound) +
    (yearRound ? "" : stars(d)) +
    warningsFor(d) +
    '<div class="deal-actions">' +
      '<a class="btn-deal" href="/go/' + encodeURIComponent(d.deal_id) + '" rel="' + rel + '">Xem deal</a>' +
    "</div>" +
    '<div class="deal-id">' + esc(d.deal_id) + "</div>" +
  "</article>";
}

function groupHtml(cat, list) {
  const sorted = sortDeals(list);
  if (cat === "Alibaba") {
    const b2b = sorted.filter((d) => d.nha_cung_cap === "Alibaba.com");
    const ae = sorted.filter((d) => d.nha_cung_cap !== "Alibaba.com");
    const sec = (title, items) =>
      '<div class="subgroup"><h3>' + title + ' <span class="cat-count">(' + items.length + " deal)</span></h3>" +
      (items.length
        ? '<div class="deal-grid">' + items.map(cardHtml).join("") + "</div>"
        : '<p class="empty-note">' + NO_DEAL_NOTE + "</p>") + "</div>";
    return '<section class="cat-section"><h2>Alibaba <span class="cat-count">(' + list.length + " deal)</span></h2>" +
      sec("Alibaba.com (B2B)", b2b) + sec("AliExpress", ae) + "</section>";
  }
  return '<section class="cat-section"><h2>' + esc(cat) + ' <span class="cat-count">(' + list.length + " deal)</span></h2>" +
    '<div class="deal-grid">' + sorted.map(cardHtml).join("") + "</div></section>";
}

/* Separate "Ưu đãi quanh năm" section: year-round offers only.
 * Cards show the "Ưu đãi thường xuyên" loai_deal badge, no hot stars,
 * and "Không rõ thời hạn" instead of a countdown. */
function yearRoundSectionHtml(list) {
  const sorted = sortDeals(list);
  return '<section class="cat-section year-round-section"><h2>Ưu đãi quanh năm <span class="cat-count">(' + list.length + " deal)</span></h2>" +
    '<p class="section-intro">Các ưu đãi này áp dụng quanh năm, không phải chỉ riêng dịp Black Friday.</p>' +
    '<div class="deal-grid">' + sorted.map((d) => cardHtml(d, { yearRound: true })).join("") + "</div></section>";
}

function emptySection(cat) {
  const note = (cat === "Shopee" || cat === "Alibaba" || cat === "Lazada") ? EMPTY_NOTE : NO_DEAL_NOTE;
  if (cat === "Alibaba") {
    return '<section class="cat-section"><h2>Alibaba <span class="cat-count">(0 deal)</span></h2>' +
      '<div class="subgroup"><h3>Alibaba.com (B2B)</h3><p class="empty-note">' + note + "</p></div>" +
      '<div class="subgroup"><h3>AliExpress</h3><p class="empty-note">' + note + "</p></div></section>";
  }
  return '<section class="cat-section"><h2>' + esc(cat) + ' <span class="cat-count">(0 deal)</span></h2>' +
    '<p class="empty-note">' + note + "</p></section>";
}

function render() {
  const counts = { all: deals.length };
  CATEGORIES.forEach((c) => { counts[c] = deals.filter((d) => d.hang_muc === c).length; });
  document.querySelectorAll("[data-count]").forEach((el) => {
    el.textContent = "(" + (counts[el.getAttribute("data-count")] || 0) + ")";
  });
  $("#verified-note").textContent =
    "Đang hiển thị " + deals.length + " deal đã xác minh mức A (VPS " + counts.VPS +
    ", AI " + counts.AI + ", Domain " + counts.Domain +
    ", Shopee " + counts.Shopee + ", Lazada " + counts.Lazada +
    "). Các deal chưa xác nhận không được hiển thị.";

  const box = $("#deals");
  /* Split the filtered list: Black Friday deals in the main sections,
   * year-round offers in a separate section at the bottom. The 5 year-round
   * deals still count toward their category filter counts (computed above). */
  const filtered = currentCat === "all" ? deals : deals.filter((d) => d.hang_muc === currentCat);
  const bf = filtered.filter((d) => !YEAR_ROUND_IDS.has(d.deal_id));
  const yr = filtered.filter((d) => YEAR_ROUND_IDS.has(d.deal_id));
  let html = "";
  if (currentCat === "all") {
    html += CATEGORIES.map((cat) => {
      const list = bf.filter((d) => d.hang_muc === cat);
      return list.length ? groupHtml(cat, list) : emptySection(cat);
    }).join("");
  } else {
    html += bf.length ? groupHtml(currentCat, bf) : emptySection(currentCat);
  }
  if (yr.length) html += yearRoundSectionHtml(yr);
  box.innerHTML = html;
  tickCountdowns();
}

function fmtCountdown(ms) {
  if (ms <= 0) return null;
  const totalSec = Math.floor(ms / 1000);
  const days = Math.floor(totalSec / 86400);
  const hours = Math.floor((totalSec % 86400) / 3600);
  const mins = Math.floor((totalSec % 3600) / 60);
  const secs = totalSec % 60;
  const pad = (n) => String(n).padStart(2, "0");
  return days + " ngày " + pad(hours) + ":" + pad(mins) + ":" + pad(secs);
}

function tickCountdowns() {
  const now = Date.now();
  document.querySelectorAll("[data-cd]").forEach((el) => {
    const id = el.getAttribute("data-cd");
    if (id === "none") return;
    const c = COUNTDOWN[id];
    if (!c) return;
    const deal = deals.find((d) => d.deal_id === id);
    const isUpcoming = deal && deal.trang_thai === "Sắp diễn ra" && c.start;
    let target = null, label = "Kết thúc sau";
    if (isUpcoming) {
      const startMs = new Date(c.start).getTime();
      if (now < startMs) { target = startMs; label = "Bắt đầu sau"; }
      else if (c.end) { target = new Date(c.end).getTime(); }
    } else if (c.end) {
      target = new Date(c.end).getTime();
    }
    if (target == null) { el.textContent = "Không có ngày kết thúc xác định."; return; }
    const left = fmtCountdown(target - now);
    if (left == null) {
      el.textContent = "Đã hết hạn.";
      el.classList.add("expired");
      return;
    }
    el.textContent = label + ": " + left;
    if (target - now <= 48 * 3600 * 1000) el.classList.add("urgent");
  });
}

async function init() {
  const loading = $("#loading"), error = $("#error");
  try {
    /* cache: no-store — Cloudflare đặt Browser Cache TTL mặc định 4h cho
     * trình duyệt, nên deals.json phải bỏ qua cache trình duyệt thì deal
     * mới/hết hạn mới hiện ngay; edge cache vẫn giới hạn ở 60s. */
    const res = await fetch("deals.json", { cache: "no-store" });
    if (!res.ok) throw new Error("HTTP " + res.status);
    deals = await res.json();
    if (!Array.isArray(deals)) throw new Error("deals.json không phải là danh sách");
    loading.hidden = true;
    render();
    setInterval(tickCountdowns, 1000);
  } catch (e) {
    loading.hidden = true;
    error.hidden = false;
    error.textContent = "Không tải được dữ liệu deal (deals.json). Vui lòng thử lại sau. (" + e.message + ")";
  }
}

document.querySelectorAll(".filter-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".filter-btn").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    currentCat = btn.getAttribute("data-cat");
    render();
  });
});

$("#sort-select").addEventListener("change", (e) => {
  currentSort = e.target.value;
  render();
});

init();
