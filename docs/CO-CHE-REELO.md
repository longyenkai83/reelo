# CƠ CHẾ HOẠT ĐỘNG REELO — Bản mô tả hệ thống hiện tại

> **Mục đích:** tài liệu **trung gian** — mô tả Reelo đang vận hành thế nào ở thời điểm quét, để một kỹ sư (phiên Claude khác / người kỹ thuật) xem xét mà không phải tự đào lại toàn bộ folder.
> **Ngày quét:** 2026-07-22. **Nguồn:** quét trực tiếp file thật (`.claude/`, `engine/`, `_private/`, `openspec/`, `CLAUDE.md`, `SOP-MASTER.md`) — không suy diễn. Chỗ chưa xác minh được đánh dấu `[chưa rõ]`.
> **Cảnh báo tuổi thọ:** đây là ảnh chụp một thời điểm. Hệ đang sống (tự cập nhật mỗi phiên). Con số file/nhãn chiến dịch sẽ trôi — coi phần cơ chế là ổn định, phần số liệu là tham khảo.

---

## 1. REELO LÀ GÌ

**Một câu:** Reelo là "Hệ Quản Trị Tri Thức Lũy Tiến" — biến nguồn (video, insight, chiến lược) thành content video/carousel tiếng Việt **đúng giọng một thương hiệu cá nhân**, có chiến lược dẫn đường, rồi đẩy lên Notion để duyệt & đăng.

**Đầu vào → Đầu ra:**
```
NGUỒN (link video · insight thô · chiến lược)
   → tiêu hóa & lưu 3 lớp (RAW → WIKI → OUTPUT)
   → áp chiến lược (Pipeline 5 bước · Ma trận 30 ngày · JTBD)
   → THÀNH PHẨM: Reel · Video dài · Carousel (đúng voice brand)
   → đẩy Notion (bảng duyệt) → chị Hiền đăng
```

**Bản chất kép (quan trọng để hiểu kiến trúc):** Reelo vừa là **engine bán được** (công thức + skill dùng chung cho brand bất kỳ), vừa chứa **data riêng của một khách** (chị Trịnh Nhi Hiền). Toàn bộ thiết kế folder xoay quanh việc **tách 2 phần này** để đóng gói bán (xem §4).

---

## 2. CÁC VAI

| Vai | Là ai | Làm gì |
|---|---|---|
| **Chiến lược gia** | Anh Tuấn (người) | Quyết định, duyệt, khóa hướng. Không có chữ DUYỆT thì không build/không sửa lõi. |
| **Kỹ sư CW** | Claude ("Vịt Máy", xưng "em") | Đề xuất + thi công lõi hệ thống (skill · luật · gate · format) theo quyết định đã duyệt. Không tự mở phạm vi. |
| **Chủ vận hành** | Chị Hiền | Quyền quyết cao nhất trên DATA brand của chị; vận hành hằng ngày (viết bài, nạp nguồn, cập nhật voice/hồ sơ khách). |
| **Vịt con** | Subagent | Thợ phụ kỹ sư phái đi làm việc nặng (quét, audit) rồi mang kết quả về — không bóp nghẹt phiên chính. |
| **Critic** | Agent `critic-ban-giam-khao` | Ban giám khảo độc lập, chấm bản nháp trước khi trình người duyệt. Chỉ đọc, không sửa bài. |

> Lưu ý: "kỹ sư" là **vai của Claude**, không phải một agent/cấu phần riêng. Agent duy nhất trong hệ là Critic.

---

## 3. HAI CƠ CHẾ TRÍ NHỚ NỀN

Reelo dựa trên nguyên lý **"file = bộ nhớ ngoài"**: mỗi phiên Claude là một trí nhớ mới, nên mọi thứ cần nhớ đều ghi ra file và đọc lại đầu phiên.

