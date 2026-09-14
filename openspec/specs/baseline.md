# OpenSpec — KIẾN TRÚC LÕI REELO (Frozen Baseline)

**Ngày đóng băng:** 2026-07-22
**Mục đích:** Tài liệu "hiến pháp" lưu cấu trúc **bất biến** của hệ thống. `CLAUDE.md` + `SOP-MASTER.md` là file SỐNG để vận hành hằng ngày; file này là bản GỐC để đối chiếu. Chi tiết vận hành đầy đủ: `docs/CO-CHE-REELO.md`.
**Nguồn & kiểm chứng:** quét file thật ngày 2026-07-22 (2 subagent) + đối chiếu độc lập bằng Fable 5 (soi từng claim với `CLAUDE.md`, `SOP-MASTER.md`, `proposal.md`, `.claude/skills/*`, `critic-ban-giam-khao.md`, `cong-kiem-chat-luong.md`, `notion-config.md`, `.mcp.json`).

---

## 1. BẢN CHẤT HỆ THỐNG
Reelo là "Hệ Quản Trị Tri Thức Lũy Tiến" — biến nguồn (video, insight, chiến lược) thành content tiếng Việt **đúng giọng một thương hiệu cá nhân**, có chiến lược dẫn đường, sau đó đẩy lên Notion để duyệt và đăng.
**Đầu ra:** 5 định dạng (Reel · Bài ngắn · Bài dài văn viết · Video dài · Carousel) + 1 chế độ **Chắt lọc nguyên bản** (bám gốc 100%). Mỗi định dạng có luật độ dài riêng (Reel/Bài ngắn/Bài dài có trần chữ; Video dài có sàn ≥1000 chữ; Carousel tính theo slide).

## 2. NGUYÊN TẮC KIẾN TRÚC (5 cốt lõi)
- **NT1 (Project):** Reelo là một Project tự đủ, mọi skill nằm bên trong hệ thống.
- **NT2 (Tách Engine ↔ Brand):** tách rạch ròi `engine/` (công thức/quy trình/skill chung — bán được) và `_private/` (data riêng thương hiệu). **Hiện thực hóa:** `scripts/export.sh` xuất bản BÁN (tự loại `_private/` + output); mở bản bán không có `_private/` → `viet-script` Bước 0 chặn viết và hướng người dùng chạy `/bat-dau` (intake brand mới).
- **NT3 (Obsidian-friendly):** cây thư mục gọn, rõ, hiển thị đẹp trong Obsidian.
- **NT4 (OpenSpec):** mọi thay đổi lõi đi qua đề xuất → duyệt → apply → archive.
- **NT5 (Bảo toàn năng lực):** gộp/sửa file tuyệt đối không làm mất năng lực hiện có.

## 3. KIẾN TRÚC DỮ LIỆU — 3 LỚP
```
NGUỒN → RAW → WIKI → OUTPUT → Notion
```
- **RAW** (`_private/kho-kien-thuc/raw/`): video qua tokscript → giữ con trỏ YAML, XÓA transcript sau khi trích (lấy lại qua source_url); nguồn KHÔNG recall tự động (Notion/dán tay/Google Doc) → giữ **NGUYÊN VĂN**.
- **WIKI** (`_private/kho-kien-thuc/wiki/`): ý đã chắt, có nguồn (chống bịa), đánh dấu góc đã khai thác.
- **OUTPUT** (`scripts-output/` · `carousel-output/`): thành phẩm sau Cổng Kiểm + người duyệt.
- **Nhịp bắt buộc:** nạp RAW trước → CHỜ LỆNH → mới chắt RAW→WIKI (lấy góc khai thác có chủ đích).
- **Kho lạnh:** RAW >~100KB → `_private/kho-kien-thuc/raw-archive/` + để lại file con trỏ CÙNG TÊN ở `raw/` (giữ wikilink không gãy); file kho lạnh chỉ grep, **cấm Read cả file**.

