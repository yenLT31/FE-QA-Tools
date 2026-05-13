import streamlit as st
import pandas as pd
# Import hàm từ thư mục scripts
from scripts.extract_pdf import extract_from_pdf 

st.title("📄 Tool Trích xuất Quyết định")

uploaded_file = st.file_uploader("Chọn file PDF Quyết định", type="pdf")

if uploaded_file is not None:
    # Xử lý trích xuất
    with st.spinner('Đang đọc dữ liệu PDF...'):
        data = extract_from_pdf(uploaded_file)
        df = pd.DataFrame(data)
        st.success("Trích xuất thành công!")
        st.dataframe(df) # Hiển thị dữ liệu lên web
        
        # Nút tải Excel
        st.download_button("Tải file Excel về máy", data=df.to_csv().encode('utf-8'), file_name="Ket_qua.csv")
