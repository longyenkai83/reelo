# specs.md — Tái cấu trúc Reelo Mức B / Đợt B1 (lõi bán được)

> Yêu cầu + tiêu chí nghiệm thu cho đợt B1. Delta so với baseline hiện tại (Mức A đã áp dụng).
> Phạm vi B1: tách `_private/` (brand + kho-kien-thuc) + `engine/cong-thuc-viral/` + `scripts/export.sh`. **KHÔNG** đụng scripts-output/carousel-output (để đợt B2).

---

## YÊU CẦU 1 — Tách ENGINE ↔ DATA RIÊNG (điều kiện để BÁN)

**Mô tả:** Mọi thứ riêng chị Hiền phải nằm gọn trong `_private/`; engine (skill/agent/công thức) không chứa gì riêng brand.

**Tiêu chí nghiệm thu:**
- [ ] AC1.1 — `_private/brand/nhi-hien/` chứa TOÀN BỘ file trước ở `kho-kien-thuc/cong-thuc-viral/brand-profiles/nhi-hien/` (16+ file, gồm `references/` + `mau-giong-chuan/`). Không sót file.
- [ ] AC1.2 — `_private/kho-kien-thuc/raw/` và `_private/kho-kien-thuc/wiki/` chứa toàn bộ raw (69) + wiki (74) cũ, GIỮ quan hệ raw↔wiki cạnh nhau (để wikilink không gãy).
- [ ] AC1.3 — `engine/cong-thuc-viral/` chứa 11 file công thức chung + `_mau-brand-profile.md` + `_quy-trinh-tinh-chinh-voice.md` + `khach-hang-mau/` (template tạo brand). KHÔNG còn `brand-profiles/nhi-hien/` bên trong.
- [ ] AC1.4 — Sau tách, grep toàn `.claude/` + `engine/` (trừ `_private/`) KHÔNG còn chuỗi dữ liệu riêng "nhi-hien", "Trịnh Nhi Hiền" (trừ ví dụ minh họa có chủ đích trong template).

## YÊU CẦU 2 — Đồng bộ 100% đường dẫn (không gãy hệ thống)

**Tiêu chí nghiệm thu:**
- [ ] AC2.1 — Mọi path tuyệt đối `kho-kien-thuc/cong-thuc-viral/brand-profiles/<brand>/…` đổi thành `_private/brand/<brand>/…` (điểm nứt kép: phần `cong-thuc-viral` KHÔNG giữ lại).
- [ ] AC2.2 — Mọi path `kho-kien-thuc/raw/…` · `kho-kien-thuc/wiki/…` (tuyệt đối từ root) đổi prefix thành `_private/kho-kien-thuc/raw|wiki/…`.
- [ ] AC2.3 — Mọi path `kho-kien-thuc/cong-thuc-viral/<công-thức>.md` (KHÔNG brand) đổi thành `engine/cong-thuc-viral/<công-thức>.md`.
- [ ] AC2.4 — Wikilink `[[raw/…]]`, `[[wiki/…]]`, relative `../raw/…` bên TRONG cụm wiki/raw GIỮ NGUYÊN (đã xác minh: resolve theo tên, không gãy khi dời cùng nhau).
- [ ] AC2.5 — Test khói: mở phiên mới, chạy `/viet-bai` với 1 link → skill đọc được voice/ma-tran/kho-cau-chuyen ở vị trí mới, không báo "không tìm thấy file".
- [ ] AC2.6 — `don-kho` (quét wiki) + `critic-ban-giam-khao` (đối chiếu raw/wiki) trỏ đúng `_private/kho-kien-thuc/`.

## YÊU CẦU 3 — Cơ chế xuất bản bán (export.sh)

**Tiêu chí nghiệm thu:**
- [ ] AC3.1 — `scripts/export.sh <thư-mục-đích>` copy toàn project SANG đích, TỰ loại bỏ `_private/` + `scripts-output/` + `carousel-output/` + `_backup/` + `.obsidian/` + `NHAT-KY-PHIEN*.md` + `SO-LOI-REELO.md`.
- [ ] AC3.2 — Bản xuất giữ: `.claude/` + `engine/` + `CLAUDE.md` + `README.md` + `docs/` + `openspec/specs` + `scripts/`.
- [ ] AC3.3 — Bản xuất, khi mở phiên, engine tự nhận diện "không có `_private/`" → chuyển sang chế độ intake (dùng `/bat-dau` + `_mau-brand-profile.md`) thay vì báo lỗi thiếu brand.

## NGOÀI PHẠM VI B1 (ghi rõ để không lạm)
- Gom output → `san-pham/` (đợt B2).
- Xây cỗ máy nhân bản đa-brand tự động (đợi brand thật thứ 2 — giữ ranh giới NT2).
- Đổi tên/gộp file bên trong các folder (chỉ DI CHUYỂN nguyên khối + sync path).
- Sửa nội dung luật/công thức (đây là đợt cấu trúc, không đợt nội dung).