## 4. BỘ NÃO ĐIỀU PHỐI (chiến lược trước, bài sau)
- **Pipeline 5 bước — thứ tự bất biến:** `NGÁCH → TỪ KHOÁ → SẢN PHẨM → FUNNEL → CONTENT`. Không nhảy cóc; bước **SẢN PHẨM là cổng chặn** (sản phẩm mỏng → dừng, không viết content bù).
- **Nhạc trưởng `/chien-luoc-gia`** (cửa vào cả chiến dịch): JTBD 4 động từ `LIỆT KÊ → SẮP XẾP → LỰA CHỌN → THỰC THI`. Nguyên tắc cốt: **không chạy hết, chỉ làm bài đúng job đã chọn.**
- **Phân tầng cửa vào:** `/chien-luoc-gia` = cả chiến dịch · `/viet-bai` = 1 bài lẻ.

## 5. HAI CỬA ẢI + VÒNG KHÉP (đo → nhân bản)
Kiến trúc 2 bảng Notion = 2 cửa ải (chốt 2026-07-21):
- **Cửa ải 1 — SẢN XUẤT** (Bảng ① "Content Đã Duyệt"): Reelo ghi bài vào để duyệt/đăng.
- **Cửa ải 2 — ĐO & NHÂN BẢN** (Bảng ② số thật view/share/CTR): đăng → số vào `so-lieu-hieu-suat.md` → xếp hạng tuyến → **nhân bản tuyến thắng** → nuôi lại voice. *(Bảng ② hiện 404 → nạp số thủ công.)*

## 6. QUY TRÌNH END-TO-END (chặng 0 + 7 chặng)
0. **GATE:** ① soi chiến lược (chiến dịch 🟢 ĐANG CHẠY → ma trận → bài phục vụ job/sản phẩm nào, chưa rõ → DỪNG) + ② GATE 5 câu (Ai đọc? · Trăn trở gì? · Vì sao quan tâm brand? · Cảm xúc bốc cao? · Đòn bẩy share?).
1. **THU:** nạp qua 3 cửa — Video (tokscript) · Insight thô (Google Drive) · Chiến lược/nguồn ngoài (Notion) — cộng chuyện chuyên môn chị Hiền cấp (`/nap-chuyen`).
2. **LẤY & DỌN:** trích transcript → lưu RAW/ → vét ý đắt vào WIKI/.
3. **VIẾT:** chọn tầng phễu → nguyên lý tâm lý → đẻ hook → chốt format → viết.
4. **KIỂM:** Cổng chất lượng theo rubric DUY NHẤT `cong-kiem-chat-luong.md` — **Lớp 1 chống bịa (VETO)** · Lớp 2 giọng AI & nhạc tính · Lớp 3 hook/tiêu đề · Lớp 6 độ tươi. **Cổng bằng chứng:** header bài phải có 3 dòng (Reference đã mở · GATE · số chữ đếm thật), thiếu → Critic từ chối chấm; Critic tự mở `_INDEX.md`, không tin header. Bài quan trọng (dài · video dài · pillar · BoFu · trượt 2 lần) → chế độ **Tòa án 4 người**. *(Lớp 4 rubric 0-100 + Lớp 5b mẫu giọng: chờ GĐ2, đủ ≥5 mẫu.)*
5. **DUYỆT:** subagent `critic-ban-giam-khao` chấm VERDICT=ĐẠT → người dùng duyệt.
6. **HỌC:** đưa bài tốt vào `mau-giong-chuan/` để hội tụ Voice.
7. **XUẤT:** lưu output + đẩy Notion (Cửa ải 1).

