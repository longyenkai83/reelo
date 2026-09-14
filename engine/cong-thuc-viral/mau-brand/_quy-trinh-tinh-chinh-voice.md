# SOP — Quy trình tinh chỉnh VOICE cho mỗi brand

> Áp dụng cho MỌI thương hiệu — brand đang chạy hôm nay lẫn khách hàng mai sau. Đây là phần lõi của hệ thống, không gắn riêng ai.

## Nguyên tắc gốc
- Voice (about-me / voice-profile / writing-rules) **không bao giờ đúng từ bản đầu**. Nó **hội tụ dần qua mẫu thật**.
- **"Đô giọng chuẩn" KHÔNG định nghĩa bằng tính từ** (kiểu "ấm", "điềm tĩnh" — mỗi người hiểu một kiểu, máy không đo được).
- **Chuẩn = giống các bài đã được duyệt là ƯNG.** Nên ta định nghĩa giọng bằng **mẫu thật**, rồi rút đặc điểm đo được từ đó.

## Mỗi brand có 1 folder mẫu giọng
Đường dẫn: `_private/brand/<ten-brand>/mau-giong-chuan/`
- Mỗi mẫu = 1 file `.md`, dán nguyên văn bài.
- Ghi ở đầu file mẫu thuộc **loại nào** (giá trị khác nhau):
  - **Loại A — bài THẬT do brand tự viết** (caption/script đã đăng, đã ưng) → **quý nhất**, là giọng gốc 100%.
  - **Loại B — bài AI viết đã được chỉnh tới mức ƯNG** → là "đích" muốn AI nhắm tới.

## Quy trình 3 bước
1. **THU MẪU** — bài nào duyệt "ưng giọng" → bỏ vào `mau-giong-chuan/` của brand. Cứ tích dần.
2. **CHỜ ĐỦ MẪU** — **chưa phân tích khi < 5 bài.** Ít mẫu quá → rút đặc điểm sai, voice lệch. Proof first.
3. **PHÂN TÍCH → CẬP NHẬT** — khi đủ ≥5, phân tích ra **"chân dung giọng" đo được**, rồi ghi vào `voice-profile.md` + `writing-rules.md`:
   - Độ dài câu trung bình (ngắn/vừa/dài), nhịp.
   - Cách mở bài hay dùng · cách chốt/CTA hay dùng.
   - Từ/cụm đặc trưng (hay xuất hiện) · từ/cụm TRÁNH.
   - Tỉ lệ từ đệm, mức độ dứt khoát, ngôi xưng.
   - Lỗi lặp lại cần cấm (ví dụ đã có: không chèn nhãn nhịp nghỉ trong câu).

## Học giọng bằng NHẬP bài mẫu (không chỉ đọc lướt) — học từ Joe Vitale
Joe Vitale: *"Bắt chước văn hay là cách nhanh nhất học viết hay"* — ông học bằng cách **chép tay nguyên văn** bài mình mê, để "cảm được đúng cảm giác tác giả có lúc viết". Áp vào bước PHÂN TÍCH ở trên:
- Với 1–2 bài đắt nhất trong `mau-giong-chuan/`, **nhập lại từng câu** (gõ/chép, không đọc lướt) → cảm **nhịp, chỗ ngắt, từ brand hay dùng**.
- Vừa nhập vừa ghi "cảm giác": câu dài hay ngắn, mở kiểu gì, chốt kiểu gì, từ nào lặp.
- Đây là cách rút **"chân dung giọng" chắc hơn** đọc lý thuyết. Giọng thật của brand > mọi sách bên ngoài.

## Vòng lặp (cách voice càng ngày càng đúng)
Viết bài → người duyệt sửa → bài ưng vào `mau-giong-chuan/` → đủ mẫu thì phân tích lại → cập nhật voice → lần sau viết đỡ sai hơn.
→ Sau vài chục bài, voice **ổn định**. Đó là lúc đủ chín để đóng SOP bán cho khách.

## Cho khách hàng (khi đóng SOP)
SOP bán cho khách **kèm luôn quy trình này** — khách điền about-me/voice thô lúc đầu (sẽ chưa chuẩn, điều đó bình thường), làm vài bài, tích bài ưng, rồi tinh chỉnh. Bán "công cụ + quy trình hội tụ giọng", không bán cái khung rỗng.
