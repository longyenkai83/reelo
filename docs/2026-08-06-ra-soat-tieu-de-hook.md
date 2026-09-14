# RÀ SOÁT TIÊU ĐỀ + HOOK — batch 2026-08-06 · 07 (6 bài)

> Người nhận: **anh Tuấn** (kỹ sư, người duyệt). Nguồn: 4 vịt con Fable rà quy trình (4 lăng kính) + Ban Giám Khảo (BGK) chấm lại từng bài. Ngày lập: 2026-08-06.
> ⚠️ Mọi đề xuất sửa engine trong mục 5 là **ĐỀ XUẤT — chờ anh Tuấn duyệt mới sửa**.

---

## 1. KẾT LUẬN (3 dòng)

1. **Quy trình KHÔNG bị bỏ — nó bị thủng đúng một chỗ: TIÊU ĐỀ là vùng không có gate.** Hook/câu mở 6/6 bài ĐẠT (luật số thật 4B áp nghiêm), chống bịa sạch, chống lặp trục có bằng chứng; nhưng rubric Lớp 3 chỉ có 1 dòng lỏng cho tiêu đề, Critic không bị buộc mở `bo-tieu-de.md`, prompt batch-content.js không nhắc tiêu đề, và chốt "TRÌNH USER CHỌN" biến mất khi chạy batch mà không có gì thay thế.
2. **Mức độ thật: 5/6 bài CẦN SỬA tiêu đề** (BGK chấm lại) — 2 lỗi nặng nhất là nhãn khung "trá hình" (tự chế nhưng khai như khung kho: 4/6 bài) và lấy luật "giữ đáp án" của CÂU MỞ (4B②) áp nhầm sang TIÊU ĐỀ, đẻ ra tiêu đề mơ hồ — chính là bài chị Hiền bắt ("Người khách trong đầu bạn có gương mặt không?").
3. **Bài sạch duy nhất: `2026-08-07-bd-neu-lam-lai-thuong-hieu-ca-nhan.md`** (Khung 14 đúng từng chữ, đúng khuôn CT1 đã ra 360.888 view) — đây là mẫu chuẩn; không có gate nào ÉP 5 bài kia làm như bài này.

---

## 2. BẢNG 6 BÀI

| Bài | Tiêu đề chốt | Tiêu đề | Hook | Nhãn khung bịa (trích nguyên văn) |
|---|---|---|---|---|
| `2026-08-06-r1-ba-cau-truoc-khi-viet.md` | Ba câu phải trả lời được trước khi viết bất kỳ bài nào | 🔴 CẦN SỬA | ✅ ĐẠT | 4/4 nhãn tự chế: "Khung số đóng (Promise + Payoff)" · "Khung thú nhận / nghịch lý" · "Khung chẩn nguyên nhân" · "Khung chi phí thấp" — không nhãn nào có trong khung 1–16 |
| `2026-08-06-r2-viet-cho-mot-nguoi-khong-ton-tai.md` ← **bài chị Hiền bắt** | Người khách trong đầu bạn có gương mặt không? | 🔴 CẦN SỬA | ✅ ĐẠT | "Khung 9 (biến thể tự chế — chạm người đã đánh mất)" — Khung 9 thật là "Cách thật sự [làm X] (khi bạn đã quên/đánh mất…)", tiêu đề chốt không còn thành phần nào của Khung 9; #5 "tự chế — Negative Frame" (Negative Frame là Story Lock mục D, không phải khung tiêu đề) |
| `2026-08-06-bd-ho-so-khach-mot-buoi-sang.md` | Cho đủ: cách mình dựng hồ sơ khách hàng trong một buổi sáng | 🔴 CẦN SỬA | ✅ ĐẠT | #4 "Khung 16 — ẩn dụ (trục sáng tạo)" — Khung 16 thật đòi nghịch-lý-reveal "cái đổi là MÌNH", #4 chỉ là contrast thường; #1 khai Khung 13 nhưng giấu tiền tố "Cho đủ:" nằm ngoài khung |
| `2026-08-07-r1-cong-thuc-mot-cau-dinh-vi.md` | Công thức 1 câu định vị: ba ô, một hơi thở | 🔴 CẦN SỬA | ✅ ĐẠT | #1 "Khung 13 — 'Đây là cách [kết quả] (trong [điều kiện ngắn])'" — tiêu đề không có "cách", không có kết quả khao khát → tự chế khoác nhãn khung thật. (Ghi nhận: #4 khai thẳng "tự chế" — minh bạch nhất batch) |
| `2026-08-07-r2-dung-ve-phia-ai.md` | Người ta nhớ bạn vì bạn đứng về phía ai | 🔴 CẦN SỬA | ✅ ĐẠT | 0/4 nhãn truy được về kho dù bảng tự xưng "(khung `bo-tieu-de.md`)": "Tuyên bố lật niềm tin" · "Nghịch lý" · "Thú nhận" · "Câu hỏi trần" |
| `2026-08-07-bd-neu-lam-lai-thuong-hieu-ca-nhan.md` | Nếu được làm lại thương hiệu cá nhân từ số 0, mình sẽ không bắt đầu bằng việc đăng bài | ✅ ĐẠT | ✅ ĐẠT | Không nhãn tiêu đề bịa (Khung 14 có thật, khớp madlib). Nhãn HOOK ghi sai nguồn: "CT1 lời thú nhận" ghi cột hook-system.md (CT1 là của wiki số thật); "Con số làm mồi" không có trong mục B |

