---
name: don-kho
description: Kiểm tra sức khỏe Kho tri thức (Knowledge Base Health Check). Khi người dùng gõ /don-kho hoặc "dọn kho" — đóng vai Thủ thư: quét _private/kho-kien-thuc/wiki/, phát hiện wiki TRÙNG chủ đề (đề xuất gộp), file rác/rỗng, liên kết [[wikilink]] gãy, và cập nhật wiki/_INDEX.md. Markdown thuần, KHÔNG script. 🔴 AN TOÀN: chỉ ĐỀ XUẤT gộp/archive/xóa → NGƯỜI DUYỆT mới làm; archive-first, KHÔNG tự xóa file.
---

# /don-kho — THỦ THƯ KHO TRI THỨC (Health Check)

> Đóng vai **Thủ thư**: giữ kho `wiki/` gọn, không trùng, không rác, link không gãy. **Markdown thuần, KHÔNG script.**
> 🔴🔴 **LUẬT AN TOÀN TỐI THƯỢNG:** skill này **CHỈ QUÉT + ĐỀ XUẤT**. Mọi gộp/archive/xóa phải **người duyệt mới làm**, **archive-first** (chuyển `wiki/_archive/`, KHÔNG xóa hẳn). Xóa file = HỎI duyệt TỪNG cái. Đúng luật cứng "không xóa file, không gộp/đập hàng loạt".

## BƯỚC 1 — QUÉT (chỉ đọc)
- Liệt kê toàn bộ `_private/kho-kien-thuc/wiki/*.md` (trừ `_INDEX.md`, `_archive/`).
- Với mỗi file CHỈ quét **MẶT TIỀN (frontmatter)**: `title` · `chu-de` (nhãn) · 1 dòng ý chính ở đầu. 🔴 **TUYỆT ĐỐI KHÔNG chui đọc sâu ruột file** (BẢN ĐỒ KHAI THÁC / TẦNG INSIGHT...) ở bước quét — tránh ngốn token / tràn bộ nhớ. Việc đọc sâu (vd xác định file đã ✅ khai thác hết để archive) là **thao tác RIÊNG, chỉ chạy SAU khi người dùng duyệt đề xuất** (Bước 4).

## BƯỚC 2 — PHÁT HIỆN 4 LOẠI VẤN ĐỀ
1. **TRÙNG chủ đề:** ≥2 wiki cùng nhãn + ý chính gần nhau → ứng viên GỘP. (Vd nhiều wiki PTL cùng "bán qua vấn đề".)
2. **RÁC / RỖNG:** wiki thiếu nội dung thật, hoặc đã ✅ khai thác hết từ lâu (nên archive), hoặc trùng hẳn 1 wiki khác.
3. **LINK GÃY:** `[[wikilink]]` / `Sources: [[raw/...]]` trỏ tới file KHÔNG tồn tại.
4. **THIẾU CHUẨN:** wiki cũ thiếu YAML frontmatter / thiếu `Sources:` / thiếu BẢN ĐỒ KHAI THÁC.

## BƯỚC 3 — BÁO CÁO + ĐỀ XUẤT (KHÔNG tự làm)
In bảng cho từng vấn đề: *File · Loại vấn đề · Đề xuất xử lý*. Đề xuất theo thứ tự an toàn:
- **Gộp:** "Gộp [A]+[B] → 1 wiki concept giàu nguồn (giữ ĐỦ góc độc + ghi ĐỦ nguồn từng file)." → người duyệt.
- **Archive:** wiki đã ✅ khai thác hết / rác → đề xuất chuyển `wiki/_archive/` (giữ vết). **Raw GIỮ.**
- **Sửa link gãy:** trỏ về file đúng (nếu tìm được) HOẶC báo "nguồn mất".
- **Nâng chuẩn:** wiki thiếu YAML/Sources → đề xuất bổ sung (chỉ thêm cái truy được từ nguồn, KHÔNG bịa).
🔴 Mỗi đề xuất chờ **người duyệt gật** mới thực hiện.

## BƯỚC 4 — SAU KHI DUYỆT (mới được làm)
- **Backup trước** (`_backup/don-kho-<ngày>/`).
- Gộp/archive/sửa link **đúng cái đã duyệt** (archive-first).
- **Cập nhật `wiki/_INDEX.md`** cho khớp (bỏ dòng đã archive, gộp dòng trùng, thêm wiki mới). _INDEX = mục lục, cập nhật được; nhưng nội dung wiki thì chỉ động cái đã duyệt.
- Báo: đã gộp/archive/sửa gì · backup ở đâu.

## Ràng buộc
- Markdown thuần, KHÔNG script/không cài tool. Quét = đọc file qua công cụ Claude Code.
- 🔴 KHÔNG tự xóa/gộp/đập hàng loạt. Đề xuất → người duyệt → backup → làm từng cái. Mỗi mục trong kho phải có ích; cái loại bỏ thì archive (đảo ngược được), không xóa hẳn.