- **Nhật ký phiên** (`NHAT-KY-PHIEN.md`): cầu nối giữa các phiên — làm gì, quyết gì, đang dở, định bụng phiên sau + mục "🔁 NHẮC LẶP" (thói quen hay quên). Nén theo **dung lượng** (>~55KB → tách sang `_archive`).
- **Sổ bài đã viết** (`scripts-output/_INDEX.md`): chống lặp — mỗi bài 1 dòng kèm cột **TRỤC** (để không lặp mô-típ). Nén >~40KB.
- **Kho lạnh:** RAW >~100KB chuyển sang `raw-archive/`, để lại "bia mộ" cùng tên giữ wikilink; file kho lạnh **chỉ được grep, cấm Read cả file** (tránh tràn context).

---

## 4. BẢN ĐỒ 5 KHỐI (kiến trúc file)

```
reelo/
├── .claude/                 ★ KHỐI 1 — ENGINE: skills (9) + agents (1 Critic)
│   └── skills/viet-script/  ├─ formats/ (17 khung nội dung)
│                            └─ references/ (~24 file phụ, gồm power-words-nu)
├── engine/cong-thuc-viral/  ★ KHỐI 2 — CÔNG THỨC CHUNG (bán được)
│                            11 file công thức + _INDEX + mau-brand/ (template brand mới)
├── _private/                ★ KHỐI 3 — DATA RIÊNG chị Hiền (KHÔNG bán)
│   ├── brand/nhi-hien/      31 file (voice · hồ sơ khách · pillars · ma trận · kho chuyện · offer…)
│   └── kho-kien-thuc/       raw/ (89) · wiki/ (99) · raw-archive/ (1, kho lạnh)
├── scripts-output/          ★ KHỐI 4a — THÀNH PHẨM bài viết (~145 file + _INDEX)
├── carousel-output/         ★ KHỐI 4b — THÀNH PHẨM carousel (17 file + _INDEX)
├── openspec/                ★ KHỐI 5 — cổng kiểm soát thay đổi (xem §11)
├── scripts/export.sh        ★ đóng gói bản BÁN (tự loại _private/ + output)
├── CLAUDE.md · SOP-MASTER.md · README.md   ← luật + bản đồ (đọc mỗi phiên)
├── NHAT-KY-PHIEN.md         ← trí nhớ giữa phiên
├── docs/                    ← tài liệu (file này nằm đây)
├── _backup/                 (23 mốc backup theo ngày) · _archive/ (đồ cũ)
```

**Nguyên tắc tách để bán:** mở bản BÁN ra sẽ **không có `_private/`** → engine chạy chế độ intake (gọi `/bat-dau` để khách mới khai brand vào `_private/brand/<brand>/`, engine giữ nguyên). `scripts/export.sh` tự loại phần riêng + thành phẩm.

---

## 5. KIẾN TRÚC DỮ LIỆU 3 LỚP (RAW → WIKI → OUTPUT)

```
NGUỒN → RAW → WIKI → OUTPUT → Notion
```

| Lớp | Ở đâu | Quy tắc |
|---|---|---|
| **RAW** | `_private/kho-kien-thuc/raw/` | **Video qua tokscript:** trích ý sang Wiki xong thì **XÓA transcript**, chỉ giữ con trỏ YAML (title/source_url/hook), lấy lại qua source_url. **Nguồn KHÔNG recall tự động** (Notion, tài liệu dán, Google Doc): **GIỮ NGUYÊN VĂN** (nguồn ngoài mất là mất luôn → phải tự chủ). |
| **WIKI** | `_private/kho-kien-thuc/wiki/` | Ý chính dạng bản đồ tư duy, **có ghi nguồn** (chống bịa), có mục "KHAI THÁC" đánh dấu góc đã dùng (chống lặp). |
| **OUTPUT** | `scripts-output/` · `carousel-output/` | Thành phẩm sau khi qua Cổng Kiểm + người duyệt → đẩy Notion. |

