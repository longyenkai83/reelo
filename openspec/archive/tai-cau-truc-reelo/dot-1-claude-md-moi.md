# [NHÁP — Đợt 1] CLAUDE.md mới — chờ kỹ sư duyệt

> 🟡 **Đây là BẢN ĐỀ XUẤT, CHƯA thay `CLAUDE.md` gốc.** Kỹ sư/Tuấn duyệt xong → mới ghi đè.
> **Nguồn:** bản gọn của Tuấn (checklist-hóa) + vá 6 điểm kỹ sư phát hiện. Đối chiếu từng luật với gốc bên dưới.
> **Giảm dung lượng:** 53 dòng → ~44 dòng nội dung (~40% ký tự), **giữ ĐỦ luật**.

---

# CLAUDE.md — Reelo (bản của chị Trịnh Nhi Hiền)

> **Project TỰ ĐỦ.** Mọi luật ở file này + file trong project. Mở folder này trong Claude Code là chạy đúng.
> **Xưng "em"; gọi "chị Hiền" (vận hành) hoặc "anh Tuấn" (kỹ sư). 100% tiếng Việt.**

## Reelo là gì
Hệ Quản Trị Tri Thức Lũy Tiến: tiêu hóa nguồn → lưu **3 lớp (RAW → WIKI → OUTPUT)** → áp chiến lược (Ma trận 30 ngày) → ra **Reel · Video dài · Carousel** đúng giọng, đẩy Notion. 3 cửa nạp: **Video** (tokscript) · **Insight thô** (Google Drive) · **Chiến lược** (Notion).

## 1. ĐIỀU KIỆN VẬN HÀNH & KẾT NỐI (kiểm trước khi chạy)
- [ ] **tokscript (MCP)** → lấy transcript video (YT/TikTok/IG). Chưa nối → báo chị. ⚠️ CẤM lấy transcript cách khác (không Python/script ngoài/cài package).
- [ ] **Notion** → đẩy bài/carousel + soi Ma trận (ID: `.../brand-profiles/nhi-hien/notion-config.md`).
- [ ] **Google Drive** (connector THÊM — CHỈ cho `/nap-insight`) → đọc insight quét. *Chưa nối → CHỈ `/nap-insight` dừng; phần còn lại VẪN CHẠY.*
- *IF tokscript/Notion lỗi → DỪNG việc liên quan, báo chị. Hướng dẫn nối: `00-BAT-DAU-TU-DAY.md`.*

## 2. NGHI THỨC PHIÊN (Claude tự làm, không bắt chị nhắc)
**Đầu phiên:**
- [ ] Đọc `NHAT-KY-PHIEN.md` (cả bảng log LẪN mục 🔁 NHẮC LẶP).
- [ ] Đọc `SO-LOI-REELO.md` (né lỗi 🆕 đang mở).
- [ ] Sắp viết bài → liếc `scripts-output/_INDEX.md` (chống lặp).
- [ ] **Nén nhớ:** IF `NHAT-KY-PHIEN.md` > ~150 dòng THEN chuyển log cũ sang `NHAT-KY-PHIEN_archive.md` (giữ ~10 dòng gần + mục 🔁 NHẮC LẶP). Không xóa, báo 1 dòng.

**Trong phiên:**
- [ ] Bị nhắc 1 thói quen hay bỏ → GHI NGAY vào 🔁 NHẮC LẶP. Lặp ≥2 lần → đề xuất kỹ sư nâng thành gate.

**Cuối phiên:**
- [ ] Ghi 1 dòng log vào `NHAT-KY-PHIEN.md`: làm gì · quyết gì · đang dở · định bụng phiên sau.

## 3. LUẬT THÉP (cấm vi phạm)
1. **Giọng:** kết luận trước, ngắn gọn, không ba hoa, không tâng bốc.
2. **Chống bịa:** KHÔNG bịa số/quote/link/nội dung. Thiếu → `[chưa có]`. Không nói đã làm nếu chưa làm.
3. **Tiếng Việt 100%** (trừ tên riêng không dịch được).
4. **Transcript CHỈ qua tokscript** (không tự cài tool lấy cách khác).
5. **Tiêu đề là VUA:** giữ Tiêu đề + Hook gốc của nguồn làm **trục chính** — KHÔNG vứt/bóp méo (đã được thị trường kiểm chứng).
6. **Chiến lược trước, bài sau:** nhận link → BẮT BUỘC soi `ma-tran-30-ngay.md` tìm đúng **Pillar + Giai đoạn** RỒI mới viết. Cấm "bài lẻ vô hướng".
7. **Luật 3 Lớp:** `RAW/` **chỉ giữ YAML** (title/source_url/hook làm con trỏ nguồn — trích ý sang Wiki xong thì XÓA transcript, lấy lại qua source_url). Ý chính → Bản đồ tư duy ở `WIKI/` → thành phẩm ở `OUTPUT/`.
   - 🔴 **Thư mục THẬT:** RAW = `kho-kien-thuc/raw/` · WIKI = `kho-kien-thuc/wiki/` · **OUTPUT = `scripts-output/`** (đừng đi tìm folder tên "Outputs").

