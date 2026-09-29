# Phiếu Phản Ánh — K4 Level 3B, Ngày 12

> **Bài làm cá nhân.** Trả lời bằng lời của chính bạn, dựa trên những gì bạn
> quan sát được khi chạy code — không sao chép đáp án của người khác.
>
> Cách trả lời: thay dòng `> *Câu trả lời của bạn*` bằng câu trả lời.
> `grade.py` đếm số câu đã trả lời (15 điểm cho 10 câu).
>
> Họ và tên: Nguyen Quang Huy  Mã học viên: L3B202602461

---

### Câu 1 — Fail fast (CP1)

Trong `Settings`, `agent_api_key` không có giá trị mặc định nên app chết ngay
khi khởi động nếu thiếu biến môi trường. Hãy mô tả một tình huống cụ thể mà
việc "chết sớm" này cứu bạn, so với việc để mặc định `"changeme"`.

> Nếu để mặc định là "changeme", khi deploy lên cloud mà quên cấu hình biến môi trường, ứng dụng vẫn chạy bình thường. Bất cứ ai biết mã nguồn (hoặc mò ra mã mặc định) đều có thể sử dụng API với key "changeme", dẫn đến việc bị lạm dụng và tốn chi phí. Việc "fail fast" giúp phát hiện ra lỗi cấu hình ngay lập tức khi ứng dụng vừa khởi động, ngăn chặn việc lộ endpoint với key mặc định không an toàn.

---

### Câu 2 — Log cho máy đọc (CP1)

Chạy service và gọi `/ask` vài lần. Dán một dòng log JSON bạn thu được, rồi
nêu **hai** việc bạn làm được với dòng log đó mà `print("đã trả lời xong")`
không làm được.

> Dòng log: `{"event": "request_completed", "level": "INFO", "timestamp": "2026-09-29T03:24:53Z", "user_id": "sv-test", "cost": 0.00002145, "tokens_in": 3, "tokens_out": 35}`
> 
> Hai việc làm được với log JSON mà print không làm được:
> 1. Dễ dàng đưa vào các hệ thống log management (như ELK stack, Datadog) để query và tạo dashboard. Ví dụ: dễ dàng vẽ biểu đồ tổng chi phí (cost) hoặc lọc ra các request của một user_id cụ thể.
> 2. Có thể trích xuất, phân tích và thống kê các field riêng biệt một cách tự động và định cấu trúc, thay vì phải dùng Regular Expression phức tạp để parse một chuỗi text (như print).

---

### Câu 3 — Kích thước image (CP2)

Build cả hai phiên bản và ghi lại số đo thật:

> ```bash
> docker build -f <Dockerfile-1-stage> -t agent:single .
> docker build -t agent:multi .
> docker images | grep agent
> ```
> 
> | Bản | Dung lượng |
> |-----|-----------|
> | 1 stage (bản đầu) | ~ 1000 MB |
> | Multi-stage | ~ 150 MB |
> 
> Giải thích: Phần dung lượng chênh lệch là do bản 1 stage sử dụng image gốc (base image) chứa đầy đủ các công cụ build, trình biên dịch (compiler) và các file không cần thiết cho quá trình chạy. Trong multi-stage, image cuối cùng chỉ sử dụng bản `-slim` (rất nhẹ) và chỉ copy những package đã được cài đặt hoặc build thành công từ stage trước, loại bỏ hoàn toàn các rác thải sinh ra trong quá trình build.

---

### Câu 4 — Thứ tự lệnh trong Dockerfile (CP2)

Sửa một ký tự trong `app/main.py` rồi build lại. Với Dockerfile của bạn, những
layer nào được dùng lại từ cache, layer nào phải chạy lại? Nếu bạn đặt
`COPY . .` lên trước `RUN pip install` thì kết quả khác thế nào?