Lỗi phụ đã đẩy Notion: bài bd 06/08 mang tiêu đề có từ nội bộ **đã đẩy Notion** — cần sửa trên Notion sau khi chốt tiêu đề mới.

---

## 3. LỖI GỐC CỦA QUY TRÌNH (gộp, ưu tiên cái ≥2 vịt con cùng chỉ)

### 3.1 — Nhãn khung tiêu đề không truy vết được (4/4 vịt con + BGK cùng chỉ) 🔴
Không luật nào bắt cột "Khung" ghi **SỐ** (1–16) hoặc chữ **TỰ CHẾ**. Hệ quả: 4/6 bài dán nhãn chữ tự nghĩ nghe như khung thật ("Khung chi phí thấp", "Tuyên bố lật niềm tin"), 2 bài mượn số khung "gần giống" (Khung 9, Khung 13, Khung 16) dán cho tiêu đề không mang cấu trúc khung. Tự chế KHÔNG phạm luật (rubric đã nới 2026-07-20) — lỗi là **tự chế đội lốt nhãn kho + không ai kiểm**.

### 3.2 — Luật 4B② "giữ đáp án" của CÂU MỞ bị áp nhầm sang TIÊU ĐỀ (3 vịt con cùng chỉ) 🔴
4B② là luật giữ chân SAU khi bấm; `bo-tieu-de.md` mục PHÂN VAI ghi ngược lại: tiêu đề gặp TRƯỚC khi bấm, nhiệm vụ làm dừng + bấm. Không dòng nào cấm dùng chéo → bài r2 06/08 chốt tiêu đề mơ hồ "có vẻ đúng luật", trong khi 3 phương án gán ĐÚNG khung ngay trong bảng bị loại. Kèm chiều ngược: 2 bài D2 **giấu đáp án ở hook nhưng in nguyên đáp án lên tiêu đề** (r2 07/08 "đứng về phía ai", r1 07/08 "ba ô, một hơi thở") — tự phá vòng lặp mình dựng, Critic chấm từng ô rời rạc nên không thấy 2 dòng đá nhau trong cùng file.

### 3.3 — Mất cân gác: hook có thang 6 ô, tiêu đề có 1 dòng "NÊN" (4/4 vịt con cùng chỉ) 🔴
Câu mở có thang chấm chặt neo số thật (360.888 view); tiêu đề chỉ có "Tiêu đề đã đủ lực chưa? NÊN neo khung… (ghi tên khung)". Không ô "đọc rời có hiểu không", không ô "có từ nội bộ không", không ô đối chiếu madlib. Thợ viết tự dán nhãn → tự tick ✅ → Critic tin lời khai (cùng bệnh vụ chống-lặp-trục 2026-07-20).

