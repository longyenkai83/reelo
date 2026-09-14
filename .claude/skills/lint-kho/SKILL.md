---
name: lint-kho
description: Bảo trì sức khỏe kho kiến thức (raw + wiki) theo phương pháp Karpathy LLM-Wiki. Gọi khi muốn audit định kỳ — tìm trùng · mâu thuẫn · trang mồ côi · khái niệm thiếu trang · nguồn cạn/stale · vệ sinh cột KT. CHỈ BÁO CÁO + đề xuất, KHÔNG tự sửa (chờ Tuấn duyệt).
---

# /lint-kho — Kiểm tra sức khỏe kho (Karpathy Lint)

> **Vì sao:** data lớn dần → nếu không bảo trì sẽ loạn (trùng, mâu thuẫn, nguồn nạp rồi không ai dùng). Karpathy gọi đây là **Lint**: định kỳ để LLM tự dọn thứ người lười làm.
> **Nguyên tắc AN TOÀN:** skill này CHỈ QUÉT + BÁO CÁO + ĐỀ XUẤT. TUYỆT ĐỐI không tự xóa/gộp/sửa — Tuấn duyệt từng mục rồi mới thi công (backup trước).

## KHI GỌI — phái vịt con (subagent, ưu tiên Fable) quét kho

**Phạm vi mặc định:** `_private/kho-kien-thuc/` (raw + wiki + wiki/_INDEX). Nếu Tuấn nói "lint nhãn X" → chỉ nhãn đó.
**Đọc trước:** `wiki/_INDEX.md` (danh mục + cột KT) · `scripts-output/_INDEX.md` (bài đã viết, để đối chiếu khai thác).

## 6 HẠNG MỤC AUDIT (checklist Karpathy)

1. **🔗 Trang mồ côi (orphan):**
   - RAW nào KHÔNG có WIKI tương ứng (nạp rồi bỏ quên, chưa chắt)?
   - WIKI nào KHÔNG được bài nào / wiki nào link tới (không ai dùng)?
2. **♻️ Trùng lặp:** 2+ wiki cùng nhãn nội dung gần trùng → đề xuất GỘP (giữ cái đầy hơn).
3. **⚔️ Mâu thuẫn:** 2 wiki nói NGƯỢC nhau về cùng 1 điểm → nêu cả 2 + hỏi cái nào đúng.
4. **🕳️ Khái niệm thiếu trang:** khái niệm được nhắc nhiều lần trong các wiki mà CHƯA có wiki/mục riêng → đề xuất tạo.
5. **🌾 Nguồn cạn / stale:**
   - Wiki có mục `## 🗺️ KHAI THÁC` mà TẤT CẢ góc đã ✅ → đề xuất **archive** (`wiki/_archive/`).
   - Wiki quá cũ / kiến thức lỗi thời → gắn cờ xem lại.
6. **🧹 Vệ sinh cột KT + mục KHAI THÁC:**
   - Wiki nào THIẾU mục `## 🗺️ KHAI THÁC` (theo gate mới)?
   - Cột KT ở `_INDEX` có khớp thực tế bài đã viết không (đối chiếu `scripts-output/_INDEX`)?
   - Wiki nào có CẢ "Bản đồ khai thác" cũ LẪN "KHAI THÁC" mới (dư) → đề xuất gộp.

## OUTPUT — báo cáo phân mức
Trả bảng theo mức ưu tiên:
- 🔴 **CẦN XỬ** (mâu thuẫn thật · orphan nhiều · trùng nặng) — Tuấn nên quyết sớm.
- 🟡 **NÊN XEM** (nguồn cạn nên archive · concept thiếu trang · KT lệch).
- 🟢 **ỔN** (số liệu tổng: bao nhiêu raw/wiki, bao nhiêu đã khai thác).

Mỗi mục: nêu FILE cụ thể + vấn đề 1 dòng + đề xuất hành động. 🔴 **KHÔNG bịa** — chỉ báo cái đối chiếu được thật; không chắc thì ghi "cần xem tay".

## SAU BÁO CÁO
Trình Tuấn → Tuấn chọn mục nào dọn → **backup → thi công từng mục có kiểm soát** (phân vai kỹ sư). Ghi 1 dòng vào `NHAT-KY-PHIEN.md` (đã lint gì, dọn gì).

> **Nhịp đề xuất:** chạy `/lint-kho` mỗi ~2-4 tuần hoặc sau mỗi đợt nạp nhiều nguồn.
