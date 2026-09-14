---
name: review-chu-ky
description: Đánh giá chu kỳ content 30 ngày. Khi người dùng gõ /review-chu-ky hoặc "review chu kỳ" — đọc scripts-output/_INDEX.md + NHAT-KY-PHIEN.md, phân tích tỷ lệ phân bổ phễu (ToFu/MoFu/BoFu), phát hiện Format bị lạm dụng, đề xuất chiến lược chu kỳ tới. Markdown thuần, KHÔNG script — chỉ đọc + phân tích + báo cáo. KHÔNG sửa file nào.
---

# /review-chu-ky — SOI CHU KỲ CONTENT (System Review)

> Cuối mỗi chu kỳ 30 ngày (hoặc khi anh gõ "review chu kỳ") → soi lại đã làm gì, lệch đâu, chu kỳ tới đẩy gì. **Markdown thuần: chỉ ĐỌC + phân tích, KHÔNG sửa/xóa file.**

## BƯỚC 1 — ĐỌC DỮ LIỆU (không bịa, chỉ đếm cái có thật)
1. `scripts-output/_INDEX.md` — danh sách bài đã viết (định dạng · phễu/giai đoạn · pillar · format · nguồn).
2. `NHAT-KY-PHIEN.md` — mục tiêu chu kỳ, đã quyết/khóa, đang dở.
3. (Nếu có) `_private/brand/<brand>/ma-tran-30-ngay.md` — kế hoạch gốc để đối chiếu thực-tế vs kế-hoạch.
🔴 Chỉ thống kê từ dữ liệu THẬT trong file. Thiếu cột → ghi "chưa rõ", KHÔNG đoán số.

## BƯỚC 2 — PHÂN TÍCH (3 trục)
1. **Tỷ lệ phễu (ToFu/MoFu/BoFu):** đếm bài mỗi tầng → ra %. So với **mục tiêu chiến dịch** (Dynamic Ratio: Gieo 80/20/0 · Nuôi 30/60/10 · Thu 10/20/70). Lệch nhiều → gắn cờ.
2. **Format có bị lạm dụng?** đếm tần suất từng Format (1–17) + Nhóm (A–E). 🔴 Báo nếu **1 format/nhóm chiếm đa số** (vd 05 Contrarian > 1/4 số bài, hay toàn nhóm B). Đối chiếu LUẬT ĐA DẠNG NHÓM.
3. **Pillar phủ đều?** đếm bài mỗi Pillar (**P1–P4** — hệ 4 pillar chốt 2026-08-06, khớp cột `Pillar` trên Notion; xem `content-pillars.md`). Pillar nào bỏ trắng / pillar nào dồn quá → nêu. ⚠️ **P4 gánh 3 nhánh** (chuyện cá nhân · lối sống · chuyện học viên) nên tự phình — đừng đọc "P4 to" là "đã đa dạng".
4. **🎯 BẢNG ĐIỂM 4DX** — mở `_private/brand/<brand>/khung-4dx-facebook.md`: đối chiếu **KPI đòn bẩy** (việc mình làm được: số bài đăng · số DM · số comment trả lời) với thực tế chu kỳ. 🔴 Chấm **KPI đòn bẩy trước, WIG sau** — vì đòn bẩy là cái điều khiển được. Ô nào chưa có số thật → ghi `[chưa có số]`, **KHÔNG đoán**.
5. **🔄 TRỤC BÀI có lặp?** đếm cột **TRỤC** trong `_INDEX.md` (contrast · ẩn dụ · hình ảnh cụ thể · nghịch lý · tuyên ngôn · câu hỏi). 🔴 Báo cờ nếu **1 trục > 40%** — bệnh đã từng gặp: contrast+tuyên ngôn chiếm 70%.

## BƯỚC 3 — BÁO CÁO (bảng, gọn)
In bảng:
- **Tỷ lệ phễu thực tế** vs mục tiêu (cờ nếu lệch).
- **Top format/nhóm** + cảnh báo lạm dụng.
- **Pillar lệch** (trắng / dồn).
- **CTA có lặp khuôn?** (liếc 5 bài gần — cùng đuôi quá nhiều).

## BƯỚC 4 — ĐỀ XUẤT CHU KỲ TỚI
- Mục tiêu chu kỳ tới nên là gì (Gieo→Nuôi→Thu leo dần)? → gợi ý tỷ lệ Dynamic Ratio tương ứng.
- Format/nhóm nên ĐẨY (đang thiếu) · format nên GIẢM (đang lạm).
- Pillar cần bù.
- 🔴 Chỉ **ĐỀ XUẤT** — người dùng quyết. KHÔNG tự đổi ma trận/luật.

## BƯỚC 5 — ĐÓNG VÒNG ĐỜI CHIẾN DỊCH (thêm 2026-07-20 — bịt khoảng trống giữa review và chiến dịch kế)
> Trước đây hệ **không có luật nào** nói "hết 30 ngày thì file kế hoạch cũ đi đâu" → mỗi lần đổi chiến dịch phải cứu file thủ công, dễ quên.

- [ ] **Soi nhãn TRẠNG THÁI** ở đầu mọi file kế hoạch trong `_private/brand/<brand>/`. Chiến dịch nào **quá ngày kết thúc** mà vẫn mang `🟢 ĐANG CHẠY` → **gắn cờ NGAY** (đây là nguồn gây viết bài theo lịch chết).
- [ ] **TRÌNH ĐỀ XUẤT ĐÓNG** (KHÔNG tự làm — chờ người duyệt), gồm đúng 3 việc:
  1. Đổi nhãn `🟢 ĐANG CHẠY` → `⚫ HẾT HẠN (ngày…)`.
  2. Nêu **phần nào đáng CỨU** sang file nền trước khi archive *(số thật · offer · khung dùng lại được)* — nói rõ cứu về file nào.
  3. Chuyển vào `_archive/<ngày>-<tên-chiến-dịch>/` kèm **`_VI-SAO-ARCHIVE.md`** (lý do · đã cứu gì về đâu · cách hồi lại).
- [ ] **Kiểm mâu thuẫn tồn đọng:** grep xem còn file nào nhắc **đích cũ / offer đã bỏ / hệ pillar cũ** không. 🔴 *Bài học 2026-07-20: một file chiến lược cũ mang dòng "đọc file này TRƯỚC" nhưng trỏ về workshop đã bỏ — **file mâu thuẫn nguy hơn file mồ côi**.*
- [ ] **Đề xuất chiến dịch kế** tiếp nối chỗ đang nghẽn — **KHÔNG lặp lại 30 bài cũ** (theo `HUONG-DAN-KE-HOACH-NOI-DUNG.md`).

## Ràng buộc
- Markdown thuần, KHÔNG script. Chỉ đọc + phân tích + báo cáo. **KHÔNG tự sửa/xóa/di chuyển file** — Bước 5 chỉ **TRÌNH ĐỀ XUẤT**, người duyệt gật rồi mới làm.
- Số liệu chỉ từ file thật (chống bịa). Hết chu kỳ → gắn với nghi thức "review chu kỳ" trong `chien-luoc-content.md`.