**Nhịp bắt buộc:** nạp RAW trước → **CHỜ LỆNH** → mới chắt RAW→WIKI (lấy góc khai thác có chủ đích, không tự động chắt ngay).

---

## 6. BA CỬA NẠP

| # | Cửa | Qua công cụ | Ghi chú |
|---|---|---|---|
| 1 | **Video** (YT/TikTok/IG) | **tokscript** (MCP) | Cách DUY NHẤT lấy transcript. Cấm script/package ngoài. |
| 2 | **Insight thô** | **Google Drive** | Đọc file Data Miner (insights-pack v1/v2, phân-tích-toàn-diện). Chỉ cho `/nap-insight`. |
| 3 | **Chiến lược / nguồn ngoài** | **Notion** hoặc dán tay / `/nap-chuyen` | Nguồn ngoài & chuyện chuyên môn chị Hiền cấp trực tiếp. |

---

## 7. BỘ NÃO ĐIỀU PHỐI

Reelo **không chỉ là công cụ viết** — có một tầng chiến lược đứng trên quyết định *viết gì, cho ai, đẩy họ đi đâu*.

### 7.1 Pipeline 5 bước — thứ tự bất biến
```
NGÁCH → TỪ KHOÁ → SẢN PHẨM → FUNNEL → CONTENT
```
| # | Bước | File | Luật |
|---|---|---|---|
| 1 | Ngách | `about-me.md` · `ho-so-khach-hang.md` | Bán cho ai, họ đau gì? |
| 2 | Từ khoá | `kho-tu-khoa-chu-de.md` | Họ đang TÌM gì? |
| 3 | 🔴 **Sản phẩm** | `kho-san-pham-offer.md` | Bán CÁI GÌ? Lời hứa A→B? **(cổng chặn: sản phẩm mỏng → dừng, không viết content bù)** |
| 4 | Funnel | `customer-journey-map.md` · `kho-cta.md` | Đường từ người lạ → khách? |
| 5 | Content | `ma-tran-30-ngay.md` · kế hoạch · `viet-script` | Bài này đẩy họ đi bước nào? |

**3 luật:** không nhảy cóc · content cho thật cho đủ (sản phẩm bán THỜI GIAN/tốc độ/người đi cùng, không bán thông tin) · mỗi bài phải khai được nó phục vụ mảnh nào của sản phẩm.

### 7.2 Nhạc trưởng `/chien-luoc-gia` — JTBD 4 động từ
Cửa vào cả chiến dịch. Vận hành: **LIỆT KÊ** job/pain (từ `ho-so-khach-hang`) → **SẮP XẾP** (job đau cao + chưa ai giải = underserved) → **LỰA CHỌN** 2-3 job, bỏ phần còn lại → **THỰC THI** (soi pipeline + cân trụ cột → bảng chiến lược → giao từng bài xuống `viet-script`). Nguyên tắc cốt: **không chạy hết, chỉ làm bài đúng job đã chọn.**

---

## 8. NĂNG LỰC — 9 SKILL

| Skill | Kích hoạt | Việc chính | Ra |
|---|---|---|---|
| **chien-luoc-gia** | `/chien-luoc-gia`, "lên chiến lược", "reelo đang ở đâu" | Nhạc trưởng: mục tiêu → pipeline → JTBD → bảng chiến lược | Bảng chiến lược (KHÔNG viết bài) → giao `viet-script` |
| **viet-bai** | `/viet-bai`, "viết reel/bài/carousel" | Router mỏng: hỏi định dạng (1-6), không tự viết | Route ngữ cảnh → `viet-script` |
| **viet-script** | Nhận từ `viet-bai` (backend, không tự kích hoạt) | Lõi thi công: GATE → raw→wiki → 5 khối GATE → viết → Critic → loop | Bản ĐẠT → `scripts-output/` + Notion |
| **bat-dau** | `/bat-dau` (brand MỚI) | Phỏng vấn 9 câu → chân dung khách → sinh pillars + ma trận | `ho-so-khach-hang` · `voice-profile` · `content-pillars` · `ma-tran-30-ngay` |
| **nap-chuyen** | `/nap-chuyen` + nội dung | Phân loại (A) chuyện thật / (B) chuyên môn → chèn nguyên văn | `kho-cau-chuyen.md` |
| **nap-insight** | `/nap-insight` | Đọc Drive → trích Pains/Gains → merge chống trùng | `ho-so-khach-hang.md` |
| **review-chu-ky** | `/review-chu-ky` (cuối chu kỳ) | Đếm tỷ lệ phễu/format/pillar thực tế vs mục tiêu | Báo cáo (không tự sửa) |
| **don-kho** | `/don-kho` | Quét wiki: trùng/rác/link gãy/thiếu chuẩn | Bảng đề xuất (chờ duyệt) |
| **lint-kho** | định kỳ | Audit 6 hạng mục Karpathy | Báo cáo 🔴/🟡/🟢 (chỉ báo) |

