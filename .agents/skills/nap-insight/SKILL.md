---
name: nap-insight
description: Nạp insight từ máy quét (Data Miner trên Google Drive) vào hồ sơ khách. Khi người dùng gõ /nap-insight — dùng Google Drive Connector tìm + đọc 3 file (insights-pack_v1.md, insights-pack_v2.md, phan-tich-toan-dien.md), trích Nỗi đau (Pains, đặc biệt Meta-Pains: Time poverty · Reputation risk · sợ AI thay thế · smokescreen) + Mong muốn ẩn (Gains) + Lệnh cấu hình (Mode, Visual), rồi MERGE vào ho-so-khach-hang.md của brand hiện tại (chống trùng, không đè dữ liệu cũ, có backup). Dùng khi gõ /nap-insight hoặc "nạp insight", "nạp dữ liệu máy quét".
---

# /nap-insight — NẠP INSIGHT TỪ MÁY QUÉT (Drive → hồ sơ khách)

Nạp tinh hoa insight (Pains/Gains/Config) từ Data Miner trên Google Drive vào `ho-so-khach-hang.md`. **KHÔNG viết content** — chỉ nạp dữ liệu đạn dược.

## BƯỚC 0 — ĐIỀU KIỆN + HÀNG RÀO (bắt buộc, trước mọi thứ)
1. 🔴 **Kiểm Google Drive Connector** đã nối chưa. **CHƯA nối → DỪNG, báo:** *"Cần nối Google Drive Connector để chạy /nap-insight. Hướng dẫn nối ở README.md (mục Cài đặt 3 bước)."* (Reelo điều kiện gốc chỉ có tokscript + Notion — Drive là connector THÊM cho lệnh này.)
2. Xác định **brand hiện tại** (nếu `_private/brand/` chỉ có 1 brand thì lấy brand đó; nhiều brand thì HỎI) → đích ghi: `_private/brand/<brand>/ho-so-khach-hang.md`.

## BƯỚC 1 — TÌM + ĐỌC 3 FILE (chống đọc nhầm bản)
Dùng Drive `search_files` tìm theo tên:
- `insights-pack_v1.md`, `insights-pack_v2.md`, `phan-tich-toan-dien.md`.
- 🔴 **CHỐNG TRÙNG TÊN (các file này có NHIỀU bản ở nhiều folder/version):** nếu >1 kết quả cùng tên → **chọn bản `modifiedTime` MỚI NHẤT** + **BÁO RÕ id + ngày sửa của file đã đọc** (provenance — để người dùng kiểm). Nếu lệch nhiều bản gây phân vân (vd có cả v6/v7 mới hơn v1/v2) → **hỏi người dùng chọn 1 lần** trước khi đọc.
- Đọc nội dung 3 file (Drive `read_file_content`). Không lấy được file nào → báo, bỏ qua file đó (không bịa nội dung).

## BƯỚC 2 — TRÍCH INSIGHT (chỉ lấy cái CÓ THẬT trong file)
- **Từ `phan-tich-toan-dien.md` → PAINS cực đắt**, đặc biệt **Meta-Pains**: *Time poverty · Reputation risk · sợ AI thay thế · smokescreen* (+ pain đắt khác nếu có).
- **Từ `insights-pack_v1/v2.md` → GAINS (mong muốn ẩn)** + **Lệnh cấu hình** (Mode, Visual).
- Mỗi insight giữ **nguyên ý gốc** + ghi **nguồn** (file + ngày). 🔴 KHÔNG tự chế pain/gain ngoài file (chống bịa).

## BƯỚC 3 — MERGE VÀO ho-so-khach-hang.md (AN TOÀN)
1. 🔴 **BACKUP TRƯỚC:** copy `ho-so-khach-hang.md` → `_backup/nap-insight-<ngày>/`. (Đây là file giàu: 48 pain + PAIN×JOB×GAIN + Value Map — không được làm hỏng.)
2. **Map insight vào ĐÚNG NHÓM có sẵn** (vd: *Kinh doanh kiệt sức* → nhóm 5 Tâm lý / 9 Cuộc sống · *Gia đình gồng gánh* → nhóm 10 Gia đình). Không có nhóm khớp → tạo mục "Insight từ máy quét (ngày)".
3. 🔴 **CHỐNG TRÙNG — không đè dữ liệu cũ:** trước khi chèn 1 insight, **so với nội dung đã có** (ý tương đương = bỏ qua, không chèn lại). Chỉ **CHÈN cái MỚI** (append vào nhóm), KHÔNG xóa/ghi đè dòng cũ.
3.5. 🔴🔴 **SUPERSESSION — GHI ĐÈ KHI HÀNH VI DỊCH CHUYỂN (kỹ sư chốt 2026-06-25, KHÔNG append máy móc):** với mỗi insight mới, so với insight cũ cùng chủ đề: nếu phát hiện **dịch chuyển hành vi** — insight cũ **đã lạc hậu / MÂU THUẪN** với insight mới (vd cũ: "khách sợ dùng công nghệ" → mới: "khách đã quen công nghệ, giờ sợ bị AI thay") → **KHÔNG chỉ cộng thêm.** Thay vào đó:
   - **Archive nỗi đau cũ** (gạch bỏ, chuyển xuống mục *"⚰️ Nỗi đau đã thay thế (archive)"* trong file — GIỮ VẾT, không xóa hẳn) + ghi *"thay bởi [insight mới], ngày, vì sao"*.
   - **Đưa nỗi đau mới lên** thay chỗ.
   - 🔴 **TRÌNH cho người duyệt TRƯỚC khi ghi đè** (đây là thay đổi chân dung khách — rủi ro): nêu rõ "Cũ [X] có vẻ lạc hậu/mâu thuẫn với mới [Y] → đề xuất archive cũ, thay mới. Đồng ý?". Người dùng gật mới đè. KHÔNG tự ý gạch nỗi đau cũ.
   - Phân biệt: insight mới **BỔ SUNG** (cũ vẫn đúng) → append (mục 3); insight mới **THAY THẾ** (cũ sai/lạc) → supersession (mục này).
4. **TRÌNH TÓM TẮT trước khi ghi cuối:** "Sẽ chèn N insight mới (X pains, Y gains) vào nhóm […]; bỏ Z cái trùng." → ghi. *(Người dùng có thể chặn nếu thấy sai.)*
5. Ghi nguồn cuối mục chèn: *(nạp từ máy quét — [tên file] [ngày])*.

## BƯỚC 4 — THÔNG BÁO
> **"Đã nạp thành công [N] insight mới từ máy quét. Kho đạn dược đã sẵn sàng! 💪"**
- Kèm 1 dòng: đã đọc file nào (id/ngày) · chèn vào nhóm nào · bỏ bao nhiêu trùng · backup ở đâu.

## Ràng buộc
- Markdown thuần + dùng Google Drive MCP (connector, KHÔNG script ngoài). Không cài/chạy gì.
- An toàn mặc định: backup trước · chống trùng · không đè cũ · provenance rõ. Mọi bước lùi được qua `_backup/`.
- 🗂️ **Đồng bộ LLM Wiki Pattern (provenance = `Sources:`):** mỗi insight nạp phải **truy ngược được nguồn gốc** (tên file + id + ngày sửa — đúng tinh thần `Sources:` trích ngược RAW) và **giữ NGUYÊN VĂN ý gốc, không bóp méo**. Đây là cùng luật "không bịa + truy nguồn" của hệ tri thức (xem AGENTS.md mục 🗂️).
