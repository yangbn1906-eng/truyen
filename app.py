import streamlit as st
import os

# Cấu hình giao diện
st.set_page_config(page_title="Reader Pro", layout="centered")

# 1. Danh sách file truyện (Đảm bảo tên file khớp với file bạn push lên GitHub)
DANH_SACH_TRUYEN = {
    "Những Ngày Cuối Tháng 4": "Truyen_Full_Nhung_Ngay_Cuoi_Thang_4.txt",
    "Truyện Thứ Hai": "ten_file_2.txt"
}

def lay_noi_dung(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            full_text = f.read()
            # Tách chương theo dấu ngăn cách bạn đã dùng
            return [p.strip() for p in full_text.split("---------------") if p.strip()]
    return None

# Sidebar chọn truyện
st.sidebar.title("📚 Thư Viện")
ten_truyen_chon = st.sidebar.selectbox("Chọn bộ truyện:", list(DANH_SACH_TRUYEN.keys()))
file_path = DANH_SACH_TRUYEN[ten_truyen_chon]
data = lay_noi_dung(file_path)

if data:
    # 2. Khởi tạo session_state để lưu vị trí chương
    if 'chapter_index' not in st.session_state:
        st.session_state.chapter_index = 0

    # Nếu đổi truyện thì reset về chương 0
    if 'current_story' not in st.session_state or st.session_state.current_story != ten_truyen_chon:
        st.session_state.current_story = ten_truyen_chon
        st.session_state.chapter_index = 0

    # Sidebar mục lục (Radio sẽ đồng bộ với session_state)
    index = st.sidebar.radio("Mục lục:", range(len(data)), 
                             index=st.session_state.chapter_index,
                             key="radio_nav",
                             format_func=lambda x: f"Phần {x + 1}")
    
    # Cập nhật index từ radio vào session_state
    st.session_state.chapter_index = index

    # Hiển thị nội dung
    st.title(f"📖 {ten_truyen_chon}")
    st.markdown(f"### Phần {st.session_state.chapter_index + 1}")
    st.write(data[st.session_state.chapter_index])

    # 3. Hàng nút bấm Điều hướng (Next/Prev)
    st.write("---")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.session_state.chapter_index > 0:
            if st.button("⬅️ Trước"):
                st.session_state.chapter_index -= 1
                st.rerun()

    with col3:
        if st.session_state.chapter_index < len(data) - 1:
            if st.button("Sau ➡️"):
                st.session_state.chapter_index += 1
                st.rerun()
    
    with col2:
        st.write(f"Trang {st.session_state.chapter_index + 1} / {len(data)}")

else:
    st.error("❌ Không tìm thấy dữ liệu truyện.")

# CSS cho đẹp
st.markdown("""
    <style>
    .stMarkdown p { font-size: 20px; line-height: 1.8; font-family: 'Georgia', serif; }
    div.stButton > button { width: 100%; border-radius: 10px; background-color: #8b4513; color: white; }
    </style>
    """, unsafe_allow_html=True)
