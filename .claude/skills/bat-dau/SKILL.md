---
name: bat-dau
description: Phỏng vấn setup brand MỚI. Khi người dùng gõ /bat-dau — đóng vai người phỏng vấn, hỏi lần lượt 9 câu định nghĩa khách hàng mục tiêu + vị thế thương hiệu (từ references/setup-audience.md), HỎI TỪNG CÂU MỘT. Sau 9 câu, tổng hợp chân dung khách + ghi vào _private/brand/<brand>/ho-so-khach-hang.md, cập nhật vị trí voice vào voice-profile.md, RỒI tự sinh content-pillars.md (5-8 trụ cột) + HỎI mục tiêu chiến dịch (Gieo hạt/Nuôi dưỡng/Thu hoạch) để sinh ma-tran-30-ngay.md theo Tỷ lệ Động (ToFu/MoFu/BoFu) + map format theo phễu. Dùng cho brand MỚI chưa có hồ sơ.
---

# /bat-dau — PHỎNG VẤN SETUP BRAND

Người dùng gõ `/bat-dau`. Bạn đóng vai **người phỏng vấn** để định nghĩa khách hàng mục tiêu + vị thế thương hiệu cho một brand, rồi ghi vào hồ sơ.

## BƯỚC 0 — XÁC ĐỊNH BRAND + 🔴 HÀNG RÀO AN TOÀN (làm TRƯỚC, bắt buộc)
1. Hỏi: **"Mình setup cho thương hiệu nào? (tên brand, vd: kim-anh — dùng chữ thường, có gạch nối)"**. Đó là folder `_private/brand/<brand>/`.
2. 🔴 **CHỐNG GHI ĐÈ MẤT DỮ LIỆU — kiểm `_private/brand/<brand>/ho-so-khach-hang.md`:**
   - File **CHƯA tồn tại** hoặc chỉ là template rỗng → brand MỚI, đi tiếp bình thường.
   - File **ĐÃ CÓ dữ liệu thật** (vd có "48 nỗi đau", bảng PAIN×JOB×GAIN, "VALUE MAP", hoặc dài > ~30 dòng) → **DỪNG. CẢNH BÁO người dùng:**
     > *"⚠️ Brand `<brand>` đã có hồ sơ khách hàng với dữ liệu thật (X dòng). Chạy /bat-dau sẽ GHI ĐÈ và làm MẤT toàn bộ (nỗi đau, Value Map…). Anh/chị chắc chắn muốn ghi đè không? (có/không)"*
     - Chưa xác nhận "có" → **KHÔNG ghi gì cả.** Gợi ý: nếu chỉ muốn chỉnh audience → sửa tay, đừng chạy /bat-dau.
     - Xác nhận "có" → **BACKUP trước** (copy file cũ sang `_backup/bat-dau-<ngày>/`) rồi mới ghi đè.
3. **KHÔNG bao giờ ghi đè khi chưa qua hàng rào này.**

## BƯỚC 1 — PHỎNG VẤN 9 CÂU (hỏi TỪNG CÂU MỘT)
- Mở `.claude/skills/viet-script/references/setup-audience.md` — **dùng đúng 9 câu trong đó** (1 nguồn sự thật, không tự chế thêm/bớt câu).
- 🔴 **QUY TẮC CỨNG:** hỏi **1 câu → CHỜ người dùng trả lời → mới hỏi câu kế.** TUYỆT ĐỐI không hỏi dồn 9 câu cùng lúc, không tự trả lời thay.
- Câu nào người dùng chưa rõ → gợi ý ví dụ (mỗi câu trong setup-audience đã có ghi chú), nhưng **để họ tự quyết**, không bịa thay.
- Câu 9 (vị thế brand: Trên / Cạnh / Đồng cấp) = **vị trí VOICE** — ghi nhớ để cập nhật `voice-profile.md`.

## BƯỚC 2 — TỔNG HỢP CHÂN DUNG
- Viết **đoạn chân dung ngắn** theo mẫu ở `setup-audience.md` mục "Kết quả":
  > *Khách mục tiêu: [giới tính] [tuổi], [nghề]. Loay hoay: [PAIN]. Khao khát sâu: [GAIN]. Nỗi sợ lõi: [cảm xúc]. Gu: [xem/đọc gì]. Ngôn ngữ: [tiếng Anh hay không]. Brand ở vị trí [1/2/3] so với khách.*
- Đối chiếu khung 4 nhóm A/B/C/D (`references/audience-va-marketing.md`) → ghi audience chạm nhóm nào → sắc thái ngôn ngữ.
- 🔴 **Chỉ tổng hợp từ câu trả lời THẬT của người dùng** — không thêm nỗi đau/khao khát họ chưa nói (chống bịa).

## BƯỚC 3 — GHI FILE
1. **`_private/brand/<brand>/ho-so-khach-hang.md`:**
   - Brand MỚI (file chưa có) → **tạo file**, ghi đoạn chân dung + tiêu đề brand. (Hồ sơ chi tiết 48 nỗi đau/PAIN×JOB×GAIN/Value Map sẽ bổ sung sau khi vận hành — KHÔNG bịa ra.)
   - Brand cũ đã backup + xác nhận (Bước 0) → ghi đè.
