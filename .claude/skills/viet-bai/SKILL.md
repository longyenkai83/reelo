---
name: viet-bai
description: CỬA NGÕ DUY NHẤT để viết content (Router). Kích hoạt khi người dùng gõ /viet-bai HOẶC các cụm tự nhiên: "viết bài", "tạo content", "làm content", "viết script", "viết nội dung", "viết reel/bài ngắn/bài dài/video dài/carousel", kèm link/yêu cầu. Hiển thị danh sách đánh số 1–5 hỏi định dạng đầu ra (Reel · Bài ngắn · Bài dài · Video dài · Carousel), KHÔNG tự viết ngay. Sau khi người dùng chọn số, route lệnh + toàn bộ ngữ cảnh về skill lõi viet-script (backend) để thi công: bóc băng → viết → Ban Giám Khảo critic (xuất khi VERDICT=ĐẠT).
---

# /viet-bai — CỔNG CHUYỂN HƯỚNG (Router)

Skill này **chỉ làm 2 việc**: (1) hỏi định dạng, (2) trỏ về skill lõi `viet-script`. **KHÔNG tự bóc băng/viết** — đó là việc của `viet-script`.

## BƯỚC 1 — HIỂN THỊ MENU (KHÔNG tự viết ngay)
Người dùng gõ `/viet-bai [link hoặc yêu cầu]`. 🔴 **KHÔNG viết Reel/bài ngay.** Trước hết **IN DANH SÁCH ĐÁNH SỐ** (text thuần — 🔴 **TUYỆT ĐỐI KHÔNG dùng công cụ AskUserQuestion**):

> **Bạn muốn làm định dạng nào? (gõ số)**
> 1. **Reel** — 210–240 chữ · văn nói (mặc định)
> 2. **Bài ngắn** — 200–400 chữ · văn viết (post FB/blog ngắn)
> 3. **Bài dài** — 400–800 chữ · kể chuyện sâu
> 4. **Video dài** — kịch bản 6 bước (bám gốc)
> 5. **Carousel** — slide ảnh (4 công thức)
> 6. **Chắt lọc nguyên bản** — giữ nguyên ý tác giả, không chế biến, không thêm chuyện cá nhân (chỉ chuyển ngữ thành văn nói tiếng Việt + sắp mượt + ghi nguồn)

- Nếu người dùng đưa link/yêu cầu kèm `/viet-bai` → **GIỮ NGUYÊN** ngữ cảnh đó, chờ họ chọn số (đừng hỏi lại link).
- Người dùng gõ số ngoài 1–6 / chưa rõ → hỏi lại gọn 1 lần.

## BƯỚC 2 — ROUTE VỀ `viet-script` (sau khi chọn số)
Người dùng gõ số → xác định định dạng → **chuyển giao cho skill lõi `viet-script`** kèm **toàn bộ ngữ cảnh**:
- **Định dạng đã chọn** (1 Reel / 2 Bài ngắn / 3 Bài dài / 4 Video dài / 5 Carousel / **6 Chắt lọc nguyên bản**).
  - 🔴 **Số 6 (Chắt lọc nguyên bản):** báo `viet-script` bật **CHẾ ĐỘ BÁM GỐC** — TẮT thêm chuyện cá nhân · VÔ HIỆU luật ghép 2 nguồn · không đẻ hook/format sáng tạo. Chỉ chuyển ngữ thành văn nói tiếng Việt + sắp mượt + ghi nguồn (xem viet-script mục "CHẾ ĐỘ CHẮT LỌC NGUYÊN BẢN").
- **Link / yêu cầu / text gốc** người dùng đưa.

→ Từ đây **`viet-script` điều khiển**: chạy QUY TRÌNH (Bước 0 GATE → bóc băng raw→wiki → **🔴 SOI MA TRẬN 30 ngày: xếp link vào ô trống khớp Pillar+Giai đoạn, in thông báo "Đã xếp vào Pillar [X], Giai đoạn [Y], Format [Z]"** → GATE FIT Value Map → viết theo luật định dạng đã chọn → cổng kiểm → **Hàng rào Critic `critic-ban-giam-khao` (chỉ xuất khi VERDICT=ĐẠT)** → trình). Áp đúng **LUẬT TỪNG LUỒNG ĐỊNH DẠNG** trong `viet-script/SKILL.md`.

> **Quan hệ skill:** `viet-bai` = router mỏng (hỏi + trỏ). `viet-script` = lõi thực thi (mọi luật viết, format, gate, critic ở đó — 1 nguồn sự thật). Router KHÔNG nhân đôi luật viết.

## Ràng buộc
- Markdown thuần, không script. Việc duy nhất: hỏi định dạng → trỏ ngữ cảnh sang `viet-script`.
- Lệnh tắt cũ vẫn chạy thẳng (bỏ menu): "viết reel/bài ngắn/bài dài/video dài/carousel `<link>`" → vào luôn luồng đó qua `viet-script`.
