import streamlit as st
import os

st.set_page_config(page_title="Reader Pro", layout="centered")

# Hàm cuộn lên đầu trang bằng JavaScript
def scroll_to_top():
    st.components.v1.html(
        """
        <script>
            // Chờ 100ms để Streamlit render nội dung mới xong
            setTimeout(function() {
                // Cuộn cả trang web chính lên đầu
                window.parent.scrollTo({
                    top: 0,
                    left: 0,
                    behavior: 'smooth'
                });
            }, 100);
        </script>
        """,
        height=0,
    )


# --- PHẦN LOGIC TRUYỆN (Giữ nguyên từ bản trước) ---
DANH_SACH_TRUYEN = {
    "Những Ngày Cuối Tháng 4": "Truyen_Full_Nhung_Ngay_Cuoi_Thang_4.txt",
    "|VỤ ÁN CÓ THẬT| HAI THẾ KỶ": "truyen hai the ky.txt" # Thay bằng tên file thực tế của bạn
}

def lay_noi_dung(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return [p.strip() for p in f.read().split("---------------") if p.strip()]
    return None

st.sidebar.title("📚 Thư Viện")
ten_truyen_chon = st.sidebar.selectbox("Chọn bộ truyện:", list(DANH_SACH_TRUYEN.keys()))
data = lay_noi_dung(DANH_SACH_TRUYEN[ten_truyen_chon])

if data:
    if 'chapter_index' not in st.session_state:
        st.session_state.chapter_index = 0

    # Hàm xử lý khi bấm nút + gọi lệnh cuộn trang
    def cong_trang():
        if st.session_state.chapter_index < len(data) - 1:
            st.session_state.chapter_index += 1
            scroll_to_top() # Cuộn lên khi qua trang mới

    def tru_trang():
        if st.session_state.chapter_index > 0:
            st.session_state.chapter_index -= 1
            scroll_to_top() # Cuộn lên khi về trang trước

    # Sidebar: Cập nhật index
    st.session_state.chapter_index = st.sidebar.radio(
        "Mục lục:", range(len(data)), 
        index=st.session_state.chapter_index,
        format_func=lambda x: f"Phần {x + 1}"
    )

    st.title(f"📖 {ten_truyen_chon}")
    st.markdown(f"### Phần {st.session_state.chapter_index + 1}")
    st.write(data[st.session_state.chapter_index])

    st.write("---")
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        st.button("⬅️ Trước", on_click=tru_trang, disabled=(st.session_state.chapter_index == 0))
    with col3:
        st.button("Sau ➡️", on_click=cong_trang, disabled=(st.session_state.chapter_index == len(data) - 1))
    with col2:
        st.markdown(f"<p style='text-align: center;'>{st.session_state.chapter_index + 1} / {len(data)}</p>", unsafe_allow_html=True)
else:
    st.error("Không tìm thấy file truyện.")

st.markdown("<style>.stMarkdown p { font-size: 21px; line-height: 1.8; }</style>", unsafe_allow_html=True)
