### 🗺️ BẢN ĐỒ KIẾN TRÚC & QUY TRÌNH REELO (SOP MASTER)
Reelo chia làm 2 lớp: **LÕI CHUNG** (nhân bản cho mọi brand: quy trình, cổng kiểm, hook) và **LỚP RIÊNG** (chứa trong `_private/brand/`: hồ sơ, voice, pillar).

#### 1. QUY TRÌNH 7 CHẶNG (END-TO-END)
* **0. GATE:** ① Soi chiến lược (chiến dịch 🟢 ĐANG CHẠY → ma trận → bài phục vụ job/sản phẩm nào theo pipeline 5 bước) + ② GATE 5 câu (Ai? · Trăn trở gì? · Vì sao chọn brand? · Cảm xúc bốc cao? · Đòn bẩy share?).
* **1. THU (3 Cửa Nạp):** Video đa nền tảng (tokscript) / Nguồn ngoài (Notion/Text) / Chuyện chuyên môn (từ Hiền).
* **2. LẤY & DỌN:** Trích xuất Transcript → Lưu `RAW/` (chỉ giữ YAML pointer) → Vét cạn ý đắt lập mindmap tại `Wiki/`.
* **3. VIẾT (Trái tim hệ thống):** Chọn Tầng/Giai đoạn → Chọn Nguyên lý tâm lý → Đẻ ≥8 Hook → Chọn Khung Tiêu Đề → Chốt Format → Viết dàn ý → Viết nháp.
* **4. KIỂM (Cổng chất lượng):** Lớp 1 (Chống bịa - VETO) · Lớp 2 (Giọng AI & nhạc tính) · Lớp 3 (Hook/Tiêu đề) · Lớp 6 (Độ tươi). Cổng bằng chứng trước khi chấm; bài quan trọng → Tòa án 4 người. *(Lớp 4/5b chờ GĐ2, đủ ≥5 mẫu giọng.)*
* **5. DUYỆT:** Ban giám khảo (Critic) chấm điểm `VERDICT=ĐẠT` → Người dùng duyệt.
* **6. HỌC:** Tích lũy bài duyệt tốt vào `mau-giong-chuan/` để hội tụ voice.
* **7. XUẤT:** Lưu file vào `scripts-output/` hoặc `carousel-output/` → Đẩy Notion.

#### 2. CHIẾN LƯỢC CONTENT & ĐỊNH DẠNG
* **4 Tuyến Phễu (Dynamic Funnel):** Lạnh (ToFu) → Ấm (MoFu) → Nóng (BoFu) → Bán. Tương ứng với 28 khung tiêu đề.
* **3 Định dạng đầu ra:** Reel (văn nói, chạm nhanh) · Video dài (kịch bản 6 bước sâu) · Carousel (cô đọng).
* **17 Format thân bài (5 Nhóm chống lặp):** Cấu trúc (A) · Kể chuyện (B) · Copywriting (C) · Hook (D) · Nâng cao (E).

#### 3. BỘ NÃO HỆ THỐNG (TRA CỨU NHANH)
* Lõi thi công AI: `.claude/skills/viet-script/SKILL.md`
* Cổng kiểm duyệt: `engine/cong-thuc-viral/cong-kiem-chat-luong.md`
* Luật ngôn ngữ: `_private/brand/<brand>/writing-rules.md`
* Chiến lược Phễu/Format: `engine/cong-thuc-viral/chien-luoc-content.md`