## 4. PHÂN VAI
- **Chị Hiền = quyền quyết định cao nhất (CHỦ):** quyết + duyệt mọi thay đổi; vận hành hằng ngày — viết · nạp nguồn · carousel · cập nhật **DATA brand của chị** (voice · hồ sơ khách · pillars · kho chuyện · notion-config).
- **Kỹ sư (anh Tuấn + em) = THI CÔNG lõi hệ thống** (SKILL · luật · format · gate · công thức) **theo quyết định của chị** — sửa **từng file, có kiểm soát** (chống loạn bản).
- **Gặp lỗi / Reelo làm sai** → ghi 1 dòng vào `SO-LOI-REELO.md` → kỹ sư xử → gửi chị bản mới.

## 📖 Đọc thêm khi cần (không phải mỗi phiên)
`README.md` (dùng hằng ngày) · `HUONG-DAN-KE-HOACH-NOI-DUNG.md` (kế hoạch 30 ngày) · `SOP-MASTER.md` (tổng quan 7 chặng) · `.claude/skills/viet-script/SKILL.md` (quy trình viết) · `00-BAT-DAU-TU-DAY.md` (máy mới).
**Lệnh nhanh:** `viết reel / video dài / carousel <link>` · `tìm video từ kênh @<user>` → `chạy batch`.

---

## 📋 ĐỐI CHIẾU — 6 điểm đã vá (cho kỹ sư kiểm)

| # | Bản gọn của Tuấn | Đã vá thế nào | Neo gốc |
|---|---|---|---|
| 1 🚩 | Google Drive để "BẮT BUỘC" + "IF thiếu THEN DỪNG hệ thống" | Sửa: Drive là connector THÊM, **chỉ `/nap-insight` dừng, phần còn lại vẫn chạy** | gốc dòng 16 |
| 2 🚩 | Mất luật phân vai | Thêm lại mục 4 — **theo hướng mới: chị Hiền quyền cao nhất (quyết/duyệt) · kỹ sư thi công lõi** | gốc dòng 37–40 (Tuấn chỉnh) |
| 3 🟡 | Mất "kết luận trước, không ba hoa" | Thêm vào Luật thép #1 | gốc dòng 28 |
| 4 🟡 | Luật 3 Lớp mất thư mục thật | Giữ đủ: RAW/WIKI/OUTPUT = đường dẫn thật | gốc dòng 35 |
| 5 🟡 | Bỏ trắng "đây là gì" + cách dùng + cửa đọc | Giữ gọn: "Reelo là gì" + mục "Đọc thêm khi cần" trỏ file | gốc dòng 6–10, 19–25, 42–46 |
| 6 🔵 | Còn citation `[4][7]…` | Bỏ sạch (rác công cụ) | — |

**Còn giữ nguyên các luật gốc:** chống bịa · tiếng Việt · transcript chỉ tokscript · tiêu đề là vua · chiến lược trước · 3 lớp · nén trí nhớ · 🔁 NHẮC LẶP.

---
---

# ĐỢT 2 — viet-script/SKILL.md (REVIEW + ĐỀ XUẤT — chờ kỹ sư quyết)

> 🟡 **REVIEW.** Tuấn đã soạn bản gọn (checklist-hóa, giảm ~50%). Vịt Máy (kỹ sư) gác cổng phát hiện **mất ~6 gate**. **CHƯA dán đè `viet-script/SKILL.md` gốc (289 dòng).**
> **Bối cảnh:** đây là file **mật độ luật cao nhất** — mỗi cụm là 1 gate chống 1 lỗi đã từng mắc.

## A. Đánh giá tổng
- **Khung checklist của Tuấn: TỐT** — giữ đúng xương (5 bước + 5 khối GATE + Critic loop UNTIL ĐẠT). Sắc, dễ đối chiếu.
- **Vấn đề:** bản gọn **XÓA THẲNG** ~6 gate thay vì **đẩy xuống `references/` + trỏ tới**. Nhiều gate hiện **nằm inline trong SKILL.md, chưa có file reference riêng** → xóa khỏi đây = **mất hẳn**.