### 3.4 — Critic không bị buộc mở `bo-tieu-de.md` (3 vịt con cùng chỉ) 🔴
`critic-ban-giam-khao.md` mục "File chuẩn phải đọc" có 5 file, KHÔNG có `bo-tieu-de.md`; hướng dẫn Lớp 3 nguyên văn chỉ nói HOOK. 6/6 bài qua Critic (nhiều bài "sửa vòng 2") mà không vòng nào bắt được nhãn khống.

### 3.5 — batch-content.js bỏ rơi tiêu đề hoàn toàn (vịt lỗ-hổng-gate, có bằng chứng sống) 🔴
WRITER_PROMPT đòi bảng ≥8 hook nhưng KHÔNG đòi bảng tiêu đề (bài r1 07/08 tự khai "bổ sung BẢNG TIÊU ĐỀ sửa vòng 2" — vòng 1 không có mà vẫn qua); CRITIC_PROMPT thu hẹp Lớp 3 thành "(hook)"; chốt an toàn "TRÌNH USER CHỌN" của SKILL.md biến mất khi batch cách ly, không có gì thay thế. **Tiêu đề là ô duy nhất trong 5 khối gate mất hẳn người kiểm khi batch** — 6 bài này đều đi đường batch → đẩy thẳng Notion.

### 3.6 — Từ nội bộ rò rỉ ra tiêu đề công khai (3 vịt con + BGK cùng chỉ)
"Cho đủ:" là nhãn vai trong file chiến dịch (cùng hệ "**Mở (CT1):**", "**Thân:**") + thuật ngữ pipeline CLAUDE.md, bị bê nguyên vào tiêu đề đăng — bài còn coi là ưu điểm ("giữ nguyên tên ô trong file chiến dịch"). File chiến dịch trộn nhãn chỉ đạo với tiêu đề nháp trong cùng ô lịch, không có quy ước phân biệt.

### 3.7 — Lăng kính hook: 4 lỗ riêng (vịt nhãn-công-thức-hook)
① `hook-system.md` TỰ MÂU THUẪN: mục G.1 đòi "mỗi hook MỘT công thức khác nhau", mục I chỉ đòi "≥5 công thức" — thợ viết chọn chuẩn lỏng. ② Cột "Công thức" không khóa vào 10 tên mục B → Story Lock (D), kỹ thuật mục H, CT1–CT4 ghi lẫn, số công thức đếm phồng (r2 06/08 khai 7). ③ Luật I-4 "không lặp bộ công thức y bài trước" KHÔNG kiểm được vì `_INDEX.md` chưa ghi các bài batch (bd 07/08 tự khai) → 2 reel D2 trùng 7/8 công thức không ai phát hiện. ④ Nhãn "CT1 thú nhận" dán lên hook không thú nhận sai lầm nào (2–3 bài) — nhưng lưu ý: nhãn CT1 này **chép từ brief chiến dịch**, lỗi gốc ở file kế hoạch, không phải bài tự bịa (BGK xác nhận).

### ⚠️ MÂU THUẪN GIỮA CÁC VỊT CON (ghi rõ, không tự hoà giải)
1. **r2 06/08 — số công thức hook:** vịt hook nói bảng chỉ 4 công thức mục B, "khai phồng thành 7" = vi phạm luật I và luật chống bịa; BGK nói "10 hook, 7 công thức, nhãn đối chiếu mục B/D/H đều đúng — ô này ĐẠT thật, không bịa". Gốc mâu thuẫn: đếm CHỈ mục B hay đếm cả D/H — chính là lỗ 3.7② chưa có luật, anh Tuấn cần phân xử chuẩn đếm.
2. **Chất lượng tiêu đề r1 06/08 và r2 07/08:** vịt nhãn-khung xếp 2 tiêu đề này vào nhóm "đọc rời vẫn ĐẠT, nói thẳng ý bài"; vịt tiêu-đề-vs-câu-mở + BGK chấm CẦN SỬA (r2 07/08 lộ trọn đáp án + tuyên ngôn đứng ngoài; r1 06/08 giọng mệnh lệnh đứng ngoài, lệch ngôi với câu mở). Báo cáo này theo verdict BGK (chấm có đối chiếu file), nhưng ghi nhận: 2 tiêu đề này KHÔNG mơ hồ như r2 06/08 — lỗi khác họ.
3. **bd 07/08:** vịt nhãn-khung nói "KHÔNG lỗi"; BGK vẫn ghi 3 lỗi NHẸ (mòn khuôn với bài 22/7 cùng cụm "từ (con) số 0" · mất con số [N] của Khung 14 · vế đắt nằm cuối). Không đổi verdict ĐẠT.
4. **Mức độ r1 06/08:** vịt nhãn-khung chấm VỪA (chỉ lỗi nhãn), BGK chấm NẶNG nhiều lỗi (thêm ngôi kể + lệch câu mở + trượt 3 việc). Chênh do vịt 1 chỉ soi nhãn, BGK soi cả lực tiêu đề.

