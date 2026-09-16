> Owner Journey correction 2026-09-16: read Insight docs/v2/17-REELO-JOURNEY.md and Reelo integrations/journey/README.md before architecture/product changes. Journey precedes source matching; Insight is one source. Preserve real CI truth/angle/CIP/currentness gates. RP4 article paused; no Notion/publish/main merge. This explicit owner directive supersedes conflicting historical phase-only scope, not truth safeguards.

> Trước khi sửa kiến trúc/product logic V2: đọc Insight docs/v2/00–16 và contracts README
> trên nhánh `v2-phase-9-reelo-integration`; đọc boundary/runbook trong
> `integrations/content_intelligence/`. Nếu xung đột accepted decisions/Strategyzer: STOP, báo lại.
> Phase 9 đang chờ architect review; không tự mở phase kế tiếp.


> **Cổng V2:** Nếu đang thi hành Content Intelligence Packet đã được adapter xác thực,
> đọc `integrations/content_intelligence/V2-BOUNDARY.md` trước. Quy định V2 trong đó
> ưu tiên hơn các chỉ dẫn legacy bên dưới về profile/customer truth, tâm lý suy đoán,
> phần trăm tu từ và chấm tiêu đề. Không có packet V2: giữ quy trình cũ.

# CLAUDE.md — Reelo (engine dùng chung)

> **Project TỰ ĐỦ.** Mọi luật ở file này + file trong project. Mở folder này trong Claude Code là chạy đúng.
> **Xưng hô theo người vận hành/creator được xác định trong workspace; không đoán tên. 100% tiếng Việt.**

## Reelo là gì
Hệ Quản Trị Tri Thức Lũy Tiến: tiêu hóa nguồn → lưu **3 lớp (RAW → WIKI → OUTPUT)** → áp chiến lược (Ma trận 30 ngày) → ra **Reel · Video dài · Carousel** đúng giọng, đẩy Notion. 3 cửa nạp: **Video** (tokscript) · **Insight thô** (Google Drive) · **Chiến lược** (Notion).

## 🗂️ Bản đồ folder (tái cấu trúc 2026-07-09 — tách để BÁN)
- **`.claude/`** = ENGINE (skills · agents). **`engine/cong-thuc-viral/`** = công thức chung (hook · tiêu đề · tâm lý · critic) + **`mau-brand/`** (template tạo brand mới).
- **`_private/`** = DATA RIÊNG của creator — **KHÔNG bán**: `brand/<brand>/` (voice · luật viết · kho chuyện · ma trận · notion-config) + `kho-kien-thuc/` (raw · wiki).
- **`scripts-output/` · `carousel-output/`** = thành phẩm. **`scripts/export.sh`** = đóng gói bản bán (tự loại `_private/` + output).
- ▶ **Bản BÁN** (mở ra KHÔNG có `_private/`): tự chạy chế độ intake — gọi `/bat-dau` để khách khai brand mới vào `_private/brand/<brand>/`, engine giữ nguyên.

## 1. ĐIỀU KIỆN VẬN HÀNH & KẾT NỐI (kiểm trước khi chạy)
- [ ] **tokscript (MCP)** → lấy transcript video (YT/TikTok/IG). Chưa nối → báo chị. ⚠️ CẤM lấy transcript cách khác (không Python/script ngoài/cài package).
- [ ] **Notion** → đẩy bài/carousel + soi Ma trận (ID: `.../_private/brand/<brand>/notion-config.md`).
- [ ] **Google Drive** (connector THÊM — CHỈ cho `/nap-insight`) → đọc insight quét. *Chưa nối → CHỈ `/nap-insight` dừng; phần còn lại VẪN CHẠY.*
- *IF tokscript/Notion lỗi → DỪNG việc liên quan, báo chị. Hướng dẫn nối: `README.md` (mục Cài đặt 3 bước).*