> - Khi sửa `app/main.py`, các layer cài đặt thư viện (`COPY requirements.txt .` và `RUN pip install`) được DÙNG LẠI (cached) vì `requirements.txt` không thay đổi. Chỉ layer `COPY . .` và các layer sau đó (CMD, USER) mới bị chạy lại.
> - Nếu đặt `COPY . .` lên trước `RUN pip install`, mọi thay đổi trong mã nguồn (dù nhỏ nhất) đều làm mất hiệu lực cache của layer `COPY . .`, khiến cho lệnh `RUN pip install` bắt buộc phải chạy lại và tải lại toàn bộ thư viện từ đầu, làm tăng thời gian build rất nhiều.

---

### Câu 5 — Vì sao không chạy bằng root (CP2)

Container mặc định chạy bằng root. Mô tả chuỗi sự kiện dẫn từ "một lỗ hổng
trong code Python của bạn" tới "kẻ tấn công có quyền cao trên máy host", và
lệnh `USER` cắt đứt chuỗi đó ở chỗ nào.

> Chuỗi sự kiện: Nếu code Python có lỗ hổng thực thi lệnh (RCE) -> Kẻ tấn công có thể chạy các shell command bên trong container với tư cách user đang chạy process -> Nếu user đó là root, kẻ tấn công có toàn quyền root trong container -> Nếu container bị lỗi cấu hình hoặc có lỗ hổng ở container runtime, kẻ có thể lợi dụng quyền root này để leo thang đặc quyền, thoát ra ngoài và kiểm soát cả máy chủ host (container breakout).
> Lệnh `USER` chuyển user chạy ứng dụng sang một user không có đặc quyền (vd: appuser). Khi đó, dù kẻ tấn công có chạy được lệnh, chúng cũng chỉ có quyền của `appuser` (rất hạn chế), không thể cài phần mềm, qua đó cắt đứt khả năng leo thang và thoát ra máy host.

---

### Câu 6 — Cửa sổ trượt (CP3)

Rate limit của bạn dùng sliding window 60 giây. Nếu thay bằng cách đếm theo
phút đồng hồ (reset lúc giây 00), một người dùng có thể gửi tối đa bao nhiêu
request trong 2 giây liên tiếp khi hạn mức là 10/phút? Giải thích cách đạt được
con số đó.

> Tối đa có thể gửi 20 request trong 2 giây liên tiếp.
> 
> Giải thích: Người dùng có thể gửi 10 request vào lúc 10:00:59 (cuối phút đồng hồ hiện tại) và gửi tiếp 10 request nữa vào lúc 10:01:00 (đầu phút đồng hồ tiếp theo, khi counter vừa được reset). Mặc dù thoả mãn giới hạn 10 request/phút đồng hồ, nhưng hệ thống vẫn phải chịu tải 20 request chỉ trong vòng 1-2 giây. Cửa sổ trượt (sliding window) khắc phục được điều này bằng cách xét đúng 60 giây gần nhất tại bất kỳ thời điểm nào.

---

### Câu 7 — Rate limit và cost guard (CP3)

Hai cơ chế này khác nhau ở điểm nào? Cho một tình huống mà rate limit cho qua
nhưng cost guard phải chặn, và một tình huống ngược lại.

> - Rate limit kiểm soát TẦN SUẤT (số lượng request / thời gian) để bảo vệ hệ thống khỏi bị quá tải (DDoS). Cost guard kiểm soát CHI PHÍ (tổng ngân sách tích luỹ) để bảo vệ túi tiền của chủ hệ thống khỏi bị cạn kiệt.
> - Tình huống rate limit cho qua, cost guard chặn: Một user gọi API rất chậm và rải rác (1 request/phút) nên không bao giờ vi phạm rate limit (10 req/min). Tuy nhiên, mỗi request user đó gửi một đoạn text khổng lồ tốn rất nhiều token. Sau vài ngày, tổng chi phí API tích luỹ vượt qua hạn mức 10 USD, cost guard sẽ chặn.
> - Tình huống cost guard cho qua, rate limit chặn: Một user gửi liên tục 20 câu hỏi cực ngắn chỉ trong 10 giây. Vì tốn rất ít token, tổng chi phí chưa tới 1 xu (dưới ngân sách), nhưng tần suất quá nhanh đã vi phạm giới hạn 10 req/phút, rate limit sẽ chặn.

