import streamlit as st
import os

# Cấu hình giao diện
st.set_page_config(page_title="Kho Truyện Của Tôi", layout="centered")

# 1. Danh sách các file truyện trong thư mục
DANH_SACH_TRUYEN = {
    "Những Ngày Cuối Tháng 4": "Truyen_Full_Nhung_Ngay_Cuoi_Thang_4.txt",
    "|VỤ ÁN CÓ THẬT| HAI THẾ KỶ": "truyen hai the ky.txt" # Thay bằng tên file thực tế của bạn
}

st.sidebar.title("📚 Thư Viện")

# 2. Chọn truyện
ten_truyen_chon = st.sidebar.selectbox("Chọn bộ truyện:", list(DANH_SACH_TRUYEN.keys()))
file_path = DANH_SACH_TRUYEN[ten_truyen_chon]

def lay_noi_dung(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            full_text = f.read()
            # Tách chương theo dấu ngăn cách bạn đã dùng khi cào (--- hoặc ===)
            parts = [p.strip() for p in full_text.split("---------------") if p.strip()]
            return parts
    return None

st.title(f"📖 {ten_truyen_chon}")

data = lay_noi_dung(file_path)

if data:
    # 3. Chọn chương của truyện đã chọn
    st.sidebar.markdown("---")
    index = st.sidebar.radio("Chọn chương:", range(len(data)), 
                             format_func=lambda x: f"Phần {x + 1}")

    # Hiển thị nội dung
    st.markdown(f"### Nội dung Phần {index + 1}")
    st.write(data[index])
else:
    st.error(f"❌ Không tìm thấy file: {file_path}")

# Tùy chỉnh giao diện cho dễ đọc
st.markdown("""
    <style>
    .stApp { background-color: #F5F5DC; } /* Màu nền trang giấy cũ */
    .stMarkdown p { font-size: 20px; line-height: 1.8; color: #2C3E50; }
    </style>
    """, unsafe_allow_html=True)