## B. 🚩 6 gate ĐỎ bị mất (mất năng lực / chống lỗi)

| # | Bị xóa | Hậu quả | Dòng gốc | Đã có reference? |
|---|---|---|---|---|
| 1 | **Chế độ BATCH + TÌM VIDEO** (quét kênh → chạy hàng loạt) | Mất năng lực "tìm video từ kênh → chạy batch" đang dùng | 44–51 | ✅ `che-do-batch.md` + `che-do-tim-video.md` → **chỉ cần TRỎ** |
| 2 | **Định dạng số 6 "Chắt lọc nguyên bản"** (bám gốc 100%) | Router `viet-bai` có menu **6** → SKILL không xử số 6 = lỗi | 165–169 | ❌ inline → cần giữ/tách |
| 3 | **GHÉP 2 NGUỒN (Hồ sơ×Kho) + CÂU LÕI "không phải X mà Y"** | 🩸 **TIM chất lượng bài** — bỏ thì bài rỗng (mất "chạm + sâu") | 170–177 | ❌ inline → **PHẢI tách reference** |
| 4 | **GATE FIT — Value Map** (chỉ hứa cái Hiền làm được) | Mất chống-bịa-offer; dễ hứa sản phẩm chưa có | 119,174 | ❌ inline |
| 5 | **RANH GIỚI TỰ NGHĨ** (được nghĩ gì / cấm chế gì) | Mất gate chống bịa cốt khi kho mỏng | 178 | ❌ inline |
| 6 | **Gate 05 Contrarian + cấm lạm 01/02/05** | Lỗi **tái diễn nhiều lần** — bỏ gate = quay lại | 193,204–206 | ❌ inline |

## C. 🟡 Vàng (mất chi tiết — nên đưa xuống reference)
Cửa 3 nạp (chuyện Hiền → `kho-cau-chuyen` A/B) · **cơ chế KHO SỐNG** (rút power-words/kho-hook 1–2/video) · **chặn nạp trùng** (nhãn ≥6 wiki) + tự archive wiki · **Quy tắc viết 7 điều** (dịch từ mượn routine→nếp · nhất quán xưng hô) · **giọng Reel-văn-nói vs Bài-văn-viết** (phân nhánh).

## D. Gốc vấn đề + nguyên tắc đúng
> **Lean file lõi = ĐẨY luật xuống `references/` + TRỎ tới. KHÔNG xóa.**

Bản gọn hiện **xóa** luật. 6 cụm đỏ (trừ #1 đã có reference) đang **inline, chưa có nơi khác chứa** → xóa = bốc hơi.

## E. Đề xuất cách làm (giữ công của Tuấn, 0 luật bốc hơi)
1. **Giữ nguyên khung checklist** của Tuấn (xương tốt).
2. **Chèn lại 6 gate đỏ** dưới dạng checklist ngắn + **trỏ file** (không nhồi chi tiết vào SKILL).
3. **TÁCH** các cụm luật lớn ra reference mới, SKILL chỉ trỏ:
   - `references/luat-viet-cot-loi.md` ← ghép-2-nguồn + câu lõi + GATE FIT + ranh-giới-chống-bịa (#3,4,5).
   - `references/luat-format-da-dang.md` ← gate 05 + cấm lạm 01/02/05 + map nhóm phễu (#6).
   - Số 6 (#2) + Kho sống + chặn trùng: giữ checklist ngắn trong SKILL (nhẹ) hoặc gộp vào reference trên.
→ Kết quả: SKILL.md vẫn gọn ~50%, **đủ đạn**.

## F. ⚖️ QUYẾT ĐỊNH CẦN KỸ SƯ CHỐT
1. Đồng ý nguyên tắc **"đẩy xuống reference, KHÔNG xóa"** (thay vì dán đè bản xóa-luật)?
2. Duyệt **tách 2 reference mới** (`luat-viet-cot-loi.md` + `luat-format-da-dang.md`)?
3. Cho Vịt Máy **ráp bản SKILL.md checklist đúng + 2 reference** (bỏ file nháp, chưa đè gốc)?

> ⚠️ **Khuyến nghị kỹ sư: KHÔNG dán đè bản gọn hiện tại** — sẽ mất 6 gate, Reelo viết bài kém đi + tái phát lỗi cũ (nhất là #3 tim chất lượng, #6 gate 05).
