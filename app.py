import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG (Bắt buộc ở dòng đầu tiên)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Autumn Tea Lounge 🍁 - Quầy Bán Hàng & Doanh Thu",
    page_icon="🍁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. BỘ TƯƠNG THÍCH PHIÊN BẢN STREAMLIT
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
# 3. TRANG TRÍ CSS CHỦ ĐỀ TRÀ SỮA MÙA THU (AUTUMN THEME 🍁)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Bảng màu Mùa Thu: Cam Lá Phong, Nâu Ấm, Vàng Hổ Phách, Kem Ngọt */
    :root {
        --autumn-orange: #D96B27;
        --autumn-brown: #5C2C16;
        --autumn-gold: #D69E2E;
        --autumn-cream: #FAF5E8;
        --autumn-bg: #FDFBF7;
    }

    .stApp {
        background-color: var(--autumn-bg);
    }

    /* Hero Banner Mùa Thu */
    .autumn-banner {
        background: linear-gradient(135deg, #5C2C16 0%, #D96B27 100%);
        border-radius: 16px;
        padding: 28px 24px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 20px rgba(217, 107, 39, 0.2);
    }
    .autumn-banner h1 {
        color: #FFFFFF !important;
        font-family: 'Georgia', serif;
        font-weight: 800;
        font-size: 2.3rem;
        margin-bottom: 6px;
    }
    .autumn-banner p {
        color: #FCD34D;
        font-size: 1.1rem;
        margin: 0;
        font-style: italic;
    }

    /* Thẻ Card Signature Drinks */
    .sig-card {
        background-color: #FFFFFF;
        border-radius: 14px;
        padding: 12px;
        border: 2px solid #F3E8D5;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s;
    }
    .sig-card:hover {
        transform: translateY(-4px);
        border-color: var(--autumn-orange);
    }
    .sig-title {
        font-weight: 700;
        color: var(--autumn-brown);
        margin-top: 8px;
        font-size: 0.95rem;
    }
    .sig-price {
        color: var(--autumn-orange);
        font-weight: 800;
        font-size: 1.05rem;
    }
    .badge-autumn {
        background-color: var(--autumn-orange);
        color: white;
        padding: 3px 10px;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* Thẻ Hóa Đơn Mùa Thu */
    .bill-box {
        background-color: #FFFFFF;
        border: 2px dashed var(--autumn-orange);
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.06);
    }

    /* Custom Metric Cards cho Doanh Thu */
    .metric-card {
        background-color: #FFFFFF;
        border-left: 5px solid var(--autumn-orange);
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.04);
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. DANH MỤC MÓN NƯỚC MÙA THU & HÌNH ẢNH
# ---------------------------------------------------------
SIGNATURE_DRINKS = [
    {
        "name": "Trà Sữa Quế Hoa Mùa Thu",
        "price": "58,000 VNĐ",
        "tag": "🍁 Signature Mùa Thu",
        "img": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=500&q=80"
    },
    {
        "name": "Latte Hạt Dẻ Nướng Hazelnut",
        "price": "62,000 VNĐ",
        "tag": "🌰 Cozy Autumn",
        "img": "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?auto=format&fit=crop&w=500&q=80"
    },
    {
        "name": "Trà Hồng Trà Táo Mật Maple",
        "price": "55,000 VNĐ",
        "tag": "🍎 Fresh Autumn",
        "img": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=500&q=80"
    },
    {
        "name": "Trà Sữa Ô Long Lúa Mạch",
        "price": "52,000 VNĐ",
        "tag": "🌾 Warm & Creamy",
        "img": "https://images.unsplash.com/photo-1485808191679-5f86510681a2?auto=format&fit=crop&w=500&q=80"
    }
]

MENU_ITEMS = {
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
    "🍎 Trà Trái Cây & Refresher 🍂": {
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
        }
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
SUGAR_LEVELS = ["100% (Tiêu chuẩn)", "70% (Ít ngọt)", "50%", "30%", "0%"]
ICE_LEVELS = ["100% (Tiêu chuẩn)", "70%", "50%", "30%", "0% (Không đá)", "🔥 Uống Nóng"]
SERVICE_TYPES = ["☕ Uống tại quán", "🛍️ Mang đi", "🛵 Giao hàng"]

CUSTOMER_TIERS = {
    "Khách vãng lai": 0,
    "Thành viên Maple 🍁 (Giảm 5%)": 5,
    "Thành viên Gold Leaf 🍂 (Giảm 10%)": 10,
    "VIP Autumn Reserve 👑 (Giảm 15%)": 15
}

# ---------------------------------------------------------
# 5. KHỞI TẠO SESSION STATE
# ---------------------------------------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []
if "invoice_paid" not in st.session_state:
    st.session_state.invoice_paid = False
if "sales_history" not in st.session_state:
    # Lịch sử doanh thu mẫu để hiển thị ngay
    st.session_state.sales_history = [
        {
            "Thời gian": "17/10/2026 14:15:20",
            "Khách hàng": "Anh Minh",
            "Hình thức": "☕ Uống tại quán",
            "Số món": 2,
            "Tạm tính": 116000,
            "Giảm giá": 5,
            "Thành tiền": 110200,
            "Các món": "Trà Sữa Quế Hoa Mùa Thu (1), Latte Hạt Dẻ Nướng Hazelnut (1)"
        },
        {
            "Thời gian": "17/10/2026 15:30:10",
            "Khách hàng": "Chị Hoàng Yến",
            "Hình thức": "🛍️ Mang đi",
            "Số món": 1,
            "Tạm tính": 55000,
            "Giảm giá": 10,
            "Thành tiền": 49500,
            "Các món": "Trà Hồng Trà Táo Mật Maple (1)"
        }
    ]

# ---------------------------------------------------------
# 6. HEADER CHỦ ĐỀ MÙA THU 🍁
# ---------------------------------------------------------
st.markdown("""
    <div class="autumn-banner">
        <h1>🍁 AUTUMN TEA LOUNGE & POS 🍂</h1>
        <p>"Thưởng thức hương vị Trà Sữa Mùa Thu ấm áp & ngọt ngào"</p>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 7. PHÂN CHIA TABS CÔNG NĂNG
# ---------------------------------------------------------
tab_order, tab_analytics = st.tabs(["🧋 Quầy Gọi Món (Order POS)", "📊 Báo Cáo Doanh Thu Real-Time"])

# =========================================================
# TAB 1: QUẦY BÁN HÀNG & ORDER
# =========================================================
with tab_order:
    # Gallery Signature Mùa Thu
    st.subheader("🌟 Signature Collection - Mùa Thu 🍁")
    cols = st.columns(4)
    for idx, drink in enumerate(SIGNATURE_DRINKS):
        with cols[idx]:
            st.markdown(f"""
                <div class="sig-card">
                    <img src="{drink['img']}" style="width:100%; height:120px; object-fit:cover; border-radius:8px;">
                    <div class="sig-title">{drink['name']}</div>
                    <div class="sig-price">{drink['price']}</div>
                    <span class="badge-autumn">{drink['tag']}</span>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1.15, 0.85], gap="medium")

    # ----- CỘT TRÁI: CHỌN MÓN & TÙY CHỈNH -----
    with col_left:
        st.subheader("📝 Thông tin Đơn hàng & Tùy chọn")
        
        c1, c2, c3 = st.columns([1.2, 1.2, 1])
        with c1:
            customer_name = st.text_input("Tên khách hàng:", placeholder="Nhập tên...")
        with c2:
            selected_tier = st.selectbox("Hạng thành viên:", list(CUSTOMER_TIERS.keys()))
        with c3:
            service_type = st.selectbox("Phục vụ:", SERVICE_TYPES)

        st.markdown("---")
        
        # Chọn Nhóm & Món
        category = st.selectbox("🎯 Nhóm thức uống Mùa Thu:", list(MENU_ITEMS.keys()))
        current_category_menu = MENU_ITEMS[category]

        c_item, c_qty = st.columns([2.5, 1])
        with c_item:
            selected_tea = st.selectbox("Chọn món nước:", list(current_category_menu.keys()))
        with c_qty:
            quantity = st.number_input("Số lượng:", min_value=1, value=1, step=1)

        # HÌNH ẢNH MÓN NƯỚC HIỂN THỊ TRỰC QUAN
        drink_info = current_category_menu[selected_tea]
        col_img, col_opts = st.columns([1, 2])
        
        with col_img:
            st.image(drink_info["img"], caption=f"📷 {selected_tea}", use_container_width=True)

        with col_opts:
            c_sz, c_mlk = st.columns(2)
            with c_sz:
                selected_size = st.selectbox("Size:", list(SIZE_OPTIONS.keys()))
            with c_mlk:
                selected_milk = st.selectbox("Sữa:", MILK_OPTIONS)

            c_sug, c_ice = st.columns(2)
            with c_sug:
                selected_sugar = st.selectbox("Đường:", SUGAR_LEVELS)
            with c_ice:
                selected_ice = st.selectbox("Đá / Nóng:", ICE_LEVELS)

        selected_toppings = st.multiselect("Topping đặc biệt:", options=list(TOPPING_OPTIONS.keys()))
        custom_note = st.text_input("Ghi chú cho Barista:", placeholder="Ví dụ: Ít ngọt, đậy nắp cẩn thận...")

        # Tính đơn giá ly
        base_price = drink_info["price"]
        size_price = SIZE_OPTIONS[selected_size]
        milk_extra = 10000 if "Oat" in selected_milk or "hạnh nhân" in selected_milk else 0
        topping_price = sum(TOPPING_OPTIONS[t] for t in selected_toppings)
        
        unit_price = base_price + size_price + milk_extra + topping_price
        item_total = unit_price * quantity

        st.info(f"💡 Đơn giá 1 ly: **{unit_price:,} VNĐ** | Tổng món: **{item_total:,} VNĐ**")

        if st.button("➕ Thêm vào giỏ hàng 🍁", type="primary", use_container_width=True):
            topping_str = ", ".join(selected_toppings) if selected_toppings else "Không"
            item_data = {
                "Tên món": selected_tea,
                "Size": selected_size.split()[0],
                "Loại sữa": selected_milk.split("(")[0].strip(),
                "Đường": selected_sugar.split()[0],
                "Đá": selected_ice.split()[0],
                "Topping": topping_str,
                "Ghi chú": custom_note,
                "Đơn giá": unit_price,
                "Số lượng": quantity,
                "Thành tiền": item_total
            }
            st.session_state.cart.append(item_data)
            st.session_state.invoice_paid = False
            safe_toast(f"Đã thêm {quantity}x {selected_tea} vào giỏ hàng!", icon="🍂")

    # ----- CỘT PHẢI: GIỎ HÀNG & THANH TOÁN -----
    with col_right:
        st.subheader("🛒 Giỏ hàng Mùa Thu")

        if not st.session_state.cart:
            st.warning("Giỏ hàng đang trống. Vui lòng chọn món bên trái.")
        else:
            df_cart = pd.DataFrame(st.session_state.cart)
            
            st.dataframe(
                df_cart[["Tên món", "Size", "Topping", "Số lượng", "Thành tiền"]],
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
            stars_earned = final_price // 50000

            st.write(f"**Tạm tính:** {total_price:,} VNĐ")
            if discount_percent > 0:
                st.write(f"**Ưu đãi hạng ({discount_percent}%):** -{discount_amount:,} VNĐ")
            
            st.markdown(f"### Tổng thanh toán: <span style='color:#D96B27; font-weight:800; font-size:1.6rem;'>{final_price:,} VNĐ</span>", unsafe_allow_html=True)
            st.caption(f"🍁 Điểm tích lũy: **+{stars_earned} Lá Phong Mùa Thu**")

            st.markdown("---")
            if st.button("💳 XÁC NHẬN THANH TOÁN", type="primary", use_container_width=True):
                st.session_state.invoice_paid = True
                
                # TỰ ĐỘNG GHI LẠI VÀO BÁO CÁO DOANH THU REAL-TIME
                items_summary = ", ".join([f"{item['Tên món']} ({item['Số lượng']})" for item in st.session_state.cart])
                
                new_sale = {
                    "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "Khách hàng": customer_name if customer_name else "Khách vãng lai",
                    "Hình thức": service_type,
                    "Số món": sum(item['Số lượng'] for item in st.session_state.cart),
                    "Tạm tính": total_price,
                    "Giảm giá": discount_percent,
                    "Thành tiền": final_price,
                    "Các món": items_summary
                }
                st.session_state.sales_history.append(new_sale)
                
                if hasattr(st, "balloons"):
                    st.balloons()

    # ----- HIỂN THỊ HÓA ĐƠN & VIETQR KHI THANH TOÁN SUCCESS -----
    if st.session_state.get("invoice_paid") and st.session_state.cart:
        st.markdown("---")
        st.success("🎉 Thanh toán thành công! Đơn hàng đã được lưu vào hệ thống Doanh Thu Real-Time.")

        df_inv = pd.DataFrame(st.session_state.cart)
        tot_pr = int(df_inv["Thành tiền"].sum())
        disc_pct = CUSTOMER_TIERS[selected_tier]
        fin_pr = tot_pr - int(tot_pr * (disc_pct / 100))

        col_inv, col_qr = st.columns([1.2, 0.8])
        
        with col_inv:
            st.markdown("<div class='bill-box'>", unsafe_allow_html=True)
            st.markdown("""
                <div style="text-align:center;">
                    <h2 style="color:#5C2C16; margin-bottom:0;">🍁 AUTUMN TEA LOUNGE</h2>
                    <p style="color:#D96B27; font-size:0.85rem; margin-top:0;">HÓA ĐƠN BÁN HÀNG MÙA THU</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.write(f"**Thời gian:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            st.write(f"**Khách hàng:** {customer_name if customer_name else 'Khách vãng lai'} ({selected_tier.split('(')[0]})")
            st.write(f"**Hình thức:** {service_type}")
            
            st.table(df_inv[["Tên món", "Size", "Loại sữa", "Topping", "Số lượng", "Thành tiền"]])
            
            st.markdown(f"**Tổng tiền:** {tot_pr:,} VNĐ")
            st.markdown(f"**Giảm giá:** {disc_pct}%")
            st.markdown(f"### 🎯 TỔNG THANH TOÁN: <span style='color:#D96B27'>{fin_pr:,} VNĐ</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_qr:
            st.subheader("📲 Quét VietQR Thanh Toán")
            bank_id = "MB"
            account_no = "09999999999"
            account_name = "AUTUMN TEA LOUNGE"
            qr_url = f"https://img.vietqr.io/image/{bank_id}-{account_no}-compact2.png?amount={fin_pr}&addInfo=Thanh%20toan%20AutumnTea%20{customer_name}&accountName={account_name}"
            st.image(qr_url, caption="Mã VietQR tự động khớp đúng số tiền thanh toán", use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Tạo đơn bán tiếp theo", type="secondary", use_container_width=True):
            st.session_state.cart = []
            st.session_state.invoice_paid = False
            safe_rerun()

# =========================================================
# TAB 2: BÁO CÁO DOANH THU REAL-TIME 📊
# =========================================================
with tab_analytics:
    st.subheader("📊 Báo Cáo Doanh Thu Theo Thời Gian Thực (Real-Time Analytics)")
    
    if not st.session_state.sales_history:
        st.info("Chưa có giao dịch nào được ghi nhận trong phiên hôm nay.")
    else:
        df_sales = pd.DataFrame(st.session_state.sales_history)
        
        total_rev = int(df_sales["Thành tiền"].sum())
        total_orders = len(df_sales)
        total_items_sold = int(df_sales["Số món"].sum())
        avg_order_val = int(total_rev / total_orders) if total_orders > 0 else 0

        # Hiển thị Metrics tổng quan
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric(label="💰 Tổng Doanh Thu", value=f"{total_rev:,} VNĐ")
        with m2:
            st.metric(label="📦 Tổng Số Đơn hàng", value=f"{total_orders} đơn")
        with m3:
            st.metric(label="🧋 Tổng Ly Bán Ra", value=f"{total_items_sold} ly")
        with m4:
            st.metric(label="📈 Giá Trị Đơn TB", value=f"{avg_order_val:,} VNĐ")

        st.markdown("---")

        # Biểu đồ Doanh Thu & Bảng Lịch Sử
        col_chart, col_history = st.columns([1, 1])

        with col_chart:
            st.subheader("📈 Biểu đồ Doanh Thu Theo Giao Dịch")
            # Tạo biểu đồ doanh thu theo đơn vị giao dịch
            st.bar_chart(df_sales, x="Thời gian", y="Thành tiền", color="#D96B27")

        with col_history:
            st.subheader("📜 Nhật Ký Giao Dịch Chi Tiết")
            st.dataframe(
                df_sales[["Thời gian", "Khách hàng", "Số món", "Thành tiền", "Hình thức"]],
                use_container_width=True,
                hide_index=True
            )

        st.markdown("---")
        
        # Nút Xuất file Excel / CSV báo cáo
        csv_data = df_sales.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Tải Báo Cáo Doanh Thu (.CSV)",
            data=csv_data,
            file_name=f"AutumnTea_Revenue_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            type="primary"
        )
