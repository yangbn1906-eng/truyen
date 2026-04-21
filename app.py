import streamlit as st
import os

st.set_page_config(page_title="Reader Pro", layout="centered")

# 1. Danh sách file (đảm bảo đúng tên file trên GitHub)
DANH_SACH_TRUYEN = {
    "Những Ngày Cuối Tháng 4": "Truyen_Full_Nhung_Ngay_Cuoi_Thang_4.txt",
    "Truyện Thứ Hai": "ten_file_2.txt"
}

def lay_noi_dung(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            full_text = f.read()
            # Tách theo dấu gạch ngang bạn đã dùng khi cào
            return [p.strip() for p in full_text.split("---------------") if p.strip()]
    return None

# Sidebar chọn truyện
st.sidebar.title("📚 Thư Viện")
ten_truyen_chon = st.sidebar.selectbox("Chọn bộ truyện:", list(DANH_SACH_TRUYEN.keys()))
file_path = DANH_SACH_TRUYEN[ten_truyen_chon]
data = lay_noi_dung(file_path)

if data:
    # Khởi tạo session state
    if 'chapter_index' not in st.session_state:
        st.session_state.chapter_index = 0

    # Nếu đổi bộ truyện thì reset về trang đầu
    if 'current_story' not in st.session_state or st.session_state.current_story != ten_truyen_chon:
        st.session_state.current_story = ten_truyen_chon
        st.session_state.chapter_index = 0

    # Hàm xử lý khi bấm nút (Tránh xung đột)
    def cong_trang():
        if st.session_state.chapter_index < len(data) - 1:
            st.session_state.chapter_index += 1

    def tru_trang():
        if st.session_state.chapter_index > 0:
            st.session_state.chapter_index -= 1

    # Sidebar: Dùng selectbox hoặc radio nhưng gán chỉ số bằng session_state
    st.sidebar.markdown("---")
    st.session_state.chapter_index = st.sidebar.radio(
        "Mục lục:", 
        range(len(data)), 
        index=st.session_state.chapter_index,
        format_func=lambda x: f"Phần {x + 1}"
    )

    # Hiển thị nội dung
    st.title(f"📖 {ten_truyen_chon}")
    st.markdown(f"### Phần {st.session_state.chapter_index + 1}")
    
    # Hiển thị chữ to, rõ ràng
    st.write(data[st.session_state.chapter_index])

    # Nút bấm chuyển trang
    st.write("---")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.button("⬅️ Trước", on_click=tru_trang, disabled=(st.session_state.chapter_index == 0))

    with col3:
        st.button("Sau ➡️", on_click=cong_trang, disabled=(st.session_state.chapter_index == len(data) - 1))
    
    with col2:
        st.markdown(f"<p style='text-align: center;'>{st.session_state.chapter_index + 1} / {len(data)}</p>", unsafe_allow_html=True)

else:
    st.error("Không tìm thấy file truyện. Hãy kiểm tra tên file trên GitHub.")

# CSS giúp đọc truyện sướng hơn
st.markdown("""
    <style>
    .stMarkdown p { font-size: 21px; line-height: 1.8; font-family: 'Times New Roman', serif; }
    button { height: 50px !important; }
    </style>
    """, unsafe_allow_html=True)
