# CHẾ ĐỘ TÌM VIDEO TỪ KÊNH — discovery (bán tự động)

> Tính năng phụ của skill `viet-script`. Kích hoạt: **"tìm video từ kênh <@user>"** / **"quét kênh <link>"** (+ tùy chọn **"top N"**, mặc định 8).
> Mục đích: vào 1 kênh → lọc video **TỐT NHẤT** (view + tương tác + comment, hợp ngách) → đẩy link vào Notion "Inbox Link" → anh **chạy batch** viết tự động. *(Đây là NỬA ĐẦU; nửa sau là `che-do-batch.md`.)*

## Quy trình
1. **Chọn tool theo nền tảng** (nạp qua ToolSearch khi cần):
   - TikTok → `get_tiktok_user_videos(username, count)`
   - Instagram reels → `get_instagram_user_reels(username, count)`
   - YouTube shorts → `get_youtube_user_shorts(username, count)`
   - Lấy ~30–50 video gần đây (để có cái mà lọc), hoặc theo yêu cầu anh.
   - ⚠️ 3 tool này CHỈ trả **metadata** (title · views · likes · comments · duration · URL). **KHÔNG lấy transcript ở đây** — để batch lo (transcript chỉ qua tokscript).

2. **Lọc TỐT NHẤT** từ list trả về:
   - Xếp hạng theo **views + likes/tương tác + comments** cao.
   - **+ Hợp NGÁCH creator được chọn (bắt buộc):** đọc title/caption → đối chiếu ngách khai trong private workspace hiện tại; không mặc định pillar/audience của brand khác. **Video lạc ngách dù view cao cũng BỎ** (inbox không thành rác).
   - Giữ **top N** (mặc định 8).
   - ⚠️ TikTok trả gộp "stats" — nếu không tách rõ views/like/comment thì xếp theo cái có; thiếu metadata → ghi rõ, **KHÔNG bịa số**.

3. **Đẩy top N vào Notion "Inbox Link"** (ID ở `notion-config.md`): mỗi video 1 dòng, Trạng thái = **"Chờ chạy"**, ghi chú kèm **views/tương tác** (để anh thấy vì sao chọn). Cần connector Notion bật.

4. **Báo bảng tổng** trong chat: video chọn · views/tương tác/comment · 1 dòng lý do hợp ngách.

5. → Anh gõ **"chạy batch"** → viết tự động (xem `che-do-batch.md`).

## Luật
- **Lọc ngách TRƯỚC khi đẩy** — video lạc ngách → bỏ, không đẩy (chống rác inbox).
- **KHÔNG bịa** số view/comment — chỉ dùng số tool trả về. Thiếu → ghi rõ.
- KHÔNG lấy transcript ở discovery (batch lo). Pro/Premium tokscript cần bật; không truy cập kênh → báo anh, không bịa.
- Discovery = ra DANH SÁCH ứng viên để anh duyệt/chạy, KHÔNG phải bản chốt.