## 2. NGHI THỨC PHIÊN (Claude tự làm, không bắt chị nhắc)
**Đầu phiên:**
- [ ] Đọc `NHAT-KY-PHIEN.md` (cả bảng log LẪN mục 🔁 NHẮC LẶP).
- [ ] Sắp viết bài → liếc `scripts-output/_INDEX.md` (chống lặp).
- [ ] **Nén nhớ:** IF `NHAT-KY-PHIEN.md` > **~55KB** (đo **DUNG LƯỢNG file**, KHÔNG đo số dòng — mỗi phiên 1 dòng nhưng rất dài, đếm dòng luôn sai) THEN chuyển các dòng phiên cũ sang `NHAT-KY-PHIEN_archive.md` (giữ ~10 dòng phiên gần nhất + GIỮ NGUYÊN mục 🔁 NHẮC LẶP). Không xóa, báo 1 dòng. *(Luật tương tự cho `scripts-output/_INDEX.md` > ~40KB → tách bài cũ sang `_INDEX_archive.md`, giữ bài mới + Cảnh báo lặp.)*
- [ ] 🔴 **Vệ sinh PHIÊN (không chỉ file .md):** nếu Claude Code tự *resume* một phiên đã chạy NHIỀU NGÀY → **đừng dùng lại, mở phiên MỚI hoặc `/clear`**. File lịch sử phiên ở `~/.claude/projects/` (NGOÀI Reelo — KHÔNG đụng); chỉ cần bắt đầu phiên mới là né. *(2026-07-22: một phiên **71,5MB / 14.442 tin / 26 ngày** không clear → "Prompt too long" NGAY câu đầu, tràn trước khi làm gì. Nguyên nhân gốc là PHIÊN phình, không phải file .md.)*

**Trong phiên:**
- [ ] Bị nhắc 1 thói quen hay bỏ → GHI NGAY vào 🔁 NHẮC LẶP. Lặp ≥2 lần → đề xuất kỹ sư nâng thành gate.

**Cuối phiên:**
- [ ] Ghi 1 dòng log vào `NHAT-KY-PHIEN.md`: làm gì · quyết gì · đang dở · định bụng phiên sau.
- [ ] **Phiên chạy dài/nặng → KẾT THÚC hẳn hoặc `/clear`** (đừng để resume nối ngày qua ngày — xem "Vệ sinh PHIÊN" ở Đầu phiên).

## 2A. 🎼 NHẠC TRƯỞNG — /chien-luoc-gia (dựng 2026-07-21)

> 🔴 **Reelo KHÔNG chỉ là công cụ viết content — Reelo là HỆ THỐNG.** Có 1 chiến lược gia điều phối từ MỤC TIÊU → chiến lược → content đúng đích.
> **Cửa vào theo tầng:**
> - **`/chien-luoc-gia`** = cửa vào **cả chiến dịch** — đi từ mục tiêu, soi pipeline, ra chiến lược rõ ràng, RỒI mới giao bài. *(Học vai `ips-build` của Thầy PTL — nhạc trưởng, không tự làm hết.)*
> - **`/viet-bai`** = cửa vào **1 bài lẻ** (khi đã biết viết gì).
> 🔴 **Chưa rõ nên viết gì mà đã muốn viết → vào `/chien-luoc-gia` TRƯỚC.** Nguyên tắc: KHÔNG chạy hết, chỉ làm bài đúng mục tiêu.

## 2B. 🧭 PIPELINE 5 BƯỚC — THỨ TỰ BẤT BIẾN (chốt 2026-07-20)

> **NGÁCH → TỪ KHOÁ → SẢN PHẨM → FUNNEL → CONTENT**
> 🔴 **Lý do có mục này:** anh Tuấn 2026-07-20 — *"chúng ta cứ làm content mãi thì bị loạn"*. Bằng chứng đo được hôm đó: kho **CONTENT 353 dòng** mà kho **SẢN PHẨM chỉ 63 dòng** — dày gấp **5,6 lần**. Content chạy trước sản phẩm ⇒ bài hay mà không dẫn ai đi đâu.
> *(Nguyên lý thứ tự học từ skill `ips-san-pham` — Thầy Phạm Thành Long. Đã chắt lại, không import.)*

