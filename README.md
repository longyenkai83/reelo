### 🚀 CẨM NANG VẬN HÀNH REELO (BẮT ĐẦU TỪ ĐÂY)
Biến 1 nguồn (video/sách/insight) thành content tiếng Việt ở 3 định dạng: Reel, Video dài, Carousel. Nền tảng là tâm lý hành vi: chọn đúng cơ chế tâm lý theo nỗi đau người xem rồi mới viết.

#### ⚙️ CÀI ĐẶT 3 BƯỚC (Dành cho máy mới)
1. **Mở folder:** Mở chính folder `reelo` này trong Claude Code làm nơi làm việc.
2. **Nối Connector:** 
   - **BẮT BUỘC:** `tokscript` (MCP - để lấy transcript video) và `Notion` (để đẩy bài lên bảng duyệt).
   - **TÙY CHỌN:** `Google Drive` (chỉ bắt buộc khi dùng lệnh `/nap-insight` để đọc data thô, nếu không có vẫn viết Reel bình thường).
3. **Setup Brand:** Gõ `"setup brand"` nếu là thương hiệu mới (để khai báo 9 câu hỏi). Với Trịnh Nhi Hiền, bỏ qua bước này.

#### 💬 CÁC LỆNH GÕ HẰNG NGÀY
- `viết reel từ <link>` — (Mặc định) Viết Reel 170-220 chữ từ YouTube/TikTok/IG.
- `viết video dài cho: <link>` — Kịch bản 6 bước + 28 khung (≥1000 chữ, bám gốc).
- `làm carousel từ <link/wiki>` — Rút gọn thành 5-8 slide IG/FB.
- `nạp nguồn: <dán nội dung / link Notion>` — Nạp kiến thức từ bài viết/khóa học.
- `tìm video từ kênh @<tên> → chạy batch` — Quét kênh, lọc top, lưu Notion để viết hàng loạt.
- `/nap-chuyen + <nội dung>` — Lưu nhanh chuyện cá nhân vào kho độc quyền.
*(Lưu ý: Mặc định mỗi lượt chỉ chạy 1 định dạng).*

#### 🔒 5 LUẬT AN TOÀN TOÀN CẦU
1. **Chống bịa đặt:** Chỉ dùng nội dung CÓ trong nguồn. Thiếu thì ghi `[chưa có]`.
2. **Tiêu đề là Vua:** Giữ nguyên Tiêu đề/Hook gốc của nguồn làm trục chính.
3. **Tiếng Việt 100%:** Dịch mượt mà, không dùng văn phong dịch máy.
4. **Transcript chỉ qua tokscript:** Không tự cài Python hay script ngoài.
5. **Con người chốt cuối:** AI chỉ soạn nháp, mọi quyết định lưu/đăng phải do người dùng duyệt.
