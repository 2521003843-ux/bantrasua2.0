import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG (Đầu tiên)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Autumn Tea & Bakery Lounge 🍁",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. HÀM TƯƠNG THÍCH BẢN STREAMLIT
# ---------------------------------------------------------
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

def safe_toast(msg, icon="🍁"):
    if hasattr(st, "toast"):
        st.toast(msg, icon=icon)
    else:
        st.success(f"{icon} {msg}")

# ---------------------------------------------------------
# 3. CUSTOM CSS: BANNER ẢNH NỀN & CHỦ ĐỀ MÙA THU 🍁
# ---------------------------------------------------------
st.markdown("""
    <style>
    :root {
        --autumn-orange: #D96B27;
        --autumn-brown: #5C2C16;
        --autumn-gold: #F59E0B;
        --autumn-bg: #FDFBF7;
    }

    .stApp {
        background-color: var(--autumn-bg);
    }

    /* BANNER TIÊU ĐỀ CÓ ẢNH NỀN TONE MÙA THU CỦA QUÁN */
    .hero-banner-img {
        position: relative;
        background-image: linear-gradient(rgba(44, 19, 9, 0.75), rgba(92, 44, 22, 0.85)), 
                          url('https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        border-radius: 16px;
        padding: 40px 20px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    }
    
    .hero-banner-img h1 {
        color: #FFFFFF !important;
        font-family: 'Georgia', serif;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 8px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .hero-banner-img p {
        color: #FBBF24;
        font-size: 1.2rem;
        margin: 0;
        font-style: italic;
        font-weight: 500;
    }

    /* Card Sản Phẩm */
    .product-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 10px;
        border: 1px solid #E2D9CC;
        box-shadow: 0 4px 10px rgba(0,0,0,0.04);
        text-align: center;
        transition: transform 0.2s;
    }
    .product-card:hover {
        transform: translateY(-4px);
        border-color: var(--autumn-orange);
    }
    
    /* Hóa đơn Vintage */
    .bill-box {
        background-color: #FFFFFF;
        border: 2px dashed var(--autumn-orange);
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.06);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. KHỞI TẠO SESSION STATE (DỮ LIỆU BÁN HÀNG)
# ---------------------------------------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []
if "invoice_paid" not in st.session_state:
    st.session_state.invoice_paid = False
if "sales_history" not in st.session_state:
    st.session_state.sales_history = [
        {
            "Thời gian": "17/10/2026 14:15:20",
            "Khách hàng": "Anh Minh",
            "Loại món": "Trà sữa + Bánh",
            "Số lượng": 3,
            "Tạm tính": 154000,
            "Giảm giá": 5,
            "Thành tiền": 146300,
            "Chi tiết": "Trà Sữa Quế Hoa (1), Bánh Mì Bơ Tỏi (1), Latte Hạt Dẻ (1)"
        },
        {
            "Thời gian": "17/10/2026 15:30:10",
            "Khách hàng": "Chị Hoàng Yến",
            "Loại món": "Trà trái cây",
            "Số lượng": 1,
            "Tạm tính": 55000,
            "Giảm giá": 10,
            "Thành tiền": 49500,
            "Chi tiết": "Trà Hồng Trà Táo Mật Maple (1)"
        }
    ]

# ---------------------------------------------------------
# 5. DỮ LIỆU MENU CẢI TIẾN (ĐỒ UỐNG & BÁNH MÌ)
# ---------------------------------------------------------
DRINK_MENU = {
    "🍵 Trà Sữa Mùa Thu 🍁": {
        "Trà Sữa Quế Hoa Mùa Thu": {
            "price": 58000,
            "img": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=600&q=80"
        },
        "Latte Hạt Dẻ Nướng Hazelnut": {
            "price": 62000,
            "img": "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?auto=format&fit=crop&w=600&q=80"
        },
        "Trà Sữa Ô Long Lúa Mạch": {
            "price": 52000,
            "img": "https://images.unsplash.com/photo-1485808191679-5f86510681a2?auto=format&fit=crop&w=600&q=80"
        },
        "Trà Sữa Trân Châu Đường Đen Maple": {
            "price": 55000,
            "img": "https://images.unsplash.com/photo-1558857563-b371033873b8?auto=format&fit=crop&w=600&q=80"
        }
    },
    "🍎 Trà Trái Cây Refreshers 🍂": {
        "Trà Hồng Trà Táo Mật Maple": {
            "price": 55000,
            "img": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=600&q=80"
        },
        "Trà Đào Cam Sả Mật Ô Long": {
            "price": 50000,
            "img": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=600&q=80"
        },
        "Trà Dâu Tằm Bạc Hà Mùa Thu": {
            "price": 48000,
            "img": "https://images.unsplash.com/photo-1499638673689-79a0b5115d87?auto=format&fit=crop&w=600&q=80"
        }
    },
    "☕ Coffee & Cream Special 🌾": {
        "Caramel Macchiato Hạt Dẻ": {
            "price": 65000,
            "img": "https://images.unsplash.com/photo-1541167760496-1628856ab772?auto=format&fit=crop&w=600&q=80"
        },
        "Cold Brew Trà Đen Macchiato": {
            "price": 60000,
            "img": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=600&q=80"
        },
        "Matcha Frappuccino Kem Béo": {
            "price": 68000,
            "img": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=600&q=80"
        }
    }
}

BAKERY_MENU = {
    "🥪 Bánh Mì Sandwich Thịt Nướng BBQ": {
        "price": 45000,
        "img": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=600&q=80",
        "desc": "Bánh mì Sandwich giòn kẹp thịt nướng sốt BBQ đậm đà"
    },
    "🧄 Bánh Mì Bơ Tỏi Phô Mai Nướng": {
        "price": 38000,
        "img": "https://images.unsplash.com/photo-1573140247632-f8fd74997d5c?auto=format&fit=crop&w=600&q=80",
        "desc": "Bánh mì sốt bơ tỏi thơm lừng ngập tràn phô mai kéo sợi"
    },
    "🥐 Bánh Croissant Bơ Thụy Sĩ": {
        "price": 35000,
        "img": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=600&q=80",
        "desc": "Bánh sừng bò nướng giòn xốp thơm bơ ngậy"
    },
    "🍰 Bánh Tiramisu Hạt Dẻ Autumn": {
        "price": 48000,
        "img": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?auto=format&fit=crop&w=600&q=80",
        "desc": "Bánh Tiramisu mềm mịn thơm vị cà phê & hạt dẻ nướng"
    },
    "🧀 Bánh Cheesecake Chanh Dây": {
        "price": 45000,
        "img": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=600&q=80",
        "desc": "Cheesecake chua ngọt thanh mát hòa quyện vị chanh dây"
    }
}

SIZE_OPTIONS = {"S (Vừa)": 0, "M (Lớn)": 8000, "L (Đặc biệt)": 15000}
MILK_OPTIONS = ["Sữa nguyên kem", "Sữa yến mạch Oat Milk (+10k)", "Sữa hạnh nhân (+10k)", "Không dùng sữa"]
TOPPING_OPTIONS = {
    "Trân châu hoàng gia": 8000,
    "Thạch Quế Hoa": 8000,
    "Thạch Espresso Jelly": 10000,
    "Pudding Trứng Custard": 10000,
    "Kem Cheese Foam": 12000
}
CUSTOMER_TIERS = {
    "Khách vãng lai": 0,
    "Thành viên Maple 🍁 (Giảm 5%)": 5,
    "Thành viên Gold Leaf 🍂 (Giảm 10%)": 10,
    "VIP Autumn Reserve 👑 (Giảm 15%)": 15
}

# ---------------------------------------------------------
# 6. SIDEBAR ĐIỀU HƯỚNG & QUẢN LÝ CA LÀM
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=500&q=80", use_container_width=True)
    st.markdown("<h2 style='text-align:center; color:#5C2C16;'>🍁 AUTUMN LOUNGE</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Menu Điều Hướng Trang
    selected_nav = st.radio(
        "📌 Menu Chức Năng:",
        ["🧋 Order Nước & Bánh", "📊 Doanh Thu Real-Time", "⚙️ Quản Lý Ca & Hệ Thống"]
    )
    
    st.markdown("---")
    st.caption("👤 **Thu ngân ca trực:** Nguyễn Văn Bình")
    st.caption("⏰ **Ca làm việc:** Ca Sáng (07:00 - 15:00)")
    
    # Widget Doanh thu nhanh ngay trong Sidebar
    df_sales_quick = pd.DataFrame(st.session_state.sales_history)
    quick_revenue = int(df_sales_quick["Thành tiền"].sum()) if not df_sales_quick.empty else 0
    quick_orders = len(df_sales_quick)
    
    st.markdown("---")
    st.markdown("### 📈 Doanh thu ca hiện tại")
    st.metric(label="Tổng doanh thu", value=f"{quick_revenue:,} VNĐ")
    st.caption(f"Số đơn đã hoàn tất: **{quick_orders} đơn**")

# ---------------------------------------------------------
# 7. BANNER TIÊU ĐỀ HÌNH ẢNH MÙA THU
# ---------------------------------------------------------
st.markdown("""
    <div class="hero-banner-img">
        <h1>🍁 AUTUMN TEA & BAKERY LOUNGE 🍞</h1>
        <p>"Thưởng thức hương vị Trà Sữa Mùa Thu & Bánh Mì Nướng Nóng Giòn"</p>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 8. GIAO DIỆN CHÍNH THEO ĐIỀU HƯỚNG SIDEBAR
# ---------------------------------------------------------

# ==================== GIAO DIỆN 1: POS CALL ORDER ====================
if selected_nav == "🧋 Order Nước & Bánh":
    
    col_left, col_right = st.columns([1.2, 0.8], gap="large")

    with col_left:
        # Thông tin khách hàng
        c1, c2, c3 = st.columns([1.2, 1.2, 1])
        with c1:
            customer_name = st.text_input("Tên khách hàng:", placeholder="Nhập tên khách...")
        with c2:
            selected_tier = st.selectbox("Hạng thành viên:", list(CUSTOMER_TIERS.keys()))
        with c3:
            service_type = st.selectbox("Hình thức:", ["☕ Tại quán", "🛍️ Mang đi", "🛵 Giao hàng"])

        # TAB Chọn giữa Thức Uống và Bánh Ăn Kèm
        st.markdown("---")
        item_type = st.radio("🎯 Chọn Loại Sản Phẩm:", ["🧋 Thức Uống Mùa Thu", "🍞 Bánh Mì & Bánh Ngọt Ăn Kèm"], horizontal=True)

        if item_type == "🧋 Thức Uống Mùa Thu":
            category = st.selectbox("Nhóm thức uống:", list(DRINK_MENU.keys()))
            current_category_menu = DRINK_MENU[category]

            c_item, c_qty = st.columns([2.5, 1])
            with c_item:
                selected_drink = st.selectbox("Tên món nước:", list(current_category_menu.keys()))
            with c_qty:
                drink_qty = st.number_input("Số lượng:", min_value=1, value=1, step=1, key="drink_qty")

            drink_info = current_category_menu[selected_drink]
            
            # Khối hiển thị ảnh & tùy chọn nước
            c_img, c_opts = st.columns([1, 1.8])
            with c_img:
                st.image(drink_info["img"], caption=selected_drink, use_container_width=True)
            with c_opts:
                sz_col, mlk_col = st.columns(2)
                with sz_col:
                    selected_size = st.selectbox("Size:", list(SIZE_OPTIONS.keys()))
                with mlk_col:
                    selected_milk = st.selectbox("Tùy chọn Sữa:", MILK_OPTIONS)

                sug_col, ice_col = st.columns(2)
                with sug_col:
                    selected_sugar = st.selectbox("Mức đường:", ["100%", "70%", "50%", "30%", "0%"])
                with ice_col:
                    selected_ice = st.selectbox("Mức đá:", ["100%", "70%", "50%", "30%", "🔥 Uống Nóng"])

            selected_toppings = st.multiselect("Topping thêm:", options=list(TOPPING_OPTIONS.keys()))
            
            # Tính đơn giá ly
            unit_price = drink_info["price"] + SIZE_OPTIONS[selected_size] + (10000 if "Oat" in selected_milk or "hạnh nhân" in selected_milk else 0) + sum(TOPPING_OPTIONS[t] for t in selected_toppings)
            total_item_price = unit_price * drink_qty

            st.info(f"💡 Đơn giá 1 ly: **{unit_price:,} VNĐ** | Tổng: **{total_item_price:,} VNĐ**")

            if st.button("➕ Thêm Thức Uống Vào Giỏ", type="primary", use_container_width=True):
                topping_str = ", ".join(selected_toppings) if selected_toppings else "Không"
                item_data = {
                    "Tên món": selected_drink,
                    "Loại": "Thức uống",
                    "Size": selected_size.split()[0],
                    "Ghi chú": f"Sữa: {selected_milk.split('(')[0].strip()} | Topping: {topping_str}",
                    "Đơn giá": unit_price,
                    "Số lượng": drink_qty,
                    "Thành tiền": total_item_price
                }
                st.session_state.cart.append(item_data)
                st.session_state.invoice_paid = False
                safe_toast(f"Đã thêm {drink_qty}x {selected_drink}!", icon="🧋")

        else: # BÁNH MÌ & BÁNH NGỌT
            c_bakery, c_qty_b = st.columns([2.5, 1])
            with c_bakery:
                selected_bakery = st.selectbox("Chọn loại bánh mì / bánh ngọt:", list(BAKERY_MENU.keys()))
            with c_qty_b:
                bakery_qty = st.number_input("Số lượng bánh:", min_value=1, value=1, step=1, key="bakery_qty")

            bakery_info = BAKERY_MENU[selected_bakery]
            
            c_b_img, c_b_opts = st.columns([1, 1.8])
            with c_b_img:
                st.image(bakery_info["img"], caption=selected_bakery, use_container_width=True)
            with c_b_opts:
                st.write(f"**Mô tả:** {bakery_info['desc']}")
                heat_option = st.checkbox("🔥 Hâm nóng bánh trước khi giao", value=True)
                extra_cheese = st.checkbox("🧀 Thêm Phô Mai Nướng (+10,000 VNĐ)", value=False)

            bakery_unit_price = bakery_info["price"] + (10000 if extra_cheese else 0)
            total_bakery_price = bakery_unit_price * bakery_qty

            st.info(f"💡 Đơn giá 1 phần bánh: **{bakery_unit_price:,} VNĐ** | Tổng: **{total_bakery_price:,} VNĐ**")

            if st.button("➕ Thêm Bánh Vào Giỏ", type="primary", use_container_width=True):
                note_heat = "Hâm nóng" if heat_option else "Không hâm"
                note_cheese = "Có phô mai" if extra_cheese else ""
                note_final = f"{note_heat} | {note_cheese}".strip(" |")
                item_data = {
                    "Tên món": selected_bakery,
                    "Loại": "Bánh",
                    "Size": "Standard",
                    "Ghi chú": note_final,
                    "Đơn giá": bakery_unit_price,
                    "Số lượng": bakery_qty,
                    "Thành tiền": total_bakery_price
                }
                st.session_state.cart.append(item_data)
                st.session_state.invoice_paid = False
                safe_toast(f"Đã thêm {bakery_qty}x {selected_bakery}!", icon="🍞")

    # ----- CỘT PHẢI: GIỎ HÀNG & THANH TOÁN -----
    with col_right:
        st.subheader("🛒 Giỏ Hàng Chi Tiết")

        if not st.session_state.cart:
            st.warning("Giỏ hàng đang trống.")
        else:
            df_cart = pd.DataFrame(st.session_state.cart)
            st.dataframe(
                df_cart[["Tên món", "Loại", "Ghi chú", "Số lượng", "Thành tiền"]],
                use_container_width=True,
                hide_index=True
            )

            if st.button("🗑️ Xóa toàn bộ giỏ hàng", use_container_width=True):
                st.session_state.cart = []
                st.session_state.invoice_paid = False
                safe_rerun()

            st.markdown("---")
            total_price = int(df_cart["Thành tiền"].sum())
            discount_percent = CUSTOMER_TIERS[selected_tier]
            discount_amount = int(total_price * (discount_percent / 100))
            final_price = total_price - discount_amount

            st.write(f"**Tạm tính:** {total_price:,} VNĐ")
            if discount_percent > 0:
                st.write(f"**Ưu đãi thành viên ({discount_percent}%):** -{discount_amount:,} VNĐ")
            
            st.markdown(f"### Cần thanh toán: <span style='color:#D96B27; font-weight:800; font-size:1.6rem;'>{final_price:,} VNĐ</span>", unsafe_allow_html=True)

            st.markdown("---")
            if st.button("💳 XÁC NHẬN THANH TOÁN", type="primary", use_container_width=True):
                st.session_state.invoice_paid = True
                
                # Ghi lịch sử bán hàng real-time
                item_summary = ", ".join([f"{item['Tên món']} ({item['Số lượng']})" for item in st.session_state.cart])
                new_sale = {
                    "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "Khách hàng": customer_name if customer_name else "Khách vãng lai",
                    "Loại món": service_type,
                    "Số lượng": sum(item['Số lượng'] for item in st.session_state.cart),
                    "Tạm tính": total_price,
                    "Giảm giá": discount_percent,
                    "Thành tiền": final_price,
                    "Chi tiết": item_summary
                }
                st.session_state.sales_history.append(new_sale)
                if hasattr(st, "balloons"):
                    st.balloons()

    # HIỂN THỊ HÓA ĐƠN & MÃ QR
    if st.session_state.get("invoice_paid") and st.session_state.cart:
        st.markdown("---")
        st.success("🎉 Đơn hàng đã hoàn tất thanh toán!")

        df_inv = pd.DataFrame(st.session_state.cart)
        tot_p = int(df_inv["Thành tiền"].sum())
        disc_p = CUSTOMER_TIERS[selected_tier]
        fin_p = tot_p - int(tot_p * (disc_p / 100))

        c_inv, c_qr = st.columns([1.2, 0.8])
        with c_inv:
            st.markdown("<div class='bill-box'>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align:center; color:#5C2C16;'>🍁 AUTUMN TEA & BAKERY LOUNGE</h2>", unsafe_allow_html=True)
            st.write(f"**Thời gian:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            st.write(f"**Khách hàng:** {customer_name if customer_name else 'Khách vãng lai'}")
            st.table(df_inv[["Tên món", "Ghi chú", "Số lượng", "Thành tiền"]])
            st.markdown(f"### 🎯 TỔNG THANH TOÁN: <span style='color:#D96B27'>{fin_p:,} VNĐ</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with c_qr:
            st.subheader("📲 VietQR Thanh Toán Autopay")
            qr_url = f"https://img.vietqr.io/image/MB-09999999999-compact2.png?amount={fin_p}&addInfo=AUTUMN%20TEA%20{customer_name}&accountName=AUTUMN%20LOUNGE"
            st.image(qr_url, caption="Quét bằng App Ngân hàng hoặc MoMo", use_container_width=True)

# ==================== GIAO DIỆN 2: DOANH THU REAL-TIME ====================
elif selected_nav == "📊 Doanh Thu Real-Time":
    st.subheader("📊 Báo Cáo Doanh Thu Real-Time (Cập Nhật Tự Động)")
    
    if not st.session_state.sales_history:
        st.info("Chưa có giao dịch phát sinh.")
    else:
        df_sales = pd.DataFrame(st.session_state.sales_history)
        
        total_rev = int(df_sales["Thành tiền"].sum())
        total_orders = len(df_sales)
        total_items = int(df_sales["Số lượng"].sum())
        avg_order = int(total_rev / total_orders) if total_orders > 0 else 0

        # KPI Metrics
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.metric("💰 Tổng Doanh Thu", f"{total_rev:,} VNĐ")
        with kpi2:
            st.metric("📦 Tổng Đơn Hàng", f"{total_orders} đơn")
        with kpi3:
            st.metric("🧋 Bánh & Ly Bán Ra", f"{total_items} phần")
        with kpi4:
            st.metric("📈 Trung Bình / Đơn", f"{avg_order:,} VNĐ")

        st.markdown("---")

        col_c1, col_c2 = st.columns([1.2, 0.8])
        with col_c1:
            st.subheader("📈 Biểu Đồ Doanh Thu Dạng Chuỗi Thời Gian")
            st.bar_chart(df_sales, x="Thời gian", y="Thành tiền", color="#D96B27")

        with col_c2:
            st.subheader("📜 Nhật Ký Đơn Hàng Bán Ra")
            st.dataframe(
                df_sales[["Thời gian", "Khách hàng", "Số lượng", "Thành tiền"]],
                use_container_width=True,
                hide_index=True
            )

        # Download File Excel CSV
        csv_data = df_sales.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Tải Báo Cáo Doanh Thu (.CSV)",
            data=csv_data,
            file_name=f"Autumn_Revenue_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            type="primary"
        )

# ==================== GIAO DIỆN 3: QUẢN LÝ CA ====================
else:
    st.subheader("⚙️ Quản Lý Ca Làm Việc & Cấu Hình")
    st.info("Trang quản lý ca trực thu ngân & cập nhật tỷ lệ chiết khấu ưu đãi.")
    
    c_staff1, c_staff2 = st.columns(2)
    with c_staff1:
        st.text_input
