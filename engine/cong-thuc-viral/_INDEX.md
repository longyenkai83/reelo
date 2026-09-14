# Kho công thức viral — Hệ thống content tâm lý hành vi

Tài sản lõi của hệ thống, tách rời chủ đề, áp được **mọi ngành**. Nền tảng là tâm lý hành vi.
Nguồn gốc: phân tích video viral + framework hook của anh Tuấn + nội dung gốc đã bóc.

## Kiến trúc 6 tầng (đọc theo thứ tự khi viết)

| Tầng | File | Vai trò |
|---|---|---|
| 0. GATE | [psychology-gate.md](psychology-gate.md) | 3 câu hỏi bắt buộc + 3 công cụ + mẫu Brand Profile. 🔴 Câu 1 phải trả lời bằng **MỘT NGƯỜI**, không phải một nhóm |
| 1. Móng | [nguyen-ly-tam-ly.md](nguyen-ly-tam-ly.md) | 7 nguyên lý tâm lý hành vi (vì sao não phản ứng) |
| 2. **TIÊU ĐỀ** | [bo-tieu-de.md](bo-tieu-de.md) | 19 khung tiêu đề, mỗi khung neo 1 nguyên lý tâm lý · luật NHẮM MỘT NGƯỜI · chống lẫn 3 bảng phân loại |
| 3. Hook | [hook-system.md](hook-system.md) | 4 tiêu chí · 10 công thức × thị trường · 4 công thức câu mở (CM1–CM4) · 6 Story Locks · 3 hook aligned · checklist |
| 4. Thân | [story-structures.md](story-structures.md) | 3 cấu trúc kể chuyện ngắn (theo loại nội dung) |
| 5. Đầu ra | [dinh-dang-dau-ra.md](dinh-dang-dau-ra.md) | Reel / Video dài / Bài viết ngắn |

> 🔴 **TIÊU ĐỀ là TẦNG, không phải file phụ trợ** *(nâng hạng 2026-08-06)*. Tiêu đề là thứ người ta gặp **TRƯỚC KHI BẤM** — hook có hay tới đâu cũng vô nghĩa nếu không ai bấm vào. Xếp nó xuống hàng vệ tinh là bỏ trống đúng cửa đầu tiên.
> **Ba bảng phân loại KHÁC NHAU — mỗi cột chỉ nhận giá trị từ đúng bảng của nó:**
> | Bảng | Ở đâu | Ví dụ giá trị hợp lệ |
> |---|---|---|
> | **Nguyên lý tâm lý** (7) | `nguyen-ly-tam-ly.md` | Reframe phản trực giác · Vòng lặp chưa đóng · **Khung số đóng** |
> | **Khung tiêu đề** (19) | `bo-tieu-de.md` | **SỐ 1–19**, hoặc ghi thẳng chữ `TỰ CHẾ` |
> | **Trục bài** (6) | `cong-kiem-chat-luong.md` Lớp 2 | **nghịch lý** · ẩn dụ · **hình ảnh cụ thể** · câu hỏi · tuyên ngôn · contrast |
> Điền tên bảng này sang cột bảng kia là lỗi hay gặp nhất — *"Khung số đóng"* là **nguyên lý**, *"Nghịch lý"* là **trục**, cả hai đều KHÔNG phải khung tiêu đề.

*(Lớp ngôn ngữ tiếng Việt nằm ở `.claude/skills/viet-script/vietnamese-language-layer.md` — áp ở bước rà.)*

## File vệ tinh (phụ trợ — cùng thư mục)
- `cong-kiem-chat-luong.md` — 🔴 **cổng KIỂM chất lượng (chặng 4) — NGUỒN SỰ THẬT của mọi rubric.** File khác mô tả lại rubric thì đó là bản mirror; lệch nhau thì **file này thắng**
- `checklist-hook.md` — chấm & lọc hook (1 lớp của cổng KIỂM, mirror của Lớp 3 phần hook)
- `kho-hook.md` — kho hook thật để nhái (nguyên liệu, không phải luật)
- `khung-7-khuc-ke-chuyen.md` — khung kể chuyện dài (mở rộng của tầng 4)
- `chien-luoc-content.md` — chiến lược 30 ngày (nhóm/tầng/giai đoạn/pillar)
- `mau-brand/` — form trắng để setup brand mới
- `_private/brand/<brand>/` — hồ sơ thương hiệu (lớp riêng, KHÔNG nằm trong bản bán)

## Chống mâu thuẫn nội bộ (luật 2026-08-06)
Một khái niệm chỉ có **một nguồn sự thật**. Nhiều file cùng nói về một thứ thì phải khai rõ file nào là gốc, file nào là bản mirror.
| Khái niệm | Nguồn sự thật | Bản mirror (phải khớp, lệch thì gốc thắng) |
|---|---|---|
| Rubric chấm bài | `cong-kiem-chat-luong.md` | `.claude/agents/critic-ban-giam-khao.md` · `checklist-hook.md` |
| Công thức hook | `hook-system.md` mục B | `kho-hook.md` (chỉ là ví dụ, không định nghĩa) |
| Khung tiêu đề | `bo-tieu-de.md` | — |
| Nguyên lý tâm lý | `nguyen-ly-tam-ly.md` | — |
> Sửa nguồn sự thật thì **phải rà bản mirror ngay trong lượt đó**. Hai file cùng ra luật cho một việc mà không ai là gốc — đó là cách mâu thuẫn sống sót nhiều tháng không ai thấy.

## Triết lý dùng kho
1. **Chọn theo VẤN ĐỀ, không theo chủ đề.** Đầu vào là nỗi đau của nhóm đối tượng (GATE câu 2) → chọn nguyên lý → đẻ hook.
2. **Công thức = khung rỗng**, điền nội dung ngành nào cũng được.
3. **Contrast (tương phản) là cơ chế gốc** của mọi hook mạnh.
4. **Công cụ phân tích viral là giàn giáo tạm.** Đủ giàu → ngắt, viết bằng kho này.

## Quy tắc
- Chỉ ghi cái có **bằng chứng thật**. Trùng → thêm ví dụ vào file cũ, không tạo file mới.
- Thêm nguyên lý/công thức mới chỉ khi nó **lặp ở 2+ nguồn**.

*Cập nhật: 2026-08-06 — nâng TIÊU ĐỀ lên tầng 2 (kiến trúc 6 tầng) · khoá 3 bảng phân loại · thêm luật một-nguồn-sự-thật · gỡ dữ liệu riêng của brand khỏi engine.*