**Chuỗi lõi:** `chien-luoc-gia` (viết GÌ) → `viet-bai` (định dạng nào) → `viet-script` (thi công) → `critic-ban-giam-khao` (chấm) → xuất bản.

---

## 9. QUY TRÌNH VIẾT 1 BÀI + CÁC CỔNG

1. **(Tùy chọn, tầng cao)** `chien-luoc-gia`: mục tiêu → pipeline 5 bước (§7.1, **cổng sản phẩm** chặn nếu mỏng) → chọn job → bảng chiến lược → giao bài.
2. **`viet-bai`**: nhận link/yêu cầu → hỏi định dạng (Reel · Bài ngắn · Bài dài · Video dài · Carousel · Chắt lọc) → route.
3. **`viet-script` GATE 0**: kiểm Data Brand + bắt khai "bài này bám sản phẩm nào, mảnh nào" (thiếu → dừng).
4. Soi **chiến dịch 🟢 ĐANG CHẠY** trước → rồi ma trận 30 ngày → nạp RAW (bảo vệ RAW theo §5).
5. Dọn WIKI → mục KHAI THÁC (chống lặp góc) → trình menu góc cho chủ chọn.
6. **In 5 khối GATE tiền-viết:** GATE 5 câu · nguyên lý tâm lý · bảng ≥8 hook (có công thức) · 3-5 tiêu đề · Format + TRỤC (chống lặp trục xuyên bài — phải trích nguyên văn 2 bài gần nhất từ `_INDEX`).
7. Viết: gate giọng · rà tiếng Việt · hypnotic writing · tự rà theo `cong-kiem-chat-luong.md` · CTA xoay vòng.
8. **Phái Critic** chấm độc lập → loop sửa tới `VERDICT: ĐẠT ✅` (bài quan trọng dùng chế độ **Tòa Án 4 người**).
9. Rà lần cuối → lưu `scripts-output/` (+ caption) → **đẩy Notion** (bảng "Content Đã Duyệt") → ghi sổ khai thác ngược vào wiki nguồn.
10. **(Vòng khép)** `review-chu-ky` / nhạc trưởng bước 5 đo số thật → nhân bản tuyến thắng → nuôi lại `mau-giong-chuan/` + voice.

### Critic — các lớp đang bật
Nguồn rubric DUY NHẤT = `engine/cong-thuc-viral/cong-kiem-chat-luong.md` (Critic bắt buộc Read lại mỗi lần, không chấm theo trí nhớ). **Cổng vào:** header nháp phải đủ 3 dòng bằng chứng (reference · GATE 5 câu · số chữ đếm thật), thiếu → trả về không chấm.
- **Lớp 1 — Chống bịa** (VETO duy nhất: số/quote/case phải truy được về raw·wiki·kho-cau-chuyen).
- **Lớp 2 — Văn AI & nhạc tính** (chống cụm AI, chống lặp trục contrast, giọng THẤU không phán…) — gợi ý nâng chất.
- **Lớp 3 — Hook & tiêu đề** · **Lớp 3.5 — Kể chuyện** · **Lớp 6 — Độ tươi** (điểm thưởng).
- ⏸ **Lớp 4 (rubric 0-100) + Lớp 5b (đối chiếu mẫu giọng): CHỜ GĐ2** — cần ≥5 mẫu giọng, hiện mới **2/5** → chấm giọng còn cảm tính.

