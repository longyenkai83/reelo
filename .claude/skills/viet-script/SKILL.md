---
name: viet-script
description: BACKEND ORCHESTRATOR lõi thi công viết bài. Nguồn cấp từ router viet-bai. Cửa vào duy nhất.
disable-model-invocation: true
---

> **Cổng V2:** Nếu đang thi hành Content Intelligence Packet đã được adapter xác thực,
> đọc `integrations/content_intelligence/V2-BOUNDARY.md` trước. Quy định V2 trong đó
> ưu tiên hơn các chỉ dẫn legacy bên dưới về profile/customer truth, tâm lý suy đoán,
> phần trăm tu từ và chấm tiêu đề. Không có packet V2: giữ quy trình cũ.



### 0. KIỂM DATA BRAND (bản bán — chạy TRƯỚC mọi việc)
- [ ] IF **không có** `_private/brand/<brand>/` (ma trận · voice · hồ sơ · kho-cta) → **DỪNG, KHÔNG viết.** Đây là bản BÁN chưa khai brand → hướng người dùng chạy **`/bat-dau`** để tạo hồ sơ brand trước. *(Bản riêng của chủ luôn có sẵn `_private/` → bỏ qua bước này.)*

### 0B. 🧭 GATE PIPELINE — BÀI NÀY BÁM SẢN PHẨM NÀO? (chặn cứng, siết 2026-07-20)
> Thứ tự bất biến: **NGÁCH → TỪ KHOÁ → SẢN PHẨM → FUNNEL → CONTENT** *(xem `CLAUDE.md` mục 2B)*. Content là bước **CUỐI** — viết mà không biết mình đang bán gì thì thành bài lẻ.

- [ ] **Khai 1 dòng — thiếu = DỪNG:** `Bài này phục vụ [tên sản phẩm/offer], mảnh [___] trong lời hứa của nó.`
  - Mở `_private/brand/<brand>/kho-san-pham-offer.md` lấy **tên offer đang đẩy + lời hứa A→B**. Có chiến dịch 🟢 ĐANG CHẠY thì lấy **đích của chiến dịch đó**.
  - Không có sản phẩm nào đang đẩy → bài chỉ được làm **vai PHỦ** (nuôi/lan truyền), **CẤM** gắn CTA bán.
- [ ] 🔴 **CHO THẬT — rồi CHO THẤY CÁI HỌ KHÔNG CÓ (anh Tuấn chốt 2026-07-20):**
  - ✅ **Dạy đầy đủ, khách làm theo là ra kết quả.** KHÔNG giấu bước, KHÔNG cắt nửa vời để ép mua. Giấu = mất niềm tin, và trái với câu đã viral của chị: *"cho đủ giá trị để khách tự muốn bước tới"*.
  - 🔴 **Thứ sản phẩm bán KHÔNG phải kiến thức — mà là THỜI GIAN · TỐC ĐỘ · NGƯỜI ĐI CÙNG.** Bài xong, người đọc **biết phải làm gì**; nhưng tự làm thì **mất hàng tháng, dễ bỏ dở, không ai sửa cho**.
  - **Cách gợi tự nhiên (không ép):** sau phần hướng dẫn đủ, chạm nhẹ vào **chi phí thật của việc tự làm** — thời gian mò, thứ tự dễ sai, làm một mình hay bỏ giữa chừng. Rồi để họ tự quyết.
  - ❌ **CẤM** kiểu *"phần còn lại mua khoá học sẽ rõ"* / cắt giữa chừng / úp mở.
  - ⚠️ *Lỗi ngược lại cũng phải tránh: bài dạy xong mà **không cho thấy còn chặng đường phía trước** ⇒ người đọc tưởng xong rồi, không thấy lý do đi tiếp.*
- [ ] **IF phát hiện SẢN PHẨM chưa rõ** (chưa có lời hứa A→B · chưa có giá/link · outline mỏng) → **BÁO NGƯỜI DUYỆT TRƯỚC**, đừng viết bù bằng content. *(Sản phẩm mỏng thì content nhiều mấy cũng không bán được.)*

### 1. CHẾ ĐỘ ĐẶC BIỆT & ĐỊNH DẠNG (TRA CỨU NHANH)
* **Chạy Batch (hàng loạt):** Đọc `references/che-do-batch.md`.
* **Quét kênh tìm video:** Đọc `references/che-do-tim-video.md`.