---

## 4. CHỖ KHÔNG LỖI — đừng sửa nhầm cái đang chạy tốt

1. **CÂU MỞ/HOOK 6/6 bài ĐẠT** cả 3 việc số thật (cảnh cụ thể · giữ đáp án · ngôi "mình") — cả hook của chính bài chị bắt tiêu đề. Hỏng ở TIÊU ĐỀ (tên bài đăng), KHÔNG hỏng ở 3 giây đầu. Đừng đụng vào luật 4B cho câu mở.
2. **Chống bịa (Lớp 1) sạch:** BGK đối chiếu ngẫu nhiên CC1/CC3/CC4, chuỗi nghề — đều khớp kho, không bịa số/mốc/sự kiện nào.
3. **Chống lặp trục chạy thật:** 6/6 bài trích NGUYÊN VĂN dòng `_INDEX` trước khi chốt trục — luật siết 2026-07-20 hoạt động.
4. **Luật cho phép TỰ CHẾ tiêu đề (nới 2026-07-20) không phải thủ phạm** — đừng siết ngược thành "cấm tự chế". Lỗi là tự chế mà dán nhãn kho + không khai.
5. **Máy đẻ phương án tiêu đề vẫn tốt:** ngay bài lỗi nặng nhất, 3/5 phương án không được chốt đều gán ĐÚNG khung và mạnh hơn. Hỏng ở khâu CHỐT + khâu gác, không hỏng ở khâu sinh.
6. **Bài bd 07/08 là mẫu chuẩn** (tiêu đề = câu mở = Khung 14 = khuôn 360.888 view); bảng hook bd 06/08 là mẫu chuẩn khâu hook (9 công thức mục B + ghi lý do loại hook).

---

## 5. ĐỀ XUẤT VÁ GATE — ⚠️ CHỜ ANH TUẤN DUYỆT, chưa sửa engine

### VÁ 1 — `engine/cong-thuc-viral/cong-kiem-chat-luong.md`, Lớp 3, THAY ô tiêu đề hiện tại bằng:
> - [ ] 🔴 TIÊU ĐỀ — KIỂM NHÃN KHUNG, KHÔNG TIN LỜI KHAI (siết 2026-08-06 — anh Tuấn bác loạt tiêu đề batch): ① Bài phải có BẢNG 3–5 TIÊU ĐỀ; mỗi tiêu đề ghi SỐ khung (1–16) theo `bo-tieu-de.md` + trích nguyên văn dòng "Khung:" (madlib) của khung đó. Tiêu đề ngoài kho ghi rõ chữ TỰ CHẾ — CẤM mượn số khung "gần giống" để dán nhãn. ② Critic PHẢI tự mở `bo-tieu-de.md` lắp thử tiêu đề vào madlib đã khai; không lắp vừa = nhãn trá hình = CHƯA ĐẠT (cùng cơ chế "không tin header" của ô chống lặp trục). ③ Tiêu đề chốt (kể cả TỰ CHẾ) phải qua 2 câu Caples: (a) người LẠ đọc riêng tiêu đề có thấy lợi ích/cảnh cụ thể không? (b) có từ nội bộ, tên vai, ẩn dụ chưa giải thích nào người ngoài không hiểu không (vd "Cho đủ:", "ba ô")? Trượt 1 trong 2 = CHƯA ĐẠT. ④ PHÂN VAI: luật câu-mở 4B ("giữ đáp án", "mở vòng lặp") là luật của HOOK — giữ chân SAU khi bấm; CẤM lấy nó biện minh cho tiêu đề mơ hồ — tiêu đề phải làm người ta BẤM (`bo-tieu-de.md` mục PHÂN VAI). ⑤ Đặt tiêu đề chốt CẠNH câu mở chốt — đọc liền hai câu, có đá nhau / lộ nhau không? Reel: mặc định tiêu đề = câu mở (hoặc rút gọn); muốn tách phải ghi 1 dòng lý do trong header.

