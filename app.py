import streamlit as st
import pandas as pd
from datetime import datetime
import json
import random

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Autumn Tea & Bakery Lounge 🍁 (All-in-One POS)",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. HÀM TƯƠNG THÍCH STREAMLIT
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
# 3. CUSTOM CSS: TONE MÙA THU CỦA QUÁN 🍁
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

    /* BANNER TIÊU ĐỀ CÓ ẢNH NỀN TONE MÙA THU */
    .hero-banner-img {
        position: relative;
        background-image: linear-gradient(rgba(44, 19, 9, 0.75), rgba(92, 44, 22, 0.85)), 
                          url('https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        border-radius: 16px;
        padding: 30px 20px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    }
    
    .hero-banner-img h1 {
        color: #FFFFFF !important;
        font-family: 'Georgia', serif;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 6px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .hero-banner-img p {
        color: #FBBF24;
        font-size: 1.1rem;
        margin: 0;
        font-style: italic;
        font-weight: 500;
    }

    /* KDS Card */
    .kds-card-pending {
        background-color: #FFFBEB;
        border-left: 6px solid #F59E0B;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .kds-card-doing {
        background-color: #EFF6FF;
        border-left: 6px solid #3B82F6;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .kds-card-done {
        background-color: #ECFDF5;
        border-left: 6px solid #10B981;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }

    /* Sơ đồ bàn */
    .table-free {
        background-color: #ECFDF5;
        border: 2px solid #10B981;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        font-weight: bold;
        color: #065F46;
        margin-bottom: 10px;
    }

    .table-occupied {
        background-color: #FEF2F2;
        border: 2px solid #EF4444;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        font-weight: bold;
        color: #991B1B;
        margin-bottom: 10px;
    }

    /* Thẻ Hóa Đơn Thermal POS */
    .bill-thermal {
        background-color: #FFFFFF;
        border: 2px dashed #D96B27;
        border-radius: 12px;
        padding: 20px;
        font-family: 'Courier New', Courier, monospace;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    /* AI Box */
    .ai-box {
        background: linear-gradient(135deg, #FEF3C7 0%, #FFFBEB 100%);
        border: 1px solid #F59E0B;
        border-radius: 10px;
        padding: 12px;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    /* Lucky Wheel Box */
    .wheel-container {
        background: linear-gradient(135deg, #5C2C16 0%, #D96B27 100%);
        color: white;
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. KHỞI TẠO SESSION STATE DỮ LIỆU TOÀN DIỆN
# ---------------------------------------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []
if "invoice_paid" not in st.session_state:
    st.session_state.invoice_paid = False
if "order_counter" not in st.session_state:
    st.session_state.order_counter = 103

if "sales_history" not in st.session_state:
    st.session_state.sales_history = [
        {
            "Mã đơn": "ORD-101",
            "Thời gian": "17/10/2026 14:15:20",
            "Khách hàng": "Anh Minh",
            "Vị trí": "Bàn 02",
            "Số lượng": 3,
            "Thành tiền": 146300,
            "Chi tiết": "Trà Sữa Quế Hoa (1), Bánh Mì Bơ Tỏi (1), Latte Hạt Dẻ (1)"
        },
        {
            "Mã đơn": "ORD-102",
            "Thời gian": "17/10/2026 15:30:10",
            "Khách hàng": "Chị Hoàng Yến",
            "Vị trí": "Mang đi",
            "Số lượng": 1,
            "Thành tiền": 49500,
            "Chi tiết": "Trà Hồng Trà Táo Mật Maple (1)"
        }
    ]

if "kds_orders" not in st.session_state:
    st.session_state.kds_orders = [
        {
            "id": "ORD-101",
            "time": "14:15",
            "customer": "Anh Minh",
            "location": "Bàn 02",
            "items": [
                {"name": "Trà Sữa Quế Hoa Mùa Thu", "qty": 1, "note": "70% đường, Ít đá"},
                {"name": "Bánh Mì Bơ Tỏi Phô Mai Nướng", "qty": 1, "note": "Hâm nóng"},
                {"name": "Latte Hạt Dẻ Nướng Hazelnut", "qty": 1, "note": "Nóng"}
            ],
            "status": "Hoàn thành"
        },
        {
            "id": "ORD-102",
            "time": "15:30",
            "customer": "Chị Hoàng Yến",
            "location": "Mang đi",
            "items": [
                {"name": "Trà Hồng Trà Táo Mật Maple", "qty": 1, "note": "Sữa Oat milk"}
            ],
            "status": "Đang chế biến"
        }
    ]

if "tables" not in st.session_state:
    st.session_state.tables = {f"Bàn {i:02d}": {"status": "Trống", "order_id": None, "guests": 0} for i in range(1, 13)}
    st.session_state.tables["Bàn 02"] = {"status": "Đang ngồi", "order_id": "ORD-101", "guests": 2}
    st.session_state.tables["Bàn 05"] = {"status": "Đang ngồi", "order_id": None, "guests": 4}

if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "Trà Cốt Ô Long (g)": 4500,
        "Trà Cốt Đen (g)": 3800,
        "Sữa Tươi Kem Béo (ml)": 15000,
        "Sữa Yến Mạch Oat Milk (ml)": 4200,
        "Trân Châu Hoàng Gia (g)": 2500,
        "Bánh Mì Sandwich BBQ (Cái)": 18,
        "Bánh Mì Bơ Tỏi (Cái)": 12,
        "Bánh Croissant Bơ (Cái)": 20,
        "Bánh Tiramisu Hạt Dẻ (Cái)": 8,
        "Bánh Cheesecake Chanh Dây (Cái)": 10
    }

if "wheel_prize" not in st.session_state:
    st.session_state.wheel_prize = None

# ---------------------------------------------------------
# 5. DỮ LIỆU THỰC ĐƠN
# ---------------------------------------------------------
DRINK_MENU = {
    "🍵 Trà Sữa Mùa Thu 🍁": {
        "Trà Sữa Quế Hoa Mùa Thu": {
            "price": 58000,
            "img": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=600&q=80",
            "ingredients": {"Trà Cốt Ô Long (g)": 30, "Sữa Tươi Kem Béo (ml)": 100},
            "upsell_recommend": "🥐 Bánh Croissant Bơ Thụy Sĩ"
        },
        "Latte Hạt Dẻ Nướng Hazelnut": {
            "price": 62000,
            "img": "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?auto=format&fit=crop&w=600&q=80",
            "ingredients": {"Trà Cốt Đen (g)": 25, "Sữa Tươi Kem Béo (ml)": 120},
            "upsell_recommend": "🍰 Bánh Tiramisu Hạt Dẻ Autumn"
        },
        "Trà Sữa Ô Long Lúa Mạch": {
            "price": 52000,
            "img": "https://images.unsplash.com/photo-1485808191679-5f86510681a2?auto=format&fit=crop&w=600&q=80",
            "ingredients": {"Trà Cốt Ô Long (g)": 30, "Sữa Tươi Kem Béo (ml)": 100},
            "upsell_recommend": "🧄 Bánh Mì Bơ Tỏi Phô Mai Nướng"
        },
        "Trà Sữa Trân Châu Đường Đen Maple": {
            "price": 55000,
            "img": "https://images.unsplash.com/photo-1558857563-b371033873b8?auto=format&fit=crop&w=600&q=80",
            "ingredients": {"Trà Cốt Đen (g)": 30, "Sữa Tươi Kem Béo (ml)": 100, "Trân Châu Hoàng Gia (g)": 50},
            "upsell_recommend": "🥐 Bánh Croissant Bơ Thụy Sĩ"
        }
    },
    "🍎 Trà Trái Cây Refreshers 🍂": {
        "Trà Hồng Trà Táo Mật Maple": {
            "price": 55000,
            "img": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=600&q=80",
            "ingredients": {"Trà Cốt Đen (g)": 30},
            "upsell_recommend": "🧀 Bánh Cheesecake Chanh Dây"
        },
        "Trà Đào Cam Sả Mật Ô Long": {
            "price": 50000,
            "img": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=600&q=80",
            "ingredients": {"Trà Cốt Ô Long (g)": 30},
            "upsell_recommend": "🥪 Bánh Mì Sandwich Thịt Nướng BBQ"
        },
        "Trà Dâu Tằm Bạc Hà Mùa Thu": {
            "price": 48000,
            "img": "https://images.unsplash.com/photo-1499638673689-79a0b5115d87?auto=format&fit=crop&w=600&q=80",
            "ingredients": {"Trà Cốt Đen (g)": 30},
            "upsell_recommend": "🧀 Bánh Cheesecake Chanh Dây"
        }
    },
    "☕ Coffee & Cream Special 🌾": {
        "Caramel Macchiato Hạt Dẻ": {
            "price": 65000,
            "img": "https://images.unsplash.com/photo-1541167760496-1628856ab772?auto=format&fit=crop&w=600&q=80",
            "ingredients": {"Sữa Tươi Kem Béo (ml)": 120},
            "upsell_recommend": "🥐 Bánh Croissant Bơ Thụy Sĩ"
        },
        "Cold Brew Trà Đen Macchiato": {
            "price": 60000,
            "img": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=600&q=80",
            "ingredients": {"Trà Cốt Đen (g)": 40},
            "upsell_recommend": "🍰 Bánh Tiramisu Hạt Dẻ Autumn"
        },
        "Matcha Frappuccino Kem Béo": {
            "price": 68000,
            "img": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=600&q=80",
            "ingredients": {"Sữa Tươi Kem Béo (ml)": 150},
            "upsell_recommend": "🧄 Bánh Mì Bơ Tỏi Phô Mai Nướng"
        }
    }
}

BAKERY_MENU = {
    "🥪 Bánh Mì Sandwich Thịt Nướng BBQ": {
        "price": 45000,
        "img": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=600&q=80",
        "desc": "Bánh mì Sandwich giòn kẹp thịt nướng sốt BBQ đậm đà",
        "stock_key": "Bánh Mì Sandwich BBQ (Cái)"
    },
    "🧄 Bánh Mì Bơ Tỏi Phô Mai Nướng": {
        "price": 38000,
        "img": "https://images.unsplash.com/photo-1573140247632-f8fd74997d5c?auto=format&fit=crop&w=600&q=80",
        "desc": "Bánh mì sốt bơ tỏi thơm lừng ngập tràn phô mai kéo sợi",
        "stock_key": "Bánh Mì Bơ Tỏi (Cái)"
    },
    "🥐 Bánh Croissant Bơ Thụy Sĩ": {
        "price": 35000,
        "img": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=600&q=80",
        "desc": "Bánh sừng bò nướng giòn xốp thơm bơ ngậy",
        "stock_key": "Bánh Croissant Bơ (Cái)"
    },
    "🍰 Bánh Tiramisu Hạt Dẻ Autumn": {
        "price": 48000,
        "img": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?auto=format&fit=crop&w=600&q=80",
        "desc": "Bánh Tiramisu mềm mịn thơm vị cà phê & hạt dẻ nướng",
        "stock_key": "Bánh Tiramisu Hạt Dẻ (Cái)"
    },
    "🧀 Bánh Cheesecake Chanh Dây": {
        "price": 45000,
        "img": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=600&q=80",
        "desc": "Cheesecake chua ngọt thanh mát hòa quyện vị chanh dây",
        "stock_key": "Bánh Cheesecake Chanh Dây (Cái)"
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

PRIZES = [
    "🎟️ Voucher giảm 20% cho đơn tiếp theo",
    "🥐 Tặng 1 Bánh Croissant Bơ Thụy Sĩ",
    "🧋 Tặng 1 Topping Trân Châu Hoàng Gia",
    "🌟 Tặng +500 Điểm Thưởng Thành Viên",
    "🎁 Tặng 1 Ly Trà Sữa Quế Hoa Mùa Thu",
    "🍀 Chúc bạn may mắn lần sau!"
]

# ---------------------------------------------------------
# 6. SIDEBAR ĐIỀU HƯỚNG TỔNG HỢP
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=500&q=80", use_container_width=True)
    st.markdown("<h2 style='text-align:center; color:#5C2C16;'>🍁 AUTUMN LOUNGE</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    selected_nav = st.radio(
        "📌 Chức Năng Hệ Thống:",
        [
            "🧋 Order Bán Hàng & POS",
            "👨‍🍳 Màn Hình Bếp / Barista (KDS)",
            "🗺️ Sơ Đồ Quản Lý Bàn",
            "📦 Quản Lý Tồn Kho",
            "🎁 Vòng Quay May Mắn",
            "📊 Doanh Thu Real-Time",
            "⚙️ Quản Lý Ca"
        ]
    )
    
    st.markdown("---")
    st.caption("👤 **Thu ngân:** Nguyễn Văn Bình")
    st.caption("⏰ **Ca:** Ca Sáng (07:00 - 15:00)")
    
    df_sales_quick = pd.DataFrame(st.session_state.sales_history)
    quick_rev = int(df_sales_quick["Thành tiền"].sum()) if not df_sales_quick.empty else 0
    st.markdown("### 📈 Doanh Thu Ca")
    st.metric("Tổng doanh thu", f"{quick_rev:,} VNĐ")

# ---------------------------------------------------------
# 7. BANNER HERO TIÊU ĐỀ
# ---------------------------------------------------------
st.markdown("""
    <div class="hero-banner-img">
        <h1>🍁 AUTUMN TEA & BAKERY LOUNGE 🍞</h1>
        <p>"Thưởng Thức Hương Vị Trà Sữa Mùa Thu & Bánh Mì Nướng Nóng Giòn"</p>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 8. XỬ LÝ THEO TỪNG CHỨC NĂNG CỦA SIDEBAR
# ---------------------------------------------------------

# =========================================================
# CHỨC NĂNG 1: ORDER BÁN HÀNG & POS
# =========================================================
if selected_nav == "🧋 Order Bán Hàng & POS":
    col_left, col_right = st.columns([1.2, 0.8], gap="large")

    with col_left:
        st.subheader("📝 Thông Tin Order & Vị Trí")
        
        c1, c2, c3 = st.columns([1.2, 1.2, 1])
        with c1:
            customer_name = st.text_input("Tên khách hàng:", placeholder="Nhập tên khách...")
        with c2:
            selected_tier = st.selectbox("Hạng thành viên:", list(CUSTOMER_TIERS.keys()))
        with c3:
            table_options = ["Mang đi", "Giao hàng"] + list(st.session_state.tables.keys())
            selected_location = st.selectbox("Vị trí / Bàn:", table_options)

        st.markdown("---")
        item_type = st.radio("🎯 Chọn Sản Phẩm:", ["🧋 Thức Uống Mùa Thu", "🍞 Bánh Mì & Bánh Ngọt"], horizontal=True)

        if item_type == "🧋 Thức Uống Mùa Thu":
            category = st.selectbox("Nhóm thức uống:", list(DRINK_MENU.keys()))
            current_category_menu = DRINK_MENU[category]

            c_item, c_qty = st.columns([2.5, 1])
            with c_item:
                selected_drink = st.selectbox("Món nước:", list(current_category_menu.keys()))
            with c_qty:
                drink_qty = st.number_input("Số lượng:", min_value=1, value=1, step=1, key="drink_qty")

            drink_info = current_category_menu[selected_drink]
            
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
                    selected_sugar = st.selectbox("Đường:", ["100%", "70%", "50%", "30%", "0%"])
                with ice_col:
                    selected_ice = st.selectbox("Đá:", ["100%", "70%", "50%", "30%", "🔥 Uống Nóng"])

            selected_toppings = st.multiselect("Topping:", options=list(TOPPING_OPTIONS.keys()))
            
            # FEATURE 2: AI SMART UPSELL & RECOMMENDATION BOX
            rec_bakery = drink_info.get("upsell_recommend", "🥐 Bánh Croissant Bơ Thụy Sĩ")
            st.markdown(f"""
                <div class="ai-box">
                    <strong>🤖 AI Gợi Ý Combo Mùa Thu:</strong> Thức uống <em>{selected_drink}</em> cực kỳ hợp vị khi dùng kèm <strong>{rec_bakery}</strong>!
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"➕ Thêm Combo Gợi Ý ({rec_bakery})", type="secondary"):
                bakery_match = None
                for b_name in BAKERY_MENU.keys():
                    if rec_bakery in b_name or b_name in rec_bakery:
                        bakery_match = b_name
                        break
                if not bakery_match:
                    bakery_match = list(BAKERY_MENU.keys())[0]
                
                b_info = BAKERY_MENU[bakery_match]
                st.session_state.cart.append({
                    "Tên món": bakery_match,
                    "Loại": "Bánh (AI Combo)",
                    "Size": "Standard",
                    "Ghi chú": "Hâm nóng | AI Combo Discount -10,000đ",
                    "Đơn giá": b_info["price"] - 10000,
                    "Số lượng": 1,
                    "Thành tiền": b_info["price"] - 10000,
                    "ingredients": {b_info["stock_key"]: 1}
                })
                safe_toast(f"Đã thêm bánh Combo {bakery_match} với giá ưu đãi!", icon="🤖")

            unit_price = drink_info["price"] + SIZE_OPTIONS[selected_size] + (10000 if "Oat" in selected_milk or "hạnh nhân" in selected_milk else 0) + sum(TOPPING_OPTIONS[t] for t in selected_toppings)
            total_item_price = unit_price * drink_qty

            st.info(f"💡 Đơn giá 1 ly: **{unit_price:,} VNĐ** | Tổng: **{total_item_price:,} VNĐ**")

            if st.button("➕ Thêm Thức Uống Vào Giỏ", type="primary", use_container_width=True):
                topping_str = ", ".join(selected_toppings) if selected_toppings else "Không"
                item_data = {
                    "Tên món": selected_drink,
                    "Loại": "Thức uống",
                    "Size": selected_size.split()[0],
                    "Ghi chú": f"Sữa: {selected_milk.split('(')[0].strip()} | Đường: {selected_sugar} | Đá: {selected_ice} | Topping: {topping_str}",
                    "Đơn giá": unit_price,
                    "Số lượng": drink_qty,
                    "Thành tiền": total_item_price,
                    "ingredients": drink_info.get("ingredients", {})
                }
                st.session_state.cart.append(item_data)
                st.session_state.invoice_paid = False
                safe_toast(f"Đã thêm {drink_qty}x {selected_drink}!", icon="🧋")

        else: # BAKERY
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
                    "Thành tiền": total_bakery_price,
                    "ingredients": {bakery_info["stock_key"]: bakery_qty}
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

            if final_price >= 100000:
                st.success("🎉 Đơn hàng >= 100k! Khách hàng nhận được 1 Lượt Quay Vòng Quay May Mắn!")

            st.markdown("---")
            if st.button("💳 XÁC NHẬN THANH TOÁN & GỬI BẾP", type="primary", use_container_width=True):
                order_id = f"ORD-{st.session_state.order_counter}"
                st.session_state.order_counter += 1
                
                st.session_state.invoice_paid = True
                
                # 1. Deduct Inventory automatically
                for item in st.session_state.cart:
                    ing_map = item.get("ingredients", {})
                    for ing_name, amount in ing_map.items():
                        if ing_name in st.session_state.inventory:
                            st.session_state.inventory[ing_name] = max(0, st.session_state.inventory[ing_name] - (amount * item["Số lượng"]))

                # 2. Update Table Status
                if selected_location in st.session_state.tables:
                    st.session_state.tables[selected_location]["status"] = "Đang ngồi"
                    st.session_state.tables[selected_location]["order_id"] = order_id

                # 3. Push to KDS
                kds_item_list = [{"name": i["Tên món"], "qty": i["Số lượng"], "note
