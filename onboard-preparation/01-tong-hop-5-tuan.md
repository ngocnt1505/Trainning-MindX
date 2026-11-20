# Tổng hợp 5 tuần training

Nguyễn Thúy Ngọc · 20/11/2026

## 5 tuần đã học gì

| Tuần | Làm gì | Bài học chính |
| --- | --- | --- |
| 1 | Nghiên cứu TDD cùng AI ([Report](../week-1-tdd-research/Report.md)) | Red → Green → Refactor; test là cách kiểm chứng code AI viết; luôn hỏi lại và chạy lại, không tin ngay câu trả lời của AI |
| 2 | CLI `tickets` bằng TDD, JavaScript ([docs](../week-2-3-cli/docs/week-2-tickets/)) | Viết test list trước, quyết định thiết kế ghi lại thành văn bản, chia tầng `commands → service → storage`, commit nhỏ theo `test:` / `feat:` / `refactor:` |
| 3 | CLI `kb` gọi Knowledge Base qua Mock client và HTTP client, TypeScript ([docs](../week-2-3-cli/docs/week-3-kb/)) | Code nghiệp vụ chỉ phụ thuộc vào một **interface** `client`; đổi Mock ↔ HTTP không phải sửa nghiệp vụ. Đây chính là ý tưởng của Hexagonal (ports & adapters) |
| 4 | Xử lý 6 scenario ticket trên Odoo Helpdesk ([README](../week-4-odoo-helpdesk/README.md)) | Quy trình 7 bước; phân loại Class of Service (Standard / Priority / Expedite / Fixed Deadline); ACK đúng hạn, **hẹn mốc cập nhật chứ không hứa giờ sửa xong**; viết email theo đúng người đọc |
| 5 | Phân tích 118 ticket thật + login bot tích hợp Odoo ([README](../week-5-analysis-automation/README.md)) | Tìm vấn đề lặp lại bằng số liệu (top 5 chiếm 72 %); chọn 1 vấn đề để tự động hóa; lập kế hoạch giảm ticket có chỉ số đo được |

Kết luận:

1. **Có số liệu thì mới có đề xuất.** Ở tuần 5, kế hoạch đáng tin vì mọi hành động đều dẫn về một con số trong `analysis.md`.
2. **Tách nghiệp vụ khỏi hệ thống bên ngoài.** Tuần 3 (Mock/HTTP) và tuần 5 (HR/LMS/Odoo client có bản InMemory/DryRun) đều nhờ tách như vậy mà test được khi chưa có hệ thống thật.
3. **Giao tiếp là một phần của việc xử lý ticket.** Ticket giải quyết đúng nhưng không báo người dùng đúng lúc thì vẫn coi là xử lý kém.
