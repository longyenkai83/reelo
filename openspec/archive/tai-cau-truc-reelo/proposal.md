# ĐỀ XUẤT TÁI CẤU TRÚC REELO — bản để kỹ sư xem xét

> **Trạng thái (cập nhật 2026-07-02):** ✅ **MỨC A ĐÃ ÁP DỤNG** — Đợt 1 (CLAUDE.md) · Đợt 2 (viet-script SKILL + 2 reference luật) · Đợt 3 (writing-rules + cong-kiem + writing-rules-chi-tiet) · dọn root (README/SOP + archive 4 doc trùng). ⏸️ **MỨC B (tách `brand/` ra top-level) — TẠM HOÃN** *(Tuấn chốt 2026-07-02: đổi đồng bộ mọi đường dẫn rủi ro gãy hệ thống cao; ưu tiên giữ hệ chạy ổn định + sinh lời cho Nhi Hiền trước).*
> **Ngày:** 2026-07-01 · **Người soạn:** Vịt Máy (kỹ sư CW) · **Người duyệt:** Tuấn
> **Mục đích file:** gộp toàn bộ chẩn đoán + nguyên tắc + audit + cấu trúc đích vào 1 chỗ để review trước khi viết `specs.md` + `tasks.md`.

---

## 0. Tóm tắt điều hành

Reelo **không sai kiến trúc**, nhưng qua nhiều phiên đã **tích tụ file trùng + dư ngữ cảnh**. Đề xuất: chuẩn hóa theo **5 tầng dữ liệu** (chuẩn Agent Skills của Anthropic + 8 nguyên lý CW), tách rạch ròi **engine ↔ brand** (tư duy nhân bản), làm bằng **OpenSpec từng cụm** (Tuấn duyệt từng bước). **Audit 7 skills cho thấy KHÔNG bỏ/gộp skill nào** — bloat nằm ở docs trùng + file lõi phình, không ở số skills.

---

## 1. Bối cảnh & vấn đề

- Reelo chạy trong Claude Code (folder), phục vụ 1 brand: **Trịnh Nhi Hiền**.
- Sau nhiều phiên: file tổng quan trùng nhau, file lõi phình, kho lẫn tầng → "dư ngữ cảnh" mỗi phiên.
- Tuấn muốn: cấu trúc **khoa học, đúng chuẩn Claude/Anthropic**, và **thiết kế để nhân bản** cho brand khác nếu thành công.

**Tham chiếu mẫu:** skill `blog-da-tac-tu` (Tuấn cấp) — 1 SKILL.md hub gọn + `references/` lean-load + `scripts/` + tách data riêng `_private/`. Đây là mẫu kết cấu tốt để soi (chỉ tham khảo, Reelo vẫn là **project** không phải skill).

---

## 2. Năm nguyên tắc kiến trúc (Tuấn đã chốt)

| # | Nguyên tắc | Nghĩa |
|---|---|---|
| **NT1** | Reelo = **PROJECT** (không phải skill) | Hub `CLAUDE.md` + folders; skill nằm *trong* project |
| **NT2** | Tách **ENGINE ↔ BRAND** ngay từ đầu | Engine (skill·luật·công thức·format) dùng chung; data Hiền = 1 instance `brand/nhi-hien/`. Nhân bản sau = thêm `brand/<tên>/`, không đụng engine |
| **NT3** | **Obsidian-friendly** | Cây + tên gọn/rõ, nhìn đẹp trong Obsidian; giữ `.obsidian/` |
| **NT4** | **OpenSpec = cổng kiểm soát của Tuấn** | Mọi đổi lõi qua OpenSpec (đề xuất→duyệt→apply→archive). Cách người no-tech kiểm soát thợ |
| **NT5** | **Giữ giá trị khi gộp** | Audit trước, không gộp mù, không mất năng lực đang chạy |