## 7. BỘ 9 NĂNG LỰC (SKILLS) + 1 AGENT
1. **chien-luoc-gia** — nhạc trưởng điều phối (mục tiêu → JTBD → dàn bài).
2. **viet-bai** — router hỏi định dạng.
3. **viet-script** — lõi thi công viết bài + rà soát qua Critic.
4. **bat-dau** — phỏng vấn setup brand mới (chìa khóa nhân bản).
5. **nap-chuyen** — phân loại và nạp chuyện thật vào E-Bank (`kho-cau-chuyen`).
6. **nap-insight** — quét Google Drive lấy nỗi đau/mong muốn khách hàng.
7. **review-chu-ky** — đếm tỷ lệ phễu/format cuối chu kỳ 30 ngày.
8. **don-kho** — thủ thư kiểm sức khỏe Wiki (rác/link gãy) — **chỉ ĐỀ XUẤT, archive-first, không tự xóa**.
9. **lint-kho** — audit 6 hạng mục định kỳ (chỉ báo cáo).
- **Agent `critic-ban-giam-khao`** — giám khảo độc lập (chỉ đọc, không sửa bài).

## 8. LUẬT THÉP (cấm vi phạm)
1. Giọng: kết luận trước, ngắn gọn, không ba hoa/tâng bốc.
2. **Chống bịa:** không bịa số/quote/link/nội dung; thiếu → `[chưa có]`; không nói đã làm nếu chưa làm.
3. **Tiếng Việt 100%** (trừ tên riêng).
4. **Transcript CHỈ qua tokscript** (không tự cài tool khác).
5. **Tiêu đề là VUA:** giữ Tiêu đề + Hook gốc làm trục chính, không vứt/bóp méo.
6. **Chiến lược trước, bài sau:** soi chiến dịch 🟢 ĐANG CHẠY → ma trận rồi mới viết; nhãn ⚫ HẾT HẠN = không soi để viết.
7. **Luật 3 Lớp** (xem §3): RAW giữ con trỏ (video) / nguyên văn (nguồn ngoài).

## 9. CONNECTORS
- **Tokscript (MCP, khai trong `.mcp.json`):** bắt buộc để lấy transcript video. *(2026-07-22: đã kết nối.)*
- **Notion (connector):** 2 cửa ải (xem §5). *(Bảng ② hiện 404 → nạp thủ công qua `so-lieu-hieu-suat.md`.)*
- **Google Drive (connector THÊM):** riêng cho `/nap-insight`. Chưa nối thì chỉ `/nap-insight` dừng, phần còn lại vẫn chạy.

## 10. TRÍ NHỚ & CHỐNG PHÌNH
- **File = bộ nhớ ngoài:** `NHAT-KY-PHIEN.md` (trí nhớ giữa phiên, có mục 🔁 NHẮC LẶP) + `scripts-output/_INDEX.md` (sổ chống lặp, có cột TRỤC).
- **Tự học:** thói quen hay quên bị nhắc → ghi 🔁 NHẮC LẶP; lặp ≥2 lần → nâng thành gate.
- **Nén theo DUNG LƯỢNG (KB)**, không theo số dòng. Kho lạnh cho RAW/file lớn.
- **Vệ sinh PHIÊN:** không resume phiên chat khổng lồ (mở phiên MỚI / `/clear`) — chống lỗi "Prompt too long".

## 11. PHÂN VAI *(vai theo `CLAUDE.md` Reelo mục 4; tên gọi "Vịt Máy"/"Vịt con" theo `CLAUDE.md` Xưởng + `docs/CO-CHE-REELO.md`)*
- **Chị Hiền = CHỦ**, quyền quyết định cao nhất: quyết + duyệt mọi thay đổi; vận hành hằng ngày + cập nhật DATA brand.
- **Kỹ sư (anh Tuấn + Claude/Vịt Máy) = THI CÔNG lõi hệ thống** (skill · luật · gate · format) theo quyết định đã duyệt.
- **Vịt con** = subagent việc nặng. **Critic** = giám khảo độc lập.

---

*Baseline là nguồn sự thật để đối chiếu. Mọi thay đổi lõi sau ngày đóng băng phải đi qua OpenSpec (đề xuất → duyệt → apply → archive). Chi tiết vận hành: `docs/CO-CHE-REELO.md`.*
