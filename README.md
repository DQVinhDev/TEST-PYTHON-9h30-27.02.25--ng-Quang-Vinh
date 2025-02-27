# Hướng dẫn sử dụng ứng dụng Tải lên tệp CSV

## Giới thiệu

Ứng dụng này cho phép người dùng tải lên tệp CSV chứa dữ liệu bán hàng và thực hiện các truy vấn để lấy thông tin từ dữ liệu đã tải lên.

## Cài đặt

1. Đảm bảo rằng bạn đã cài đặt Python và pip.
2. Cài đặt các thư viện cần thiết bằng lệnh:
   ```bash
   pip install Flask pandas
   ```

## Chạy ứng dụng

Để chạy ứng dụng, sử dụng lệnh sau trong terminal:

```bash
python idb_test.py
```

Ứng dụng sẽ chạy trên `http://127.0.0.1:8000`.

## Tải lên tệp CSV

Để tải lên tệp CSV, bạn có thể sử dụng giao diện web hoặc gửi yêu cầu POST đến endpoint `/upload/` với tệp CSV.

### Ví dụ về yêu cầu POST

```http
POST /upload/
Content-Type: multipart/form-data

file: [tệp CSV]
```

## Lấy dữ liệu bán hàng

Sau khi tải lên tệp CSV, bạn có thể lấy dữ liệu bằng cách gửi yêu cầu GET đến endpoint `/sales/` với các tham số truy vấn tùy chọn:

- `start_date`: Ngày bắt đầu (định dạng: YYYY-MM-DD)
- `end_date`: Ngày kết thúc (định dạng: YYYY-MM-DD)
- `region`: Khu vực

### Ví dụ về yêu cầu GET

```http
GET /sales/?start_date=2023-01-01&end_date=2023-12-31&region=Miền Bắc
```

## Phản hồi

Phản hồi từ các yêu cầu sẽ được trả về dưới dạng JSON, bao gồm thông tin về tổng doanh thu, doanh thu trung bình, số lượng giao dịch và các bản ghi phù hợp.

## Lỗi

Nếu có lỗi xảy ra trong quá trình tải lên tệp hoặc truy vấn dữ liệu, ứng dụng sẽ trả về mã lỗi và thông báo lỗi tương ứng.
