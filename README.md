# Dự đoán giá nhà Việt Nam

## Nội dung

- `housing_model_training.ipynb`: một notebook duy nhất để đọc dữ liệu, tiền xử lý, chia train/test, huấn luyện 5 thuật toán hồi quy phù hợp, vẽ biểu đồ so sánh và lưu mô hình tốt nhất.
- `app.py`: Flask web app responsive cho desktop và mobile.
- `data/vietnam_housing_dataset.csv`: dữ liệu đầu vào.

## Chạy cục bộ

1. Cài thư viện: `pip install -r requirements.txt`
2. Mở và **Run All** file `housing_model_training.ipynb`. Notebook tạo `artifacts/housing_price_model.joblib`.
3. Chạy `python app.py`, sau đó mở `http://127.0.0.1:5000`.

## Triển khai Render

1. Đưa toàn bộ thư mục dự án (bao gồm cả `artifacts/housing_price_model.joblib` sau khi chạy notebook) lên GitHub.
2. Trên Render chọn **New → Blueprint**, kết nối repository và xác nhận cấu hình từ `render.yaml`.
3. Sau khi build xong, Render cung cấp URL ứng dụng. Giao diện tự co giãn cho desktop và mobile.

### Nếu Render báo vượt giới hạn bộ nhớ

`render.yaml` đã cấu hình một Gunicorn worker với `--preload`. Không tăng số worker trên gói RAM nhỏ vì mỗi worker có thể làm tăng đáng kể bộ nhớ khi dùng pandas và scikit-learn. Sau khi cập nhật repository, chọn **Manual Deploy → Deploy latest commit** trên Render.

> Giá dự đoán có đơn vị **tỷ VNĐ** như cột `Price` trong bộ dữ liệu.