---

## 10. ENGINE CÔNG THỨC VIRAL (`engine/cong-thuc-viral/`)

| File | Vai |
|---|---|
| `_INDEX.md` | Bản đồ 5 tầng: Gate → Nguyên lý → Hook → Cấu trúc kể → Đầu ra |
| `psychology-gate.md` | GATE 3 câu bắt buộc trước khi viết |
| `nguyen-ly-tam-ly.md` | 7 nguyên lý tâm lý nền (Reframe/Contrast là lõi) |
| `hook-system.md` | Bộ ĐẺ hook (10 công thức, 6 Story Locks, luật đa dạng hook) |
| `checklist-hook.md` | Bộ CHẤM/lọc hook (tiêu chí, 10 lỗi giết hook, công thức mở 15s) |
| `bo-tieu-de.md` | 16 khung tiêu đề (title swipe) |
| `kho-hook.md` | ~55 hook thật để học khung & nhái |
| `story-structures.md` | 3 cấu trúc kể chuyện ngắn |
| `khung-7-khuc-ke-chuyen.md` | Khung kể chuyện dài 7 khúc + ngân hàng câu hỏi cho tệp Nhi Hiền |
| `dinh-dang-dau-ra.md` | Luật 3 định dạng (Reel 170-220 chữ · Video dài ≥1000 · Carousel 5-8 slide) |
| `chien-luoc-content.md` | 7 giai đoạn hành trình + 5 Stages of Awareness + map trục (tỷ lệ % cứng đã bỏ, thay bằng Dynamic Ratio) |
| `cong-kiem-chat-luong.md` | **Rubric Critic — bản DUY NHẤT** (3 bản trùng đã gộp bỏ 2026-07-20) |
| `mau-brand/…` (3 file) | Template tạo brand mới: form Brand Profile · SOP tinh chỉnh voice · form thu thập Offer |

**Đính chính vị trí (dễ nhầm):** 17 file **Format** nằm ở `.claude/skills/viet-script/formats/`; `power-words-nu.md` ở `.claude/skills/viet-script/references/` — **không** ở `engine/`.

---

## 11. CONNECTORS & CỔNG KIỂM SOÁT

### Connectors
| Connector | Dùng cho | Khi lỗi |
|---|---|---|
| **tokscript** (MCP, `.mcp.json`) | Lấy transcript video | Dừng việc liên quan, báo chị. **⚠️ Phiên hiện tại cần authorize OAuth trước khi dùng.** |
| **Notion** | Đẩy bài/carousel + soi ma trận. 2 bảng: ① *Content Đã Duyệt* (Reelo ghi vào) · ② *Content đăng chính thức* (Reelo đọc số) | Dừng việc liên quan. **⚠️ Bảng ② hiện 404 — phải nạp số thủ công qua `so-lieu-hieu-suat.md`.** |
| **Google Drive** | Chỉ `/nap-insight` | Connector THÊM — chưa nối thì chỉ `/nap-insight` dừng, phần còn lại vẫn chạy. |

### OpenSpec (`openspec/`)
- Hiện **chỉ có** `changes/tai-cau-truc-reelo/` (proposal · specs · tasks · dot-1). **Không có `specs/` baseline, không có `project.md`** ở tầng Reelo.
- Change B1 **đã apply 2026-07-09** (tách `_private/` + `engine/` + `export.sh`), **còn Chặng 8 (archive) chưa làm** — chờ chị Hiền test `/viet-bai` vài phiên.
- 🔴 **Hệ quả:** nguồn sự thật "hệ thống LÀ gì" đang nằm ở `CLAUDE.md` + `SOP-MASTER.md` (file sống, dễ trôi), **chưa có tài liệu đóng băng**. Tài liệu này là bước lấp tạm.

