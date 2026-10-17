import ast

code_to_test = '''import streamlit as st
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
# 3. CUSTOM CSS: TONE MÙA THU 🍁 & CARD STYLING
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

    .kds-card {
        background-color: #FFFFFF;
        border-left: 6px solid var(--autumn-orange);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }

    .table-card-free {
        background-color: #E6F4EA;
        border: 2px solid #34A853;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        font-weight: bold;
        color: #137333;
    }

    .table-card-occupied {
        background-color: #FCE8E6;
        border: 2px solid #EA4335;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        font-weight: bold;
        color: #C5221F;
    }

    .bill-box {
        background-color: #FFFFFF;
        border: 2px dashed var(--autumn-orange);
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.06);
    }

    .wheel-box {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        border: 2px solid var(--autumn-gold);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. INITIALIZE SESSION STATE
# ---------------------------------------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []
if "invoice_paid" not in st.session_state:
    st.session_state.invoice_paid = False
if "last_completed_order" not in st.session_state:
    st.session_state.last_completed_order = None

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
            "table": "Bàn 02",
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
            "table": "Mang đi",
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

# Menu config
DRINK_MENU = {
    "🍵 Trà Sữa Mùa Thu 🍁": {
        "Trà Sữa Quế Hoa Mùa Thu": {
            "price": 58000,
            "img": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=600&q=80",
            "ingredients": {"Trà Cốt Ô Long (g)": 30, "Sữa Tươi Kem Béo (ml)": 100}
        },
        "Latte Hạt Dẻ Nướng Hazelnut": {
            "price": 62000,
            "img": "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?auto=format&fit=crop&w=600&q=80",
            "ingredients": {"Trà Cốt Đen (g)": 25, "Sữa Tươi Kem Béo (ml)": 120}
        },
        "Trà Sữa Ô Long Lúa Mạch": {
            "price": 52000,
            "img": "https://images.unsplash.com/photo-1485808191679-5f86510681a2?auto=format&fit=crop&w=600&q=80",
            "ingredients": {"Trà Cốt Ô Long (g)": 30, "Sữa Tươi Kem Béo (ml)": 100}
        },
        "Trà Sữa Trân Châu Đường Đen Maple": {
            "price": 55000,
            "img": "https://images.unsplash.com/photo-1558857563-b371033873b8?auto=format&fit=crop&w=600&q=80",
            "ingredients": {"Trà Cốt Đen (g)": 30, "Sữa Tươi Kem Béo (ml)": 100, "Trân Châu Hoàng Gia (g)": 50}
        }
    },
    "🍎 Trà Trái Cây Refreshers 🍂": {
        "Trà Hồng Trà Táo Mật Maple": {
            "price": 55000,
            "img": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=600&q=80",
            "ingredients": {"Trà Cốt Đen (g)": 30}
        },
        "Trà Đào Cam Sả Mật Ô Long": {
            "price": 50000,
            "img": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=600&q=80",
            "ingredients": {"Trà Cốt Ô Long (g)": 30}
        },
        "Trà Dâu Tằm Bạc Hà Mùa Thu": {
            "price": 48000,
            "img": "https://images.unsplash.com/photo-1499638673689-79a0b5115d87?auto=format&fit=crop&w=600&q=80",
            "ingredients": {"Trà Cốt Đen (g)": 30}
        }
    },
    "☕ Coffee & Cream Special 🌾": {
        "Caramel Macchiato Hạt Dẻ": {
            "price": 65000,
            "img": "https://images.unsplash.com/photo-1541167760496-1628856ab772?auto=format&fit=crop&w=600&q=80",
            "ingredients": {"Sữa Tươi Kem Béo (ml)": 120}
        },
        "Cold Brew Trà Đen Macchiato": {
            "price": 60000,
            "img": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=600&q=80",
            "ingredients": {"Trà Cốt Đen (g)": 40}
        },
        "Matcha Frappuccino Kem Béo": {
            "price": 68000,
            "img": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=600&q=80",
            "ingredients": {"Sữa Tươi Kem Béo (ml)": 150}
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

print("Setup test successfully!")
'''

ast.parse(code_to_test)
print("Syntactically valid!")