> 🚩 **Ranh giới NT2 (đã chốt):** *Thiết kế ĐỂ nhân bản được, nhưng CHƯA xây cỗ máy nhân bản.* Làm ngay: ranh giới sạch + quy ước tên. Chưa làm: cơ chế chọn brand / config đa-brand / tự động hóa nhân bản (đợi có brand thật thứ 2). **Làm cho Hiền TRƯỚC.**

---

## 3. Hiện trạng đã chẩn (số liệu quét 2026-07-01)

| Khu | Số .md | Ghi chú |
|---|---|---|
| **Root** | 11 | ⚠️ có **6 file overview trùng nhau**: so-do-reelo · TONG-QUAN-REELO · kien-truc-he-thong · SOP-MASTER · README · 00-BAT-DAU |
| **.claude/skills/** | 7 skills | viet-script · viet-bai · nap-chuyen · nap-insight · don-kho · review-chu-ky · bat-dau |
| viet-script/references/ | 21 | ⚠️ chưa audit trùng |
| viet-script/formats/ | 17 | 17 format bài (01–17) |
| .claude/agents/ | 1 | critic-ban-giam-khao |
| kho-kien-thuc/cong-thuc-viral/ | 11 | + brand-profiles/nhi-hien/ (12 file — **brand chôn sâu ở đây**) |
| kho-kien-thuc/wiki/ | 62 | tri thức (nguội) — để dài vô hại |
| kho-kien-thuc/raw/ | 57 | ⚠️ đáng lẽ chỉ giữ pointer YAML (LUẬT 3 LỚP) → cần dọn |
| scripts-output/ | 48 | bài đã viết |
| carousel-output/ | 13 | |
| **openspec/** | 0 | ⚠️ **rỗng** — kỷ luật có trong hiến pháp mà chưa dùng (change này kích hoạt) |
| .obsidian/ | — | Reelo là vault Obsidian (Tuấn xem cho đẹp cấu trúc) |

Tổng file lõi (không tính wiki/raw/output): ~7.234 dòng.

---

## 4. Mô hình 5 TẦNG (khoa học nền — "progressive disclosure" của Anthropic)

| Tầng | Là gì | Khi nào nạp | Nguyên tắc |
|---|---|---|---|
| **0 · HUB** | `CLAUDE.md` | mỗi phiên | Chỉ hiến pháp gọn + **bản đồ trỏ đi** — KHÔNG chứa hết |
| **1 · DANH TÍNH (tĩnh)** | brand: voice, khách, ma trận, kho chuyện, config | khi viết | Tách khỏi tri thức; ít đổi |
| **2 · NĂNG LỰC (skill)** | `.claude/skills/*` · `.claude/agents/*` | khi trigger | 1 skill = 1 việc; SKILL.md gọn, chi tiết lean-load |
| **3 · TRI THỨC (nguồn)** | `kho-kien-thuc/` (wiki/raw + công thức) | khi tra | Để dài không hại — mở khi cần |
| **4 · TRÍ NHỚ + SẢN PHẨM (động)** | nhật ký, sổ lỗi, outputs | theo việc | Xoay vòng, nén, archive |

> 🔑 **Chỉ Tầng 0–2 cần gọt gọn. Tầng 3–4 để dài vô hại** (lean-load). Đừng phí công gọt kho nguội.

---

## 5. Audit 7 skills → KẾT LUẬN: GIỮ CẢ 7, KHÔNG GỘP

*(Giả định ban đầu "vài skill mỏng, gộp được" — đọc kỹ thì SAI. Cả 7 đều sống, 1 việc rõ, 1 trigger riêng. Gộp = mất giá trị + mờ trigger, ngược chuẩn Anthropic "1 skill = 1 năng lực".)*

| Skill | Vai trò | Xử | Ghi chú |
|---|---|---|---|
| **viet-bai** | Router — cửa vào duy nhất, hỏi menu định dạng | GIỮ | Mỏng *có chủ đích* (tránh trigger nhầm) |
| **viet-script** | Backend lõi — thi công viết (GATE→raw→wiki→Critic) | GIỮ | `disable-model-invocation`. Trái tim Reelo. **SKILL.md 289 dòng — cần lean** |
| **nap-chuyen** | Nạp chuyện/chuyên môn → `kho-cau-chuyen` | GIỮ | 🔑 công cụ **làm đầy E-bank** |
| **nap-insight** | Nạp Pains/Gains từ Google Drive → hồ sơ khách | GIỮ | Phụ thuộc connector Drive |
| **don-kho** | Thủ thư — soi wiki trùng/rác/link gãy (read-only) | GIỮ | Bảo trì kho tri thức |
| **review-chu-ky** | Soi chu kỳ 30 ngày (phễu/format/pillar) | GIỮ | Có 48 bài để review |
| **bat-dau** | Setup brand MỚI (9 câu → hồ sơ + pillar + ma trận) | GIỮ | 🔑 **xương sống NHÂN BẢN** (NT2) |

**Không chồng lấn thật:** nap-chuyen≠nap-insight (khác đích/nguồn/connector) · don-kho≠review-chu-ky (khác đối tượng) · viet-bai/viet-script (cặp router/backend cố ý).

---

## 6. Bloat thật nằm ở đâu (KHÔNG phải ở số skills)

1. **`viet-script/SKILL.md` = 289 dòng nhồi quá nhiều luật** (GATE, MAP phễu, format rules...) → **lean: đẩy luật chi tiết xuống `references/`, giữ SKILL.md làm khung điều phối**.
2. **38 file `references/`(21) + `formats/`(17)** — **CHƯA audit trùng** (nghi có chồng: tuyen-*.md, ky-thuat-ke-chuyen vs story-locks/loops...). → cần audit riêng.
3. **6 root docs trùng** → gom về `docs/` (2 file).
4. **raw/ 57 file** — dọn về đúng LUẬT 3 LỚP (chỉ giữ pointer YAML).

---

## 7. Cấu trúc ĐÍCH đề xuất (theo NT1–NT5)

```
reelo/
├── CLAUDE.md                 # Tầng 0 — hub gọn + bản đồ + nghi thức phiên
├── docs/                     # gộp 6 file overview → 2
│   ├── tong-quan-he-thong.md   (so-do + tong-quan + kien-truc + SOP)
│   └── huong-dan-dung.md       (README + ke-hoach + 00-bat-dau)
├── .claude/                  # Tầng 2 — ENGINE (dùng chung mọi brand)
│   ├── skills/  (viet-bai · viet-script · nap-chuyen · nap-insight · don-kho · review-chu-ky · bat-dau)
│   └── agents/  (critic-ban-giam-khao)
├── brand/                    # Tầng 1 — DANH TÍNH (tách khỏi kho tri thức)
│   └── nhi-hien/               (voice · writing-rules · about-me · ho-so-khach · customer-journey
│                                · ma-tran-30-ngay · chien-luoc · kho-cau-chuyen · kho-cta · notion-config)
├── kho-kien-thuc/            # Tầng 3 — TRI THỨC
│   ├── wiki/ (+ _archive/)     (đã chắt lọc)
│   ├── raw/                    (CHỈ pointer YAML — dọn theo LUẬT 3 LỚP)
│   └── cong-thuc-viral/        (hook-system · bo-tieu-de · kho-hook · nguyen-ly-tam-ly...)
├── san-pham/                 # Tầng 4 — SẢN PHẨM
│   ├── scripts-output/ · carousel-output/
├── nhat-ky/                  # Tầng 4 — TRÍ NHỚ
│   └── nhat-ky-phien.md · so-loi-reelo.md (+ _archive)
└── openspec/                 # NT4 — cổng kiểm soát thay đổi
```

**Điểm mấu chốt NT2:** `.claude/` (engine) và `kho-kien-thuc/` + `cong-thuc-viral/` (tri thức chung) **KHÔNG chứa gì riêng Hiền**; mọi thứ riêng Hiền dồn vào `brand/nhi-hien/`. → Nhân bản v1 = **copy `brand/nhi-hien/` → `brand/<tên-mới>/`** rồi chạy `/bat-dau` khai báo lại, engine không đụng.

> ⚠️ **Chi phí của việc tách `brand/` ra top-level:** phải cập nhật đồng bộ MỌI đường dẫn `brand-profiles/<brand>/...` trong SKILL/CLAUDE (nhiều chỗ). Đây là rủi ro lớn nhất — xem Mức B.

---

## 8. Hai mức THAM VỌNG (Tuấn chọn liều lượng)

| | **Mức A — Gọn có kỷ luật** *(rủi ro thấp)* | **Mức B — Tái tầng đầy đủ** *(đích lý tưởng)* |
|---|---|---|
| Làm gì | Gom 6 doc→2 · lean `viet-script/SKILL.md` · dọn raw · audit+dọn 38 refs/formats · gom outputs & nhật ký | Thêm: **tách `brand/` ra top-level** + đổi cây như mục 7 |
| Đường dẫn | **Giữ nguyên** → không phá reference | **Đổi đồng bộ** mọi path brand → rủi ro cao |
| Nhân bản NT2 | Chưa tách hẳn (brand vẫn trong kho) | Tách sạch engine↔brand |
| Khuyến nghị | **Làm TRƯỚC** | Làm SAU khi A ổn |

---

## 9. Cách làm an toàn (NT4 — OpenSpec)

1. Change này = `openspec/changes/tai-cau-truc-reelo/` gồm **proposal.md** (file này) + sẽ thêm **specs.md** (tiêu chí nghiệm thu) + **tasks.md** (việc từng cụm) khi Tuấn chốt hướng.
2. **Backup mốc mới** trước khi động (ngoài `_backup/` sẵn có).
3. Làm **từng cụm**, mỗi cụm Tuấn duyệt riêng. Không gọt cả kho 1 phát.
4. **Không xóa file** — chỉ gộp/chuyển/archive. Mỗi file gọt xong đối chiếu "còn đủ luật không".
5. Archive xong → gộp delta vào baseline, chuyển change vào `openspec/archive/`.

---

## 10. Quyết định còn MỞ (cần Tuấn + kỹ sư chốt)

1. **Mức tham vọng:** A trước → B sau *(khuyến nghị)* / chỉ A / làm luôn B?
2. **Tách `brand/` ra top-level ngay (Mức B) hay giữ trong kho (Mức A)?** — quyết định lớn nhất, ảnh hưởng nhân bản.
3. **OpenSpec chạy tới đâu:** dựng đủ proposal+specs+tasks cho mỗi change, hay bản gọn?
4. **Naming/Obsidian:** có ràng buộc đặt tên nào để graph Obsidian đẹp không?

---

## 11. Việc AUDIT chưa làm (đề xuất bước kế)

- [ ] **Audit 38 file `references/`(21) + `formats/`(17)** của viet-script — tìm trùng thật (read-only), ra bảng giữ/gộp/bỏ. *(Đây là chỗ bloat lớn chưa soi.)*
- [ ] Đo % trùng thật của 6 root docs (để biết gộp mất gì).
- [ ] Soát voice-profile (398) + writing-rules (394) — 792 dòng, nghi trùng.

---

## Phụ lục — bài học kết cấu từ mẫu `blog-da-tac-tu`

| Nguyên tắc trong mẫu | Áp vào Reelo |
|---|---|
| 1 SKILL.md hub gọn + "bản đồ tài liệu" trỏ đi | CLAUDE.md hub + docs/ (thay 6 file trùng) |
| Lean-load: chi tiết ở `references/` | viet-script/SKILL.md lean, luật xuống references |
| Tách TĨNH/ĐỘNG/YÊU CẦU (VOICE≠KB≠REQUIREMENTS) | brand (tĩnh) ≠ wiki (tri thức) ≠ nhật ký (động) |
| Data riêng tách rời (`_private/`) để share | `brand/<tên>/` tách khỏi engine → nhân bản |
| Schema cho data chảy giữa các bước | GATE 5 khối + Critic (đã có, tương đương) |
```

---

## 12. 🔓 MỞ LẠI MỨC B (2026-07-09) — hướng SẢN PHẨM HÓA ĐỂ BÁN

> **Bối cảnh mới:** Tuấn chốt Reelo là **phần mềm để BÁN ngay từ đầu** (đa mục đích: reel + blog + …, nhân bản đa brand). Mức B từng hoãn 07-02 vì rủi ro path — nay **mở lại** vì có lý do chính đáng: chỉ khi tách sạch **engine (bán) ↔ data riêng (không bán)** thì mới xuất bản cho khách được bằng 1 lệnh. Tuấn đã DUYỆT hướng đi + chọn `_private/` + OpenSpec đầy đủ (2026-07-09).

**Điều chỉnh so với cây đích mục 7 (do mục tiêu BÁN):**

| Mục 7 (bản 07-01) | Bản 07-09 (bán được) | Vì sao |
|---|---|---|
| `brand/nhi-hien/` top-level | **`_private/brand/nhi-hien/`** | `export.sh` xóa sạch `_private/` khi giao khách (theo mẫu `blog-da-tac-tu`) |
| kho-kien-thuc chung | **`_private/kho-kien-thuc/`** (raw+wiki) | Kho đã tiêu hóa = data riêng chị (khóa học + trải nghiệm) → không bán kèm |
| — | **`engine/cong-thuc-viral/`** (tách khỏi brand) | Công thức chung = bán được, KHÔNG dính brand |
| — | **`scripts/export.sh`** + dùng `_mau-brand-profile.md` làm "bản cho khách khai" | Đóng gói bán sạch bằng 1 lệnh |

**Cây đích B (bán được):**
```
reelo/
├── CLAUDE.md · README.md · docs/ · openspec/ · .obsidian/
├── .claude/  skills/ · agents/            # ENGINE (bán)
├── engine/                                 # ENGINE tri thức chung (bán, KHÔNG brand)
│   └── cong-thuc-viral/  (11 công thức + _mau-brand-profile + _quy-trinh-voice + khach-hang-mau)
├── _private/                               # DATA RIÊNG CHỊ HIỀN — export.sh XÓA khi bán
│   ├── brand/nhi-hien/   (voice · writing-rules · about-me · kho-cau-chuyen · ma-tran · notion-config …)
│   └── kho-kien-thuc/    (raw/ + wiki/ — dời CÙNG NHAU, giữ raw↔wiki cạnh nhau)
├── scripts-output/ · carousel-output/      # OUTPUT (đợt B2, xem dưới)
└── scripts/export.sh                        # đóng gói bán, tự loại _private/
```

**Chia 2 đợt (giảm rủi ro, duyệt riêng):**
- **Đợt B1 — LÕI BÁN ĐƯỢC (làm trước):** tách `_private/` (brand + kho-kien-thuc) + `engine/cong-thuc-viral/` + tạo `scripts/export.sh`. Đây là giá trị bán chính.
- **Đợt B2 — GOM OUTPUT (hoãn / tùy chọn):** `scripts-output/` + `carousel-output/` → `san-pham/`. **Khuyến nghị HOÃN:** ~40 refs (phần lớn nằm trong wiki data, không phải luật) — sync sai chỉ gãy link tra cứu, KHÔNG gãy engine; giá trị chỉ thẩm mỹ. Làm sau khi B1 ổn.

> 🔑 **Phát hiện path (quét 2026-07-09):** wikilink `[[raw/...]]` + relative `../raw/` (28+ chỗ trong wiki) **KHÔNG cần sync** nếu raw+wiki dời CÙNG NHAU — Obsidian resolve theo tên file, quan hệ tương đối được bảo toàn. Chỉ **path tuyệt đối từ root** mới cần đổi prefix. Điều này hạ rủi ro Mức B xuống nhiều so với lo ngại 07-02.