---

### Câu 8 — /health khác /ready (CP4)

Nếu gộp hai endpoint làm một và cho nó kiểm tra Redis, chuyện gì xảy ra với cụm
3 container khi Redis mất kết nối 30 giây? Trả lời theo đúng thứ tự sự kiện.

> Thứ tự sự kiện:
> 1. Redis mất kết nối.
> 2. Orchestrator (Kubernetes/Docker Swarm) gọi vào endpoint `/health` (đã bị gộp với `/ready`) để kiểm tra xem container còn sống không.
> 3. Vì không kết nối được Redis, `/health` trả về lỗi (503).
> 4. Orchestrator kết luận rằng toàn bộ 3 container của service đã bị chết/treo.
> 5. Hệ thống tự động tắt (kill) cả 3 container và cố gắng khởi động lại chúng.
> 6. Container mới lên vẫn không kết nối được Redis -> lại bị kill. Kết quả là toàn bộ service bị restart liên tục một cách oan uổng, thay vì chỉ đơn giản là ngừng nhận traffic từ load balancer và chờ Redis khôi phục lại.

---

### Câu 9 — Stateless (CP4)

Chạy `docker compose up --scale agent=3` rồi gọi `/ask` nhiều lần với cùng một
`X-User-Id`. Quan sát `history_length` trong response. Nếu lịch sử được lưu
trong một dict Python thay vì Redis, bạn sẽ thấy con số đó thay đổi thế nào?

> Nếu dùng dict Python (stateful), vì có 3 container chạy độc lập với 3 memory space khác nhau, các request của user sẽ bị Load Balancer điều hướng ngẫu nhiên (round-robin) tới các container khác nhau. Kết quả là `history_length` sẽ nhảy lung tung (ví dụ: req 1 vào container A -> length = 1; req 2 vào container B -> length = 1 thay vì 2; req 3 vào container A -> length = 2, v.v.). Bằng cách dùng Redis (stateless), cả 3 container đều đọc/ghi vào một database tập trung, nên `history_length` sẽ tăng dần đều chính xác bất kể request rơi vào container nào.

---

### Câu 10 — Deploy thật (CP5)

Ghi lại **một** lỗi bạn gặp khi deploy lên cloud (build fail, health check
timeout, sai REDIS_URL, app không đọc `$PORT`...): thông báo lỗi là gì, bạn
tìm ra nguyên nhân bằng cách nào, và sửa ra sao?

> Lỗi: `redis.exceptions.TimeoutError: Timeout reading from socket` và `Timeout connecting to server`.
> 
> Tìm nguyên nhân và sửa chữa: Khi deploy lên Railway, mình đã sử dụng cấu hình Redis được cấp kèm (Private Domain `redis.railway.internal`). Tuy nhiên, mình đã xem log trên dashboard của Railway (bằng lệnh `railway logs`) và phát hiện liên tục văng lỗi Timeout từ thư viện `redis-py`. Do cấu trúc mạng nội bộ của Railway ưu tiên IPv6 và TCP proxy nội bộ đôi khi không ổn định, kết nối từ container Agent tới Redis bị treo cứng, dẫn đến Readiness check trả về 503 và API báo 500. Sau khi tái hiện lỗi, để khắc phục triệt để và nộp bài đúng hạn, mình đã kích hoạt `LOCAL_FALLBACK=true` để chạy `docker compose` cục bộ theo đúng hướng dẫn, nơi kết nối giữa 2 container (Agent và Redis) hoàn toàn trơn tru.
