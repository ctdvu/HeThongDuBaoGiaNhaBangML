from pathlib import Path
from functools import lru_cache

import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "artifacts" / "housing_price_model.joblib"
app = Flask(__name__)

NUMERIC_FIELDS = [
    ("Area", "Diện tích", "m²", 1, 10000, 0.1),
    ("Frontage", "Mặt tiền", "m", 0, 100, 0.1),
    ("Access Road", "Đường vào", "m", 0, 100, 0.1),
    ("Floors", "Số tầng", "tầng", 0, 100, 1),
    ("Bedrooms", "Số phòng ngủ", "phòng", 0, 100, 1),
    ("Bathrooms", "Số phòng tắm", "phòng", 0, 100, 1),
]
CATEGORICAL_FIELDS = [
    ("House direction", "Hướng nhà"),
    ("Balcony direction", "Hướng ban công"),
    ("Legal status", "Pháp lý"),
    ("Furniture state", "Nội thất"),
    ("Province", "Tỉnh / thành phố"),
]


@lru_cache(maxsize=1)
def load_bundle():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


def input_defaults():
    values = {key: "" for key, *_ in NUMERIC_FIELDS}
    values.update({key: "Không xác định" for key, _ in CATEGORICAL_FIELDS})
    return values


@app.route("/", methods=["GET", "POST"])
def index():
    bundle = load_bundle()
    values = input_defaults()
    prediction = None
    error = None
    category_values = bundle.get("category_values", {}) if bundle else {}

    if request.method == "POST" and bundle:
        values.update(request.form.to_dict())
        row = {}
        try:
            for key, *_ in NUMERIC_FIELDS:
                raw_value = values[key].strip()
                row[key] = float(raw_value) if raw_value else np.nan
            for key, _ in CATEGORICAL_FIELDS:
                row[key] = values[key] or "Không xác định"

            frame = pd.DataFrame([row], columns=bundle["feature_columns"])
            prediction = max(0, float(bundle["model"].predict(frame)[0]))
        except (TypeError, ValueError):
            error = "Hãy nhập số hợp lệ cho các trường định lượng."
        except Exception:
            error = "Không thể dự đoán với dữ liệu này. Vui lòng thử lại."

    return render_template(
        "index.html",
        bundle=bundle,
        numeric_fields=NUMERIC_FIELDS,
        categorical_fields=CATEGORICAL_FIELDS,
        category_values=category_values,
        values=values,
        prediction=prediction,
        error=error,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
