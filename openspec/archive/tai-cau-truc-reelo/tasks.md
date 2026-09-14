# tasks.md — Đợt B1 (lõi bán được) — lộ trình từng chặng

> ✅ **B1 ĐÃ APPLY 2026-07-09.** Chặng 0–7 xong (backup 234 file · move sạch · 60 sync path/35 file · nghiệm thu path sạch · test tồn tại + count khớp 100%). **CÒN:** Chặng 8 (archive change) — đợi chị Hiền test `/viet-bai` thật vài phiên rồi mới archive. **B1.5 (chuyển luật ENGINE chung → `.claude/rules/`)** + **B2 (gom output → `san-pham/`)** = đợt sau, chưa làm.


> Mỗi CHẶNG là 1 cụm nhỏ, làm xong TEST rồi mới sang chặng sau. Backup trước khi động.
> Nguồn path: bản đồ quét 2026-07-09 (vịt con Explore). Chỉ liệt kê **vùng SỐNG** — `_backup/`, `_archive/`, `openspec/changes/`, `NHAT-KY`, `SO-LOI`, `.obsidian/` KHÔNG sync (là lịch sử/tự sinh).

---

## CHẶNG 0 — Backup mốc mới (bắt buộc trước khi động)
- [ ] T0.1 — Copy toàn bộ folder cần dời sang `_backup/2026-07-09-tai-cau-truc-B1/` (brand-profiles, raw, wiki, cong-thuc-viral, + các file .claude sẽ sửa path).
- [ ] T0.2 — Ghi 1 dòng NHAT-KY: "bắt đầu B1, backup mốc 2026-07-09".

## CHẶNG 1 — Dời DATA RIÊNG vào `_private/`
- [ ] T1.1 — Tạo `_private/`.
- [ ] T1.2 — MOVE `kho-kien-thuc/cong-thuc-viral/brand-profiles/` → `_private/brand/`. *(gồm nhi-hien/ + _mau-brand-profile.md + _quy-trinh-tinh-chinh-voice.md + khach-hang-mau/)* — **KHOAN**: 3 file `_mau…`, `_quy-trinh…`, `khach-hang-mau/` là TEMPLATE ENGINE → xem T2.2, chỉ dời `nhi-hien/` + các `_mau` theo đúng đích. → **Chốt:** `brand-profiles/nhi-hien/` → `_private/brand/nhi-hien/`; còn `_mau-brand-profile.md` + `_quy-trinh-tinh-chinh-voice.md` + `khach-hang-mau/` → `engine/cong-thuc-viral/mau-brand/` (template, chặng 2).
- [ ] T1.3 — MOVE `kho-kien-thuc/raw/` → `_private/kho-kien-thuc/raw/` (giữ nguyên tên file + _archive con nếu có).
- [ ] T1.4 — MOVE `kho-kien-thuc/wiki/` → `_private/kho-kien-thuc/wiki/` (giữ `_archive/` con). Dời CÙNG raw để wikilink không gãy.

## CHẶNG 2 — Dời ENGINE tri thức
- [ ] T2.1 — MOVE `kho-kien-thuc/cong-thuc-viral/` (11 file công thức còn lại: _INDEX, psychology-gate, story-structures, nguyen-ly-tam-ly, dinh-dang-dau-ra, chien-luoc-content, checklist-hook, kho-hook, hook-system, bo-tieu-de, cong-kiem-chat-luong) → `engine/cong-thuc-viral/`.
- [ ] T2.2 — Dời template tạo brand → `engine/cong-thuc-viral/mau-brand/`: `_mau-brand-profile.md`, `_quy-trinh-tinh-chinh-voice.md`, `khach-hang-mau/thu-thap-offer.md`.
- [ ] T2.3 — `kho-kien-thuc/` giờ RỖNG (chỉ còn vỏ) → xóa vỏ hoặc để trống (báo Tuấn, không tự xóa nếu còn file lạ).

## CHẶNG 3 — SYNC PATH nhóm brand-profiles → `_private/brand/`
*(đổi prefix `kho-kien-thuc/cong-thuc-viral/brand-profiles/<b>/` VÀ `brand-profiles/<b>/` → `_private/brand/<b>/`)*
- [ ] T3.1 — `CLAUDE.md:11`
- [ ] T3.2 — `SOP-MASTER.md:2,22` (dòng 22 = điểm nứt kép)
- [ ] T3.3 — `.claude/skills/bat-dau/SKILL.md:3,11,12,33,36,45,60,71` ⚠️ mật độ cao nhất (8 chỗ)
- [ ] T3.4 — `.claude/skills/nap-chuyen/SKILL.md:3,8,11` (dòng 11 = nứt kép)
- [ ] T3.5 — `.claude/skills/nap-insight/SKILL.md:12`
- [ ] T3.6 — `.claude/skills/review-chu-ky/SKILL.md:13`
- [ ] T3.7 — `.claude/skills/viet-script/SKILL.md:51`
- [ ] T3.8 — `.claude/skills/viet-script/vietnamese-language-layer.md:48`
- [ ] T3.9 — `.claude/skills/viet-script/references/khung-caption.md:10`
- [ ] T3.10 — `.claude/skills/viet-script/references/che-do-batch.md:8,17`
- [ ] T3.11 — `.claude/skills/viet-script/references/setup-audience.md:3,11`
- [ ] T3.12 — File đã DỜI, path nội bộ tự đổi khi biên tập nội dung: `engine/cong-thuc-viral/_INDEX.md:24`, `psychology-gate.md:7,28,30`, `chien-luoc-content.md:79,80,84`, `mau-brand/_mau-brand-profile.md:4,35,38`, `mau-brand/_quy-trinh…:11`.
- [ ] T3.13 — `_private/kho-kien-thuc/wiki/2026-06-26-insight-ap-luc-me-bim-kinh-doanh.md:16`
- [ ] T3.14 — `scripts-output/_INDEX.md:79`