---

## 12. 🔴 ĐIỂM MẠNH · ĐIỂM NGHẼN · RỦI RO (phần cho kỹ sư soi)

### Điểm mạnh
- **Tách engine ↔ _private rõ ràng** → đóng gói bán được (có `export.sh`).
- **Chống bịa nghiêm** — veto ở Critic + provenance bắt buộc (mọi số/quote truy về nguồn).
- **Critic độc lập** + rubric 1 bản duy nhất (đã gộp bỏ bản trùng).
- **Trí nhớ qua file + cơ chế nén** — chống phình, có kho lạnh.
- **Pipeline có cổng chặn thật** (sản phẩm mỏng → dừng, không viết bù).

### Điểm nghẽn / rủi ro — phân loại trung thực
| Loại | Vấn đề |
|---|---|
| 🔴 **Thiếu nền** | Chưa có `openspec/specs/` đóng băng hệ thống → nguồn sự thật tản mát, phụ thuộc file sống. |
| 🔴 **Chấm giọng còn cảm tính** | Lớp 4 + 5b của Critic chờ GĐ2, mới 2/5 mẫu giọng → chất lượng giọng chưa có thước đo cứng. |
| 🟡 **Phình quy mô** | ~145 bài output · 99 wiki · 89 raw · 31 file brand · 24 references · 17 formats. Nhiều tầng → khó nắm toàn cảnh. *(Lưu ý: sự cố "Prompt too long" 2026-07-22 gốc là 1 phiên chat 71MB, KHÔNG phải các file .md này — nhưng quy mô lớn làm hệ khó bảo trì.)* |
| 🟡 **Vòng đo số chưa tự động** | Notion bảng ② (đo số) 404 → phải nạp số thủ công → vòng khép "nhân bản tuyến thắng" bị hở. |
| 🟡 **Luồng video đang tắc** | tokscript cần OAuth chưa authorize (phiên hiện tại). |
| 🟡 **Chưa nhất quán quy ước** | `ke-hoach-noi-dung-tu-khoa-thcn.md` là kế hoạch nhưng chưa gắn nhãn trạng thái 🟢/🟡/⚫. |
| 🟡 **Việc dở treo** | Change `tai-cau-truc-reelo` còn Chặng 8 chưa archive; 2 chiến dịch 🟢 chồng lấn (có chủ đích, cần theo dõi). |
| 🟡 **Doc kiến trúc cũ lệch path** | `_archive/root-docs/so-do-reelo.md` + `kien-truc-he-thong.md` có sơ đồ mermaid giá trị nhưng path lỗi thời (dùng `brand-profiles/` cũ). |

---

## 13. CÂU HỎI MỞ CHO KỸ SƯ

1. Có nên **đóng băng tài liệu này (hoặc bản kế) thành `openspec/specs/`** để làm nguồn sự thật chính thức, thay vì để `CLAUDE.md` gánh?
2. Quy mô đang phình — có cần một **vòng đơn giản hóa** (gộp references, rà skill trùng vai) không, hay giữ nguyên vì mỗi thứ có lý do?
3. **Lớp 4/5b của Critic** đợi đủ 5 mẫu giọng — có cách nào rút ngắn đường tới thước đo giọng cứng?
4. Vòng **đo số thật** đang hở (Notion 404) — chấp nhận nạp tay hay cần nối lại API?
5. Có nên **archive Chặng 8** của change tái cấu trúc để dọn openspec cho sạch?

---

*Hết. Tài liệu do kỹ sư (Claude) quét & tổng hợp 2026-07-22 từ file thật, phục vụ review. Mọi con số là ảnh chụp thời điểm — kiểm lại trước khi dựa vào để quyết định lớn.*