2. **`_private/brand/<brand>/voice-profile.md` — CẬP NHẬT (KHÔNG đè cả file):**
   - Thêm/cập nhật mục **"Vị trí voice"** = câu 9 (Trên=1 / Cạnh=2 / Đồng cấp=3) + 1 dòng sắc thái tương ứng (xem bảng trong setup-audience).
   - Nếu voice-profile chưa tồn tại (brand mới) → tạo file tối thiểu với mục Vị trí voice; các phần voice khác (mẫu giọng…) hội tụ sau qua `_quy-trinh-tinh-chinh-voice.md`.
   - ⚠️ Brand cũ đã có voice-profile giàu → **CHỈ cập nhật mục Vị trí voice**, không xóa phần khác.

## BƯỚC 3.5 — SINH PILLARS + MA TRẬN 30 NGÀY (BẮT BUỘC — chống "bài lẻ vô hướng")
> Sau khi có hồ sơ → tự sinh khung chiến lược content để mọi bài về sau có chỗ đứng. Chỉ làm cho brand MỚI chưa có 2 file này; brand cũ đã có → HỎI trước khi đè (backup).

1. **Hỏi thêm 1 câu** (nếu chưa rõ từ 9 câu): *"Chuyên môn / lĩnh vực chính của bạn là gì, bạn giúp khách giải quyết điều gì?"* → để Pillar bám đúng chuyên môn CHỦ, không chỉ nỗi đau audience.
2. **Sinh `_private/brand/<brand>/content-pillars.md`** — **5–8 trụ cột**, theo MẪU bảng:
   `| # | Pillar | Nội dung | Nhóm hồ sơ | Nhóm content hay dùng |`
   - Mỗi Pillar = 1 cụm chủ đề khách quan tâm MÀ chủ brand giải được (giao của nỗi đau audience × chuyên môn chủ). Gắn nhóm content hay dùng (Viral/Story/Education/Proof/Conversion).
   - 🔴 Chỉ rút từ dữ liệu THẬT (chân dung + chuyên môn) — KHÔNG bịa pillar ngoài chuyên môn.
3. 🔴🔴 **HỎI MỤC TIÊU CHIẾN DỊCH (Dynamic Ratio — BẮT BUỘC trước khi sinh ma trận; KHÔNG dùng tỷ lệ cứng cũ):**
   In câu hỏi: *"Mục tiêu chiến dịch hiện tại của anh/chị là: **(a) GIEO HẠT** (kéo follower) · **(b) NUÔI DƯỠNG** (thu lead) · **(c) THU HOẠCH** (chốt sales)?"* → phân bổ phễu theo bảng **Tỷ lệ Động**:

   | Mục tiêu | ToFu (kéo) | MoFu (nuôi) | BoFu (chốt) |
   |---|---|---|---|
   | **Gieo hạt** | **80%** | 20% | 0% |
   | **Nuôi dưỡng** | 30% | **60%** | 10% |
   | **Thu hoạch** | 10% | 20% | **70%** |

   🔴 Tỷ lệ THEO mục tiêu người dùng chọn — KHÔNG còn "Viral 30/Story 25…" hay "30 ngày đầu không bán". *(Người đã có nền khách → thường chọn Nuôi/Thu; người mới tinh → Gieo hạt.)*
   🔴🔴 **CHỐT CHẶN MỤC TIÊU = LUẬT TỐI CAO (kỹ sư chốt A, 2026-06-24):** mọi kế hoạch nội dung BẮT BUỘC qua câu hỏi này TRƯỚC khi chia tỷ lệ. **KHÔNG tỷ lệ cứng nào** (kể cả 35/20/20/15/10 trong Data Brand, hay phễu theo tháng) được override Dynamic Ratio. Hệ thống không cứng nhắc — quyền chọn chiến dịch thuộc người dùng.
4. **Sinh `_private/brand/<brand>/ma-tran-30-ngay.md` theo tỷ lệ động + MAP FORMAT THEO PHỄU:**
   - 30 ô phân bổ **ToFu/MoFu/BoFu đúng % mục tiêu đã chọn**. Ghi đầu file: mục tiêu chiến dịch + tỷ lệ đang dùng.
   - Mỗi ô gán **Nhóm format theo phễu** (luật cứng — chi tiết `viet-script` Bước 3.6):
     - **ToFu** (kéo traffic, khơi tò mò/chạm đau) → **Nhóm D (Hook)** hoặc **Nhóm B (Story)**.
     - **MoFu** (nuôi lead, chứng minh chuyên môn) → **Nhóm A (Cấu trúc/How-to)** + **Carousel**.
     - **BoFu** (chốt sales, CTA mạnh) → **Nhóm C (PAS/Copywriting)** hoặc **06 Case Study**.
   - Ô có sẵn: *Ngày · Phễu (ToFu/MoFu/BoFu) · Pillar · Nhóm format · Ý tưởng (ĐỂ TRỐNG) · Kiểu CTA*.
   - 30 ô = 30 chỗ chờ nội dung, không phải lệnh viết hết một lần. **Hết chu kỳ → hỏi lại mục tiêu** → phân bổ chu kỳ kế (mục tiêu leo dần: Gieo → Nuôi → Thu).

## BƯỚC 4 — BÁO CÁO
- Tóm tắt: brand gì, chân dung khách (1–2 câu), vị trí voice, **số Pillar đã sinh + ma trận 30 ô đã dựng**, file đã ghi/tạo.
- Gợi ý bước kế: nạp nguồn / viết bài đầu (skill `viet-script`) → bài sẽ tự xếp vào ô ma trận; offer thì dùng form `_private/brand/khach-hang-mau/thu-thap-offer.md`.

---
> **Ràng buộc:** skill này là markdown thuần, không script. Việc duy nhất tự động = hỏi → tổng hợp → ghi file (qua công cụ sửa file của Claude Code). Không cài/chạy gì ngoài.