## CHẶNG 4 — SYNC PATH nhóm raw/wiki tuyệt đối → `_private/kho-kien-thuc/`
*(chỉ path TUYỆT ĐỐI từ root; wikilink [[raw/]] + relative ../raw/ GIỮ NGUYÊN)*
- [ ] T4.1 — `CLAUDE.md:36`
- [ ] T4.2 — `.claude/skills/don-kho/SKILL.md:3,8,12,18,24,32` ⚠️ logic quét kho phụ thuộc path
- [ ] T4.3 — `.claude/skills/viet-script/references/checklist-truoc-khi-trinh.md:14`
- [ ] T4.4 — `.claude/skills/viet-script/references/format-carousel.md:37,41`
- [ ] T4.5 — `.claude/agents/critic-ban-giam-khao.md:23,49` (+ dòng 19 = cong-thuc-viral, xem T5)
- [ ] T4.6 — Các file OUTPUT trỏ `kho-kien-thuc/wiki/…`: carousel-output (8 file, dòng 4/7) + scripts-output (12 file). *(Đây là output data — sync để link tra cứu đúng; nếu B2 gom sau thì làm luôn ở đây.)*

## CHẶNG 5 — SYNC PATH nhóm cong-thuc-viral → `engine/cong-thuc-viral/`
- [ ] T5.1 — `SOP-MASTER.md:21,22,23`
- [ ] T5.2 — `.claude/skills/nap-chuyen/SKILL.md:11` (nứt kép: phần cong-thuc→engine, phần brand→_private)
- [ ] T5.3 — `.claude/agents/critic-ban-giam-khao.md:19`
- [ ] T5.4 — 2 nhãn text `cong-thuc-viral` trong wiki (kallaway-48, ips16-ngay2) = NHÃN chủ đề, KHÔNG phải path → GIỮ NGUYÊN.

## CHẶNG 6 — Tạo cơ chế bán
- [ ] T6.1 — Viết `scripts/export.sh` (loại `_private/`, output, `_backup/`, `.obsidian/`, nhật ký/sổ lỗi).
- [ ] T6.2 — Thêm vào `CLAUDE.md` mục 1: "IF không có `_private/` → chế độ intake brand mới (`/bat-dau`)" (cho bản bán).
- [ ] T6.3 — Cập nhật CLAUDE.md "Reelo là gì" + bản đồ folder phản ánh cây mới.

## CHẶNG 7 — Nghiệm thu (đối chiếu specs.md)
- [ ] T7.1 — Grep `.claude/` + `engine/` KHÔNG còn "brand-profiles" hay "kho-kien-thuc/raw|wiki" (path cũ). (AC2.1–2.3)
- [ ] T7.2 — Grep engine KHÔNG lộ data "nhi-hien" (trừ template minh họa). (AC1.4)
- [ ] T7.3 — TEST KHÓI phiên mới: `/viet-bai <link>` → đọc được voice/ma-tran/kho-cau-chuyen. (AC2.5)
- [ ] T7.4 — Mở Obsidian: wikilink raw↔wiki không gãy (graph còn nối). (AC2.4)
- [ ] T7.5 — Báo Tuấn kết quả từng AC → Tuấn nghiệm thu.

## CHẶNG 8 — Archive change
- [ ] T8.1 — Gộp delta vào `openspec/specs/` (cập nhật baseline cây mới).
- [ ] T8.2 — Chuyển `openspec/changes/tai-cau-truc-reelo/` → `openspec/archive/`.

---
### ⚠️ 4 điểm rủi ro cao (bản đồ path cảnh báo) — soi kỹ khi làm:
1. `bat-dau/SKILL.md` — 8 path brand trong 1 file.
2. `don-kho/SKILL.md` — 6 path raw/wiki, logic quét phụ thuộc.
3. `SOP-MASTER.md` — chạm CẢ 4 loại path (~10 dòng), nứt kép ở dòng 22.
4. Điểm nứt kép `cong-thuc-viral/brand-profiles/nhi-hien/X`: cắt 2 đích — `nhi-hien/X` → `_private/brand/nhi-hien/X` (KHÔNG phải engine).