| # | Bước | File trong Reelo | Câu hỏi phải trả lời được |
|---|---|---|---|
| 1 | **NGÁCH** | `about-me.md` · `ho-so-khach-hang.md` | Bán cho AI, họ đau gì? |
| 2 | **TỪ KHOÁ** | `kho-tu-khoa-chu-de.md` | Họ đang TÌM gì? (cầu có thật) |
| 3 | 🔴 **SẢN PHẨM** | `kho-san-pham-offer.md` | Bán CÁI GÌ? **Lời hứa A→B** là gì? |
| 4 | **FUNNEL** | `customer-journey-map.md` · `kho-cta.md` | Đường đi từ người lạ → khách? |
| 5 | **CONTENT** | `ma-tran-30-ngay.md` · kế hoạch chiến dịch · `viet-script` | Bài này đẩy họ đi bước nào? |

**3 luật của pipeline:**
1. **Không nhảy cóc.** Bước sau chỉ vững khi bước trước đã rõ. Muốn viết content mà chưa rõ sản phẩm → **dừng, làm bước 3 trước**.
2. 🔴 **CONTENT CHO THẬT, CHO ĐỦ — SẢN PHẨM BÁN THỜI GIAN, KHÔNG BÁN THÔNG TIN** *(anh Tuấn chỉnh 2026-07-20)*:
   - ✅ **Content phải hướng dẫn ĐẦY ĐỦ để khách LÀM ĐƯỢC và ĐẠT ĐƯỢC điều họ muốn.** KHÔNG giấu bớt, KHÔNG cắt nửa vời để ép mua.
   - 🔴 **Cái khách thiếu KHÔNG phải kiến thức — mà là THỜI GIAN, TỐC ĐỘ và NGƯỜI ĐI CÙNG.** Đọc xong họ biết phải làm gì; nhưng tự mò thì mất hàng tháng, làm một mình thì bỏ dở giữa chừng.
   - **Sản phẩm bán:** làm cùng · rút ngắn đường · sửa tại chỗ · hệ thống ĐANG CHẠY thay vì đống kiến thức. Offer cụ thể lấy từ workspace đang được chọn, không mặc định gói của một creator.
   - ⚖️ **Câu chốt ranh giới:** *"Bán như không bán: cho đủ giá trị để khách tự muốn bước tới."* — nguyên văn từ bài **vựa mực ĐÃ VIRAL** của chị. **Chị đã thắng bằng CHO ĐỦ, không phải giấu bớt.**
   - ❌ **BỎ luật cũ** *("content không được giải hết cái sản phẩm bán")* — sai bản chất, mâu thuẫn với chính offer của chị.
3. **Mỗi bài phải khai được nó phục vụ mảnh nào của sản phẩm.** Không khai được = bài lẻ vô hướng.

---

## 3. LUẬT THÉP (cấm vi phạm)
1. **Giọng:** kết luận trước, ngắn gọn, không ba hoa, không tâng bốc.
2. **Chống bịa:** KHÔNG bịa số/quote/link/nội dung. Thiếu → `[chưa có]`. Không nói đã làm nếu chưa làm.
3. **Tiếng Việt 100%** (trừ tên riêng không dịch được).
4. **Transcript CHỈ qua tokscript** (không tự cài tool lấy cách khác).
5. **Tiêu đề là VUA:** giữ Tiêu đề + Hook gốc của nguồn làm **trục chính** — KHÔNG vứt/bóp méo (đã được thị trường kiểm chứng).
6. **Chiến lược trước, bài sau:** nhận link → BẮT BUỘC soi chiến lược tìm đúng **Pillar + Giai đoạn** RỒI mới viết. Cấm "bài lẻ vô hướng". **Thứ tự soi (siết 2026-07-20):**
   - **① Có chiến dịch 🟢 ĐANG CHẠY?** *(file kế hoạch trong `_private/brand/<brand>/` có nhãn `🟢 ĐANG CHẠY` + hôm nay nằm trong khoảng ngày)* → soi **file đó TRƯỚC** để lấy ngày/đích/CTA.
   - **② Rồi mới `ma-tran-30-ngay.md`** — dùng làm **kho nỗi đau + công thức phân bổ**.
   - Không có chiến dịch nào đang chạy → chỉ soi ma trận (như cũ).
   - 🔴 File mang nhãn `⚫ HẾT HẠN` → **KHÔNG soi để viết** (chỉ tra lịch sử).
