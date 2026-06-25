import streamlit as st
st.image("free.jpg")
# Tiêu đề app
st.title("APP CHO VAY ONLINE KHÁCH HÀNG CÁ NHÂN_VÕ THỊ BÍCH LOAN_ĐỀ TÀI 9")
import streamlit as st
st.markdown("---")

# Tạo 2 cột để chia giao diện
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 THÔNG TIN KHOẢN VAY")
    
    # Nhập thông tin vay
    STV = st.number_input(
        "Số tiền muốn vay (Triệu đồng)",
        min_value=0.0,
        step=10.0,
        format="%.2f",
        help="Nhập số tiền bạn muốn vay"
    )
    
    TGV = st.number_input(
        "Thời gian vay (Số năm)",
        min_value=1,
        max_value=30,
        step=1,
        help="Nhập thời gian vay tính theo năm"
    )
    
    LSV = st.number_input(
        "Lãi suất cho vay (Số thập phân)",
        min_value=0.0,
        max_value=1.0,
        step=0.001,
        format="%.3f",
        help="Nhập lãi suất dạng số thập phân (ví dụ: 0.05 = 5%)"
    )
    
    st.subheader("👤 THÔNG TIN KHÁCH HÀNG")
    
    TN = st.number_input(
        "Thu nhập hàng tháng (Triệu đồng/tháng)",
        min_value=0.0,
        step=1.0,
        format="%.2f",
        help="Nhập tổng thu nhập hàng tháng của gia đình"
    )
    
    SNTGD = st.number_input(
        "Số người trong gia đình",
        min_value=1,
        max_value=20,
        step=1,
        help="Nhập số người phụ thuộc trong gia đình"
    )

with col2:
    st.subheader("💰 THÔNG TIN TÀI SẢN")
    
    GTTSDB = st.number_input(
        "Giá trị tài sản đảm bảo (Triệu đồng)",
        min_value=0.0,
        step=10.0,
        format="%.2f",
        help="Nhập giá trị tài sản dùng để đảm bảo khoản vay"
    )
    
    st.subheader("📊 THÔNG TIN BỔ SUNG")
    
    PTMC = st.number_input(
        "Số tiền phải trả cho khoản vay cũ (Triệu đồng)",
        min_value=0.0,
        step=1.0,
        format="%.2f",
        help="Nhập số tiền đang phải trả hàng tháng cho các khoản vay cũ"
    )
    
    STKKH = st.number_input(
        "Số tuổi khách hàng",
        min_value=0,
        max_value=120,
        step=1,
        help="Nhập tuổi của khách hàng"
    )

# Nút tính toán
st.markdown("---")
if st.button("🔄 TÍNH TOÁN & PHÊ DUYỆT", type="primary", use_container_width=True):
    try:
        # Tính toán các chỉ số
        CPSH = 5  # Chi phí sinh hoạt tối thiểu mỗi người (Triệu đồng)
        
        # Tính số tiền phải trả hàng tháng
        PTMM = (STV / (TGV * 12)) + (STV * (LSV / 12))
        
        # Tính DTI (Debt-to-Income Ratio)
        if (TN - SNTGD * CPSH) > 0:
            DTI = (PTMC + PTMM) / (TN - SNTGD * CPSH)
        else:
            DTI = float('inf')
        
        # Tính LTV (Loan-to-Value Ratio)
        if GTTSDB > 0:
            LTV = STV / GTTSDB
        else:
            LTV = float('inf')
        
        # Hiển thị kết quả
        st.markdown("---")
        st.subheader("📊 KẾT QUẢ PHÂN TÍCH")
        
        # Tạo 3 cột để hiển thị kết quả
        col3, col4, col5 = st.columns(3)
        
        with col3:
            st.metric(
                label="📈 Chỉ số DTI",
                value=f"{DTI*100:.2f}%",
                help="Tỷ lệ nợ trên thu nhập (phải ≤ 70%)"
            )
        
        with col4:
            st.metric(
                label="📉 Chỉ số LTV",
                value=f"{LTV*100:.2f}%",
                help="Tỷ lệ vay trên giá trị tài sản (phải ≤ 70%)"
            )
        
        with col5:
            st.metric(
                label="👤 Độ tuổi",
                value=f"{STKKH} tuổi",
                help="Độ tuổi phải từ 18 đến 70"
            )
        
        # Điều kiện phê duyệt
        st.markdown("---")
        st.subheader("✅ KẾT QUẢ PHÊ DUYỆT")
        
        # Kiểm tra điều kiện
        condition1 = DTI <= 0.7
        condition2 = LTV <= 0.7
        condition3 = 18 <= STKKH <= 70
        
        # Hiển thị từng điều kiện
        col6, col7, col8 = st.columns(3)
        
        with col6:
            if condition1:
                st.success("✅ DTI ≤ 70%")
            else:
                st.error("❌ DTI > 70%")
        
        with col7:
            if condition2:
                st.success("✅ LTV ≤ 70%")
            else:
                st.error("❌ LTV > 70%")
        
        with col8:
            if condition3:
                st.success("✅ 18 ≤ Tuổi ≤ 70")
            else:
                st.error("❌ Tuổi không hợp lệ")
        
        # Kết quả cuối cùng
        st.markdown("---")
        if condition1 and condition2 and condition3:
            st.success("🎉 CHÚC MỪNG! BẠN ĐƯỢC CHO VAY")
            st.balloons()
        else:
            st.error("❌ RẤT TIẾC! BẠN KHÔNG ĐƯỢC CHO VAY")
            st.snow()
        
        # Hiển thị chi tiết tính toán
        with st.expander("📋 Xem chi tiết tính toán"):
            st.write(f"**Số tiền phải trả hàng tháng:** {PTMM:.2f} triệu đồng")
            st.write(f"**Thu nhập sau chi phí sinh hoạt:** {TN - SNTGD * CPSH:.2f} triệu đồng")
            st.write(f"**Tổng nợ hàng tháng:** {PTMC + PTMM:.2f} triệu đồng")
            st.write(f"**Chi phí sinh hoạt mỗi người:** {CPSH} triệu đồng")
            
    except ZeroDivisionError:
        st.error("⚠️ Lỗi: Không thể chia cho 0. Vui lòng kiểm tra lại dữ liệu nhập.")
    except Exception as e:
        st.error(f"⚠️ Đã xảy ra lỗi: {str(e)}")

# Footer
st.markdown("---")
st.caption("💡 Hệ thống phê duyệt khoản vay tự động - Dựa trên DTI, LTV và độ tuổi")
st.caption(f"📅 Phiên bản 1.0 - {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