### VÁ 2 — `.claude/agents/critic-ban-giam-khao.md`:
(a) Mục "File chuẩn phải đọc trước khi chấm" thêm dòng:
> 6. `engine/cong-thuc-viral/bo-tieu-de.md` — kho 16 khung tiêu đề: đối chiếu nhãn khung bài khai, KHÔNG tin lời khai.

(b) Mục "Các lớp CHẤM", sửa bullet Lớp 3 thành:
> Lớp 3 (hook VÀ tiêu đề): kiểm bảng ≥8 hook ghi rõ cột Công thức + chốt 3⭐; VÀ 🔴 tự mở `bo-tieu-de.md` kiểm bảng tiêu đề — nhãn khung có lắp vừa madlib không, tiêu đề chốt có qua 2 câu Caples (lợi ích/cảnh cụ thể · không từ nội bộ) không. Bài tự tick "tiêu đề có khung ✅" mà Critic chưa mở kho đối chiếu = CHƯA chấm xong Lớp 3.

### VÁ 3 — `.claude/workflows/batch-content.js`:
(a) WRITER_PROMPT bước 1 thêm: `Read engine/cong-thuc-viral/bo-tieu-de.md + engine/cong-thuc-viral/hook-system.md.`
(b) WRITER_PROMPT bước 6 sửa thành: `…+ bảng ≥8 hook (trừ Carousel) + bảng 3–5 tiêu đề ghi SỐ khung theo bo-tieu-de.md (ngoài kho ghi TỰ CHẾ, cấm từ nội bộ trong tiêu đề) + trích nguyên văn _INDEX 2 bài.`
(c) CRITIC_PROMPT sửa cụm `Lớp 3 (hook)` thành: `Lớp 3 (hook + TIÊU ĐỀ: tự mở engine/cong-thuc-viral/bo-tieu-de.md kiểm nhãn khung có lắp vừa madlib không; tiêu đề mơ hồ/từ nội bộ/nhãn trá hình = lỗi NẶNG)`.
(d) Thêm cột `tieu_de` vào WRITER_SCHEMA + bảng tổng kết để Main/chị Hiền thấy ngay TIÊU ĐỀ từng bài khi duyệt — **trả lại chốt người mà batch đã làm mất** (thay cho "TRÌNH USER CHỌN").

### VÁ 4 — `engine/cong-thuc-viral/hook-system.md` (lăng kính hook):
(a) Chốt MỘT chuẩn duy nhất giữa G.1 ("mỗi hook một công thức") và I ("≥5 công thức") — hiện tự mâu thuẫn. **Kèm phân xử mâu thuẫn số 1 mục 3:** cột "Công thức" CHỈ nhận 10 tên mục B hay được đếm cả D/H? (đề xuất: chỉ mục B; Story Lock/mục H ghi cột phụ). (b) Thêm ô tự rà "không có dấu — trong MỌI hook của bảng" (luật cứng mục G đang không có ô kiểm). (c) Batch: ghi `_INDEX.md` ngay khi xong nháp HOẶC Orchestrator chuyền bảng công thức hook bài trước cho bài sau (luật I-4 hiện không kiểm được).

### VÁ 5 — `bo-tieu-de.md` + chien-luoc mục 4B, thêm 1 dòng mỗi file:
> Luật giữ-đáp-án CHỈ áp cho câu mở (sau khi bấm). Tiêu đề làm nhiệm vụ ngược lại: nói thẳng bài này về cái gì để người ta bấm.

### VÁ 6 — File chiến dịch (`chien-luoc-workshop-ban-do-thuong-hieu.md` + template sau này):
Quy ước: chữ in đậm có dấu hai chấm trong ô lịch ("**Cho đủ:**", "**Mở (CT1):**") là NHÃN CHỈ ĐẠO, cấm bê vào tiêu đề/thân bài; tiêu đề nháp đặt trong ngoặc kép. Đồng thời sửa nhãn "CT1" ở brief D2 (nguồn gốc lỗi dán nhãn CT1 cho hook không thú nhận).