7. **Luật 3 Lớp:** `RAW/` giữ con trỏ YAML (title/source_url/hook). **Với VIDEO qua tokscript:** trích ý sang Wiki xong thì XÓA transcript, lấy lại qua source_url. 🔴 **Với nguồn KHÔNG recall tự động (Notion · tài liệu dán · Google Doc): `RAW/` GIỮ NGUYÊN VĂN nội dung gốc** (nguồn ngoài đổi/mất là mình mất → phải tự chủ, không dựa nguồn ngoài). **Nhịp làm: nạp RAW trước → CHỜ lệnh → mới chắt RAW→WIKI** (lấy góc khai thác). Ý chính → Bản đồ tư duy ở `WIKI/` → thành phẩm ở `OUTPUT/`.
   - 🔴 **Thư mục THẬT:** RAW = `_private/kho-kien-thuc/raw/` · WIKI = `_private/kho-kien-thuc/wiki/` · **OUTPUT = `scripts-output/`** (đừng đi tìm folder tên "Outputs").
   - 🔴 **RAW quá lớn (>~100KB) = KHO LẠNH:** chuyển sang `_private/kho-kien-thuc/raw-archive/` + để lại **file con trỏ CÙNG TÊN** ở `raw/` (giữ wikilink `[[raw/...]]` không gãy). File trong `raw-archive/` **CHỈ `grep`/`Select-String` từ khoá — CẤM Read/đọc cả file** (tránh "Prompt is too long"). *(Đã áp cho `2026-07-19-longguru-caption-bank.md` — 353KB, 2026-07-21.)*

## 4. PHÂN VAI
- **Chủ workspace = quyền quyết định cao nhất (CHỦ):** quyết + duyệt mọi thay đổi; vận hành hằng ngày — viết · nạp nguồn · carousel · cập nhật **DATA brand của chị** (voice · hồ sơ khách · pillars · kho chuyện · notion-config).
- **Kỹ sư (anh Tuấn + em) = THI CÔNG lõi hệ thống** (SKILL · luật · format · gate · công thức) **theo quyết định của chị** — sửa **từng file, có kiểm soát** (chống loạn bản).
- **Gặp lỗi / Reelo làm sai** → **SỬA NGAY** (kỹ sư = bộ não sống, làm chung real-time). Nếu là **lỗi gốc lặp lại** → siết luật/gate tương ứng + ghi 1 dòng vào `NHAT-KY-PHIEN.md` (vì sao siết). *(Sổ lỗi cũ đã đóng băng ở `_archive/` — không còn dùng làm cầu nối vì đã sửa tại chỗ.)*

## 📖 Đọc thêm khi cần (không phải mỗi phiên)
`README.md` (dùng hằng ngày + cài máy mới) · `HUONG-DAN-KE-HOACH-NOI-DUNG.md` (kế hoạch 30 ngày) · `SOP-MASTER.md` (bản đồ kiến trúc + 7 chặng) · `.claude/skills/viet-script/SKILL.md` (quy trình viết).
**Lệnh nhanh:** `viết reel / video dài / carousel <link>` · `tìm video từ kênh @<user>` → `chạy batch`.
