---
name: nap-chuyen
description: Nạp nhanh câu chuyện cá nhân / chuyên môn của brand vào kho độc quyền (E-bank cho EEAT). Kích hoạt khi người dùng gõ /nap-chuyen HOẶC nói TỰ NHIÊN (không cần gõ /): "nạp câu chuyện của chủ thể", "lưu câu chuyện của chị", "chuyện thật của chủ thể", "nạp chuyện", "chủ thể có câu chuyện này", "nạp chuyên môn của chị"... — kèm đoạn nội dung/câu chuyện. Tự đọc hiểu + PHÂN LOẠI (A) Chuyện thật (mốc/cảm xúc/hành trình cá nhân) hay (B) Chuyên môn lõi (phương pháp/bài học tự đúc kết), rồi chèn vào ĐÚNG mục trong _private/brand/<brand>/kho-cau-chuyen.md. Lưu NGUYÊN VĂN (chống bịa), backup trước, báo rõ chèn vào đâu. KHÔNG bắt người dùng tự chỉ định A/B. Markdown thuần.
---

# /nap-chuyen — NẠP CHUYỆN CÁ NHÂN (Cửa nạp số 3, không cần prompt dài)

> Người vận hành chỉ cần `/nap-chuyen` + dán đoạn nội dung → hệ thống tự lưu vào **kho độc quyền** `_private/brand/<brand>/kho-cau-chuyen.md`, tự phân loại A/B. **Markdown thuần, không script.**

## BƯỚC 0 — XÁC ĐỊNH BRAND + ĐỌC KHO
- Brand hiện tại (nếu `_private/brand/` chỉ có 1 brand thì lấy brand đó; nhiều brand thì HỎI) → đích: `_private/brand/<brand>/kho-cau-chuyen.md`.
- Đọc kho để biết cấu trúc 2 mục: **`## (A) CHUYỆN THẬT`** và **`## (B) CHUYÊN MÔN LÕI`** + các mục con đã có (để chèn nối tiếp, không phá).

## BƯỚC 1 — TỰ PHÂN LOẠI (A hay B) — KHÔNG bắt người dùng chỉ định
Đọc hiểu đoạn nạp, phân loại theo dấu hiệu:
- **(A) CHUYỆN THẬT** — có **mốc thời gian · cảm xúc · hành trình cá nhân · sự kiện đời** ("hồi trước mình…", "năm…", "lúc đó mình thấy…", trải nghiệm/bước ngoặt). → bằng chứng sống.
- **(B) CHUYÊN MÔN LÕI** — **phương pháp · khung · bài học · nguyên tắc tự đúc kết** ("cách làm…", "3 bước…", "nguyên tắc…", kiến thức brand tự dạy). → kiến thức độc quyền.
- 🔴 **Mơ hồ / lẫn cả 2** → HỎI người dùng 1 lần ("Đoạn này em xếp vào (A) chuyện thật hay (B) chuyên môn?") thay vì đoán sai. *(Có thể tách: phần kể → A, phần bài học → B.)*

## BƯỚC 2 — CHÈN VÀO ĐÚNG MỤC (AN TOÀN)
1. 🔴 **BACKUP TRƯỚC:** copy `kho-cau-chuyen.md` → `_backup/nap-chuyen-<ngày>/`.
2. **Chèn NỐI TIẾP** dưới mục đúng (A hoặc B), KHÔNG đè/xóa chuyện cũ:
   - **(A):** thêm `## Câu chuyện [N] — [tên ngắn]` với các trường: **Dữ kiện thật** (nguyên văn người dùng đưa) · Minh họa được insight (suy từ chuyện, không bịa) · Đã dùng: `[chưa]` · Cần bổ sung: `[nếu thiếu chi tiết]`.
   - **(B):** thêm mục chuyên môn (tên phương pháp + nội dung nguyên văn).
3. 🔴 **LƯU NGUYÊN VĂN — chống bịa:** giữ đúng lời người dùng. KHÔNG thêm số/cảm xúc/mốc/kết quả họ không nói. Thiếu chi tiết → `[cần bổ sung]` (theo quy tắc kho).
4. Ghi nguồn + ngày: *(nạp 2026-..-.. — chủ thể/anh Tuấn kể)*.

## BƯỚC 3 — BÁO CÁO
> *"Đã nạp vào kho chuyện — Phần [A/B], mục '[tên]'. Backup ở [đường dẫn]."*
- 1 dòng: phân loại A hay B + vì sao · chèn vào đâu · backup ở đâu · chỗ nào để `[cần bổ sung]`.

## Ràng buộc
- Markdown thuần, KHÔNG script/cài tool. Chỉ đọc + phân loại + ghi file (qua công cụ Claude Code).
- AN TOÀN: backup trước · chèn nối tiếp không đè cũ · lưu nguyên văn (chống bịa) · provenance rõ. Mọi bước lùi được qua `_backup/`.