---

## 6. TIÊU ĐỀ THAY THẾ (khung có thật, từ BGK — chờ chị Hiền/anh Tuấn chọn)

### `2026-08-06-r1-ba-cau-truoc-khi-viet.md`
1. **Khung 16**: "Mình không thiếu khách. Là mình chưa gọi được tên một người khách nào." — đúng ngôi "mình", ăn khớp câu mở tiệm bánh.
2. **Khung 11 (đảo ngôi về mình)**: "Lý do mình đăng đều mà không ai nhắn: mình chưa trả lời nổi ba câu này." — giữ từ khoá "ba câu".
3. **Khung 14**: "Nếu viết lại từ đầu, mình sẽ trả lời ba câu này trước khi gõ chữ đầu tiên." ⚠️ bài bd 07/08 cũng đi Khung 14 — chỉ dùng một trong hai.

### `2026-08-06-r2-viet-cho-mot-nguoi-khong-ton-tai.md` (bài chị Hiền bắt)
1. **Khung 12**: "Chưa biết viết cho ai? Mở lại tin nhắn của một người khách thật" — ưu tiên số 1: khớp hành động ở thân bài.
2. **Khung 9 nguyên khung**: "Cách gọi lại đúng tên một người khách thật (khi bạn đã quên mất gương mặt của họ)" — giữ hệ hình ảnh "gương mặt" mà vẫn hứa cách làm.
3. **Khung 11 đảo ngôi**: "Mình từng viết cả năm cho một người không tồn tại" — mạnh về nỗi đau, đúng Luật 1 ngôi kể.

### `2026-08-06-bd-ho-so-khach-mot-buoi-sang.md`
1. Sửa tối thiểu: cắt "Cho đủ: " → **"Cách mình dựng hồ sơ khách hàng trong một buổi sáng"** (Khung 13 nguyên khung). ⚠️ Nhớ sửa cả bản đã đẩy Notion.
2. **Khung 12** (sẵn trong bảng, mạnh hơn): "Chưa biết khách của mình là ai? Bắt đầu bằng hai mươi câu họ đã nhắn cho bạn".
3. **Khung 16**: "Bài của bạn không dở đi, là nó chưa có ai đặt" — đúng nghịch-lý-reveal, neo ẩn dụ tiệm bánh.

### `2026-08-07-r1-cong-thuc-mot-cau-dinh-vi.md`
1. **Khung 13** (BGK đề xuất chốt): "Đây là cách giới thiệu mình gọn trong đúng một hơi thở".
2. **Khung 12**: "Chưa biết giới thiệu mình sao cho người ta nhớ? Bắt đầu từ ba dòng này".
3. **Khung 11**: "Lý do người ta gật rồi quên bạn là vì câu giới thiệu của bạn quá dài".

### `2026-08-07-r2-dung-ve-phia-ai.md`
1. **Khung 11**: "Lý do không ai nhớ bạn là vì bạn đang bận chứng minh mình giỏi."
2. **Khung 1**: "Đừng cố giỏi nhất trong ngành của bạn." — khớp câu chốt của bài.
3. **Khung 2**: "Người ta không nhớ bạn vì bạn giỏi, họ nhớ bạn vì bạn đứng cùng phía với họ." — giữ từ khoá chính, bỏ cú pháp lửng lơ kết bằng "ai". (Câu "Người ta nhớ bạn vì bạn đứng về phía ai" chuyển xuống làm câu chốt/overlay cuối — đúng chỗ số thật bảo tuyên ngôn nên nằm.)

### `2026-08-07-bd-neu-lam-lai-thuong-hieu-ca-nhan.md` — ĐẠT, không bắt buộc sửa
Gợi ý nâng (Khung 14 + trả lại con số, né mòn khuôn với bài 22/7): "Nếu được làm lại thương hiệu cá nhân từ số 0, mình sẽ trả lời năm câu hỏi này trước khi đăng bài đầu tiên".