| Định dạng | Số chữ | Giọng văn / Luật áp dụng |
| --- | --- | --- |
| **1. Reel** | 210–240 | VĂN NÓI (Nối: mà/thì/rồi). Áp 17 Format + `vietnamese-language-layer.md` |
| **2. Bài ngắn** | 200–400 | VĂN VIẾT gọn, tách bạch (`format-bai-viet.md` Mục A) |
| **3. Bài dài** | 400–800 | VĂN VIẾT kể chuyện sâu (`format-bai-viet.md` Mục B) |
| **4. Video dài**| ≥1000 | NÓI (Bám gốc 100%). Kịch bản 6 bước + 28 Khung tiêu đề |
| **5. Carousel** | Nén/Slide | Cô đọng (`format-carousel.md` 4 công thức) |
| **6. Chắt lọc** | Bám gốc | **TUYỆT ĐỐI BÁM GỐC 100%.** Chuyển ngữ sang văn nói, giữ nguyên ý/cấu trúc tác giả. CẤM đẻ hook/format sáng tạo. |

---

### 2. QUY TRÌNH THI CÔNG 5 BƯỚC (CHECKLIST BẮT BUỘC)

#### BƯỚC 0 & 1 & 2: CHIẾN LƯỢC & NẠP RAW
- [ ] **Soi chiến lược — ĐÚNG THỨ TỰ 2 BƯỚC** *(luật thép `CLAUDE.md` #6, siết 2026-07-20)*:
  - **① CHIẾN DỊCH ĐANG CHẠY trước:** liếc file kế hoạch trong `_private/brand/<brand>/` có nhãn `🟢 ĐANG CHẠY` **và hôm nay nằm trong khoảng ngày** → lấy **ngày · đích · CTA · tầng phễu tuần này**. Nhãn `⚫ HẾT HẠN` → **BỎ QUA, không soi** *(file hết hạn được thay bằng bia mộ cùng tên, mở ra sẽ thấy file kế nhiệm — đi theo đó)*.
    - 🔴 **CHỈ ĐƯỢC CÓ MỘT file 🟢 ĐANG CHẠY phủ hôm nay.** Thấy từ hai file trở lên cùng nhãn 🟢 mà khoảng ngày chồng nhau → **DỪNG, báo người duyệt** để đóng bớt; đừng tự đoán file nào đúng. *(Bài học 2026-08-08: ba file cùng đeo 🟢, một file đã hết hạn từ 02/08 mà chưa hạ nhãn.)*
  - **② Rồi `ma-tran-30-ngay.md`:** khớp Pillar + Phễu (Lạnh/Ấm/Nóng/Bán), lấy **nỗi đau + công thức phân bổ**. Ô đã đầy → dùng nội dung mới làm chất liệu.
  - Không có chiến dịch nào đang chạy → chỉ soi ma trận.
- [ ] **🧭 KHUNG KHAI THÁC (khi lên chiến lược / anh Tuấn đào insight):** đọc `_private/brand/<brand>/khung-khai-thac-vpc.md` — **Keyword → Pain/Gain khách (Value Proposition Canvas) → cách giải quyết → phân tầng thị trường** (cách phổ thông = Lạnh/Ấm · cách RIÊNG nhanh-tiện hơn = Nóng/Bán). Insight anh đưa → phân loại Gain Creator / Pain Reliever / Product rồi mới chọn tuyến.
- [ ] **🔍 IF bài SEO / bài "cách…", "làm sao…" / đang tự chọn chủ đề (KHÔNG có link nguồn):** mở `_private/brand/<brand>/kho-tu-khoa-chu-de.md` — lấy **từ khóa có người tìm thật** + intent → tầng phễu, rải từ khóa vào tiêu đề & hook. *(Bài có link nguồn → BỎ QUA, đừng mở.)*
- [ ] **Nạp nguồn:** Qua `tokscript` (Video), `notion-fetch` hoặc Hiền cấp.
- [ ] **Bảo vệ RAW (Luật 3 lớp):** Trích ý xong → XÓA TRANSCRIPT. `RAW/` CHỈ GIỮ YAML frontmatter làm con trỏ.

#### BƯỚC 3: DỌN WIKI & TẠO BẢN ĐỒ KHAI THÁC
- [ ] **Vét cạn:** Trích xuất 100% số liệu, quote đắt, case study từ transcript vào WIKI (Chống bịa).
- [ ] **Mind-map & Insight:** Đào Insight lõi, cơ chế TẠI SAO. BẮT BUỘC nêu `Sources:` trích ngược về RAW.
- [ ] **Chặn trùng & Tự Archive:** Bỏ qua nếu nhãn đã có ≥6 wiki trùng lặp. Tự archive wiki khi khai thác hết góc.
- [ ] **🗺️ MỤC KHAI THÁC (BẮT BUỘC với wiki mới):** cuối wiki phải có mục `## 🗺️ KHAI THÁC` — bảng `| Góc/Tuyến | ĐDạng | TT | Bài (scripts-output) |` (TT: ⬜ chưa · ✍️ nháp · ✅ đã viết). Đây là NƠI DUY NHẤT theo dõi nguồn này đã ra bài nào.
- [ ] 🔴 **HỎI TRƯỚC KHI TRÌNH GÓC: "CHẤT LIỆU NÀY ĐÃ RA BÀI CHƯA?" (siết 2026-07-20 — lỗi lặp 3 LẦN trong 1 ngày):**
  1. Mở mục `## 🗺️ KHAI THÁC` của RAW/wiki nguồn → góc nào 🔴 ĐÃ KHAI THÁC thì **BỎ khỏi menu**, không trình.
  2. RAW có trường **`Trạng thái = Đã khai thác`** (hoặc nguồn Notion đánh vậy) → **PHẢI đi tìm bài gốc** rồi mới trình góc. Không tìm được → **HỎI NGƯỜI DUYỆT**, đừng đoán.
  3. `grep` từ khoá lõi của chất liệu trong `scripts-output/` + `_INDEX.md` trước khi trình.
  - ⚠️ **3 lần vấp trong ngày 2026-07-20:** ① bài FOLLOW-01 trùng ý D7 ② menu góc Haidilao — 4/6 góc đã nằm trong bài viral ③ góc "cá lớn hồ nhỏ" — đã lên video viral. **Cả 3 đều do không hỏi câu này trước.**
- [ ] **BƯỚC 3.5 — MENU GÓC (CHẶN CỨNG, thiếu → DỪNG):** Bóc **TẤT CẢ** góc video chứa (mỗi góc = 1 luận điểm đứng riêng thành 1 bài). IN BẢNG MENU: `# | Góc (1 câu) | Nỗi đau/Ngày ma trận | Tầng | Định dạng hợp | Trạng thái`. Góc không khớp ma trận → ghi "ngoài ma trận", VẪN GIỮ. 🔴 CẤM tự chọn góc rồi viết luôn — **TRÌNH CHỦ CHỌN SỐ**. *(Batch nhiều video: chỉ lưu kho, trình menu gộp cuối phiên.)*
- [ ] **LƯU MENU GÓC vào mục `## 🗺️ KHAI THÁC` của CHÍNH wiki nguồn** (không tạo file riêng): ghi các góc thành dòng bảng, trạng thái `⬜ chưa · ✍️ nháp · ✅ đã viết`. Chỉ archive wiki khi bảng KHAI THÁC hết ô ⬜. *(⚠️ Cơ chế cũ `wiki/khai-thac/kt-*.md` ĐÃ BỎ 2026-07-19 — thay bằng mục KHAI THÁC trong wiki; `kt-mayashare` giữ làm lịch sử, KHÔNG tạo kt mới.)*
- [ ] **NHÂN TUYẾN (chống loãng):** chỉ nhân góc ⭐1/meta-pain **có trục đắt**; ≤3 định dạng/góc; mỗi tuyến ĐỔI góc đánh theo tầng (❄️ chạm → 🔥 kể chuyện → 🔥 bóc cơ chế), KHÔNG lặp cùng 1 ý; **≤3 góc/phiên** (giữ chất qua Critic).

#### BƯỚC 3.6 & 3.7: MỞ HỘP SỌ & IN 5 KHỐI GATE (CHẶN CỨNG)
- [ ] **ĐỌC LUẬT THÉP TRƯỚC KHI IN GATE:** BẮT BUỘC đọc `references/luat-viet-cot-loi.md` (để biết cách ghép 2 nguồn, chốt câu lõi, Gate Fit) và `references/luat-format-da-dang.md` (để tránh lạm dụng format).
- [ ] **📂 MỞ KHUNG THEO LOẠI BÀI (lean-loading — chỉ mở đúng 1, KHÔNG mở cả 2):**
  - **Bài KỂ CHUYỆN** (Bài dài · story · trải nghiệm thật) → `engine/cong-thuc-viral/khung-7-khuc-ke-chuyen.md`. Khúc **1 (mồi) · 4 (căng/nghẹn) · 7 (tấm gương + câu hỏi)** quyết định lan truyền — bám tỉ lệ %, đừng kể phẳng.
  - **Bài HƯỚNG DẪN** (how-to · "5 việc làm ngay" · checklist) → `_private/brand/<brand>/kho-huong-dan-how-to.md` lấy khung bước + cách viết bước cho gọn.
- [ ] **MỞ `<thinking>`:** Tự tranh luận nội bộ về Format, Nguyên lý, Hook TRƯỚC khi in.
- [ ] **IN 5 KHỐI GATE (THIẾU 1 KHỐI -> DỪNG VIẾT):**
  1. **GATE 5 CÂU:** (1) Nói với ai? (2) Trăn trở gì? (3) Vì sao quan tâm thương hiệu NÀY? *(chi tiết + luật "câu 3 KHÁC nhau mỗi bài, cấm lặp định vị": `psychology-gate.md`)* (4) **CẢM XÚC:** cảm xúc lõi của bài là **BỐC CAO** (nghẹn · phẫn nộ chính nghĩa · kinh ngạc · tự hào · sợ-rồi-được-giải-toả) hay chỉ **man mác** (buồn nhẹ, "hay hay")? 🔴 Man mác = KHÔNG lan → đẩy cảm xúc lên (tăng tương phản, đặc tả khoảnh khắc đỉnh) hoặc đổi góc. (5) **ĐÒN BẨY SHARE:** *"Chia sẻ bài này, người đọc nói được điều gì về CHÍNH HỌ?"* (vd "tôi cũng từng thế" · "tôi là người sâu sắc" · "tôi quan tâm gia đình"). 🔴 Không trả lời được = bài sẽ không ai share. *(Câu 4–5 học từ skill content-viral — Thầy Phạm Thành Long.)*
  2. **NGUYÊN LÝ:** Gọi đúng tên 1-2 nguyên lý từ `nguyen-ly-tam-ly.md`.
  3. **BẢNG ≥8 HOOK:** Ghi rõ CỘT CÔNG THỨC (10 công thức `hook-system.md` mục B + Story Locks mục D · ví dụ nhái `kho-hook.md`). Chốt 3⭐.
  4. **BẢNG 3-5 TIÊU ĐỀ:** Nêu tên khung (`bo-tieu-de.md` hoặc 28 khung). TRÌNH USER CHỌN.
  5. **FORMAT & TRỤC BÀI:** Khai báo Format + **TRỤC bài đắt** — chọn 1 dạng: reframe/contrast · **ẩn dụ** · hình ảnh cụ thể · nghịch lý · tuyên ngôn · câu hỏi (KHÔNG bắt buộc "Không phải X mà Y" — Van 1; xem `luat-viet-cot-loi.md` mục 2), đã qua Gate Fit.
     - 🔴 **CHẶN LẶP TRỤC (bắt buộc ghi ra, thiếu = DỪNG):** MỞ THẬT `scripts-output/_INDEX.md` → **trích 1 dòng NGUYÊN VĂN** của 2 bài gần nhất vào header + ghi trục của chúng (vd: *`| 2026-08-d21 | Reel | P1 | …` → trục contrast*) RỒI mới chốt trục bài này. **2 bài liền trước đã là contrast → bài này PHẢI đổi trục.** ⚠️ **Khai trục mà KHÔNG trích được dòng gốc = chưa soi = DỪNG.** *(Luật đầy đủ: `cong-kiem-chat-luong.md` Lớp 2 — ô CHỐNG LẶP TƯƠNG PHẢN vế ②.)*
- [ ] **Trình Dàn ý ngắn -> USER DUYỆT TRƯỚC.**

#### BƯỚC 4: VIẾT BÀI & RÀ SOÁT
- [ ] **GATE GIỌNG (Đặc biệt cho Reel):** Mở `_private/brand/<brand>/mau-giong-chuan/` nghe nhịp TRƯỚC khi gõ. *(IF brand chưa có mẫu giọng → BỎ QUA gate này, KHÔNG chặn — bản bán chưa khai giọng.)* Nhịp văn nói chung: `references/spoken-voice-va-hypnotic.md` mục A.
- [ ] **Rà Tiếng Việt (BẮT BUỘC):** rà theo `vietnamese-language-layer.md` **mục 3B (14 nguyên lý từ ngữ)** + mục 4/4B. Ép quan hệ từ, tình thái từ. *(🔴 `references/tu-vung.md` & `references/tu-tu-chi-tiet.md` = KHO TRA CỨU — chỉ mở khi **BÍ TỪ** hoặc khi **Critic báo lỗi giọng**, KHÔNG đọc mặc định mỗi bài.)*
- [ ] **HYPNOTIC WRITING (chà nhám ngôn từ — Joe Vitale):** làm đẹp vốn từ (câu báo cáo → câu đắt gợi hình) + nhịp thôi miên (câu ngắn, ngắt mượt, người đọc trượt dài). Đẹp NEO sự thật, CẤM sáo rỗng/bịa. Chi tiết: `references/spoken-voice-va-hypnotic.md` mục B.
- [ ] **TỰ RÀ THEO CỔNG KIỂM (1 nguồn duy nhất):** đối chiếu `engine/cong-thuc-viral/cong-kiem-chat-luong.md` — Lớp 1 chống bịa · Lớp 2 văn AI & nhạc tính (gồm Hướng-tương-lai · từ khóa chính · câu hỏi tấm gương · Hán Việt sáo · giọng THẤU không phán) · Lớp 3 hook & tiêu đề · Lớp 6 độ tươi. *(🔴 Đừng chép tiêu chí ra chỗ khác — sửa tiêu chí thì sửa file đó.)*
- [ ] **CTA — chọn từ kho, XOAY chống lặp:** lấy biến thể `_private/brand/<brand>/kho-cta.md` (đúng mục tiêu theo tuyến phễu); soi 2-3 bài gần `scripts-output/_INDEX.md` → KHÔNG lặp cùng kiểu + đuôi CTA quá 2 bài liền.
- [ ] **HÀNG RÀO CRITIC:** Phái sub-agent `critic-ban-giam-khao` chấm bản nháp.
  - 🏛️ **Bài quan trọng (dài / pillar / BoFu / trượt 2 lần) → TÒA ÁN 4 NGƯỜI** (3 GK song song: Sáng tạo · Sự thật · Văn chương + Thư ký chốt VERDICT). Bài thường nhật: Critic 1 người. Chi tiết: `critic-ban-giam-khao.md` + `docs/OpenSpec-Copywriter-Da-Tac-Tu.md`.
- [ ] **LOOP SỬA CHỮA:** Tự sửa theo Critic -> Chấm lại UNTIL **VERDICT = ĐẠT ✅**.

#### BƯỚC 5: XUẤT BẢN & LƯU TRỮ
- [ ] IF chưa có **VERDICT = ĐẠT ✅** -> QUAY LẠI 4.6.
- [ ] **TỔNG BIÊN TẬP:** rà lần cuối theo `cong-kiem-chat-luong.md` Lớp 2 (đặc biệt **Hướng-tương-lai** — còn cụm hoài cổ sáo rỗng thì trả lại sửa) + cổng bằng chứng `references/checklist-truoc-khi-trinh.md` + đối chiếu `checklist-hook.md` cho hook đã chốt.
- [ ] Hỏi lưu file -> Nếu có, lưu vào `scripts-output/` và viết Caption theo **`references/khung-caption.md`** (5 tầng: lặp hook · đặt tên ý tưởng · mồi bình luận · khai triển thoáng · chốt 1 CTA). 🔴 Tầng 3 (mồi bình luận) **chỉ dùng khi có tài liệu THẬT** & **KHÔNG dùng ở tuyến Lạnh**.
- [ ] **🗺️ GHI SỔ KHAI THÁC (BẮT BUỘC sau khi lưu bài — thiếu = chưa xong việc):**
  1. Mở wiki NGUỒN → mục `## 🗺️ KHAI THÁC`: đổi trạng thái góc vừa viết → ✅ + ghi TÊN FILE bài (`scripts-output/...`).
  2. Mở `wiki/_INDEX.md` → cột **KT** của dòng wiki đó: ⬜ → 🔶 (mới khai thác một phần) hoặc ✅ (đã khai thác nhiều/gần hết).
