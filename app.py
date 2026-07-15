import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- 1. SETTING & STYLE ---
st.set_page_config(page_title="Hotel Flow Grid Pro", layout="wide", page_icon="🏨")

# Custom CSS untuk mempercantik tampilan
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# Nama file CSV
INV_FILE = "data_inventaris.csv"
LEDGER_FILE = "data_transaksi.csv"
BOOKING_FILE = "data_booking.csv"
ROOM_FILE = "data_kamar.csv"

# --- 2. DATA ENGINE ---
def load_data():
    inv = pd.read_csv(INV_FILE) if os.path.exists(INV_FILE) else pd.DataFrame(columns=['Barang', 'Stok', 'Harga_Modal', 'Harga_Jual'])
    leg = pd.read_csv(LEDGER_FILE) if os.path.exists(LEDGER_FILE) else pd.DataFrame(columns=['Tanggal', 'Barang', 'Tipe', 'Jumlah', 'Total_IDR'])
    book = pd.read_csv(BOOKING_FILE) if os.path.exists(BOOKING_FILE) else pd.DataFrame(columns=['Tanggal', 'Customer', 'No_Kamar', 'Malam', 'Biaya', 'Status'])
    # Default 10 kamar jika file belum ada
    if os.path.exists(ROOM_FILE):
        rooms = pd.read_csv(ROOM_FILE)
    else:
        rooms = pd.DataFrame({'No_Kamar': [str(101+i) for i in range(10)], 'Tipe': 'Standard'})
    return inv, leg, book, rooms

def save_data(inv, leg, book, rooms):
    inv.to_csv(INV_FILE, index=False)
    leg.to_csv(LEDGER_FILE, index=False)
    book.to_csv(BOOKING_FILE, index=False)
    rooms.to_csv(ROOM_FILE, index=False)

# Inisialisasi Session State
if 'inventory' not in st.session_state:
    st.session_state.inventory, st.session_state.ledger, st.session_state.booking, st.session_state.rooms = load_data()

# --- 3. LOGIK VISUAL GRID (ROOM RACK) ---
def render_hotel_grid():
    st.subheader("🗓️ Visual Room Rack (14 Hari)")
    
    # Range tanggal: Hari ini + 13 hari ke depan
    start_date = datetime.now().date()
    date_range = [start_date + timedelta(days=x) for x in range(14)]
    date_labels = [d.strftime("%d\n%b") for d in date_range]
    
    # Daftar Kamar
    room_list = st.session_state.rooms['No_Kamar'].tolist()
    
    # Buat DataFrame kosong untuk Grid
    grid_df = pd.DataFrame("🟢 Tersedia", index=room_list, columns=date_labels)
    
    # Isi Grid berdasarkan data booking
    for _, row in st.session_state.booking.iterrows():
        try:
            checkin = datetime.strptime(str(row['Tanggal']), "%Y-%m-%d").date()
            malam = int(row['Malam'])
            
            for i in range(malam):
                current_date = checkin + timedelta(days=i)
                if start_date <= current_date < start_date + timedelta(days=14):
                    date_label = current_date.strftime("%d\n%b")
                    room_label = str(row['No_Kamar'])
                    if room_label in grid_df.index:
                        grid_df.at[room_label, date_label] = f"🔴 {row['Customer']}"
        except:
            continue

    # Styling Warna
    def style_grid(val):
        if "🔴" in val:
            return 'background-color: #ff4b4b; color: white; font-size: 11px; font-weight: bold; text-align: center;'
        return 'background-color: #2ecc71; color: white; font-size: 10px; text-align: center;'

    st.dataframe(grid_df.style.map(style_grid), use_container_width=True, height=400)

# --- 4. HEADER & DASHBOARD ---
st.title("🏨 Hotel Flow Grid Pro")

# Ringkasan Kas
cash_in = st.session_state.ledger[st.session_state.ledger['Tipe'].isin(['Penjualan', 'Booking'])]['Total_IDR'].sum()
cash_out = st.session_state.ledger[st.session_state.ledger['Tipe'] == 'Stok Masuk']['Total_IDR'].sum()
balance = cash_in - cash_out

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Pendapatan", f"Rp {cash_in:,.0f}".replace(",", "."))
c2.metric("Total Modal/Stok", f"Rp {cash_out:,.0f}".replace(",", "."))
c3.metric("Saldo Bersih", f"Rp {balance:,.0f}".replace(",", "."), delta=f"Rp {balance:,.0f}".replace(",", "."))
c4.metric("Kamar Terisi (Hari Ini)", f"{len(st.session_state.booking[st.session_state.booking['Tanggal'] == str(datetime.now().date())])} Kamar")

st.divider()

# --- 5. TAMPILAN UTAMA ---
render_hotel_grid()

st.divider()

# --- 6. INPUT & MANAJEMEN ---
tab_book, tab_inv, tab_settings = st.tabs(["📅 Reservasi Baru", "🛒 Penjualan Produk", "⚙️ Pengaturan"])

with tab_book:
    st.subheader("Input Reservasi")
    with st.form("new_booking"):
        col_b1, col_b2, col_b3 = st.columns(3)
        b_date = col_b1.date_input("Tanggal Check-in")
        b_name = col_b2.text_input("Nama Tamu")
        b_room = col_b3.selectbox("No Kamar", st.session_state.rooms['No_Kamar'].tolist())
        
        col_b4, col_b5, col_b6 = st.columns(3)
        b_malam = col_b4.number_input("Durasi (Malam)", min_value=1)
        b_price = col_b5.number_input("Total Bayar / DP (Rp)", min_value=0, step=50000)
        b_stat = col_b6.selectbox("Status", ["Lunas", "DP"])
        
        if st.form_submit_button("Simpan Reservasi"):
            # Update Data Booking
            new_row = pd.DataFrame([{'Tanggal': str(b_date), 'Customer': b_name, 'No_Kamar': str(b_room), 'Malam': b_malam, 'Biaya': b_price, 'Status': b_stat}])
            st.session_state.booking = pd.concat([st.session_state.booking, new_row], ignore_index=True)
            
            # Update Arus Kas
            new_cash = pd.DataFrame([{'Tanggal': datetime.now().strftime("%Y-%m-%d"), 'Barang': f"Kamar {b_room} ({b_name})", 'Tipe': 'Booking', 'Jumlah': 1, 'Total_IDR': b_price}])
            st.session_state.ledger = pd.concat([st.session_state.ledger, new_cash], ignore_index=True)
            
            save_data(st.session_state.inventory, st.session_state.ledger, st.session_state.booking, st.session_state.rooms)
            st.success("Booking Berhasil!"); st.rerun()

with tab_inv:
    st.subheader("Input Penjualan Barang")
    with st.form("new_sale"):
        col_s1, col_s2, col_s3 = st.columns(3)
        s_type = col_s1.selectbox("Tipe", ["Penjualan", "Stok Masuk"])
        s_item = col_s2.selectbox("Produk", st.session_state.inventory['Barang'].tolist() if not st.session_state.inventory.empty else ["Kosong"])
        s_qty = col_s3.number_input("Qty", min_value=1)
        
        if st.form_submit_button("Proses Barang"):
            if s_item != "Kosong":
                idx = st.session_state.inventory.index[st.session_state.inventory['Barang'] == s_item][0]
                price = st.session_state.inventory.at[idx, 'Harga_Jual'] if s_type == "Penjualan" else st.session_state.inventory.at[idx, 'Harga_Modal']
                
                # Update Stok
                if s_type == "Penjualan":
                    st.session_state.inventory.at[idx, 'Stok'] -= s_qty
                else:
                    st.session_state.inventory.at[idx, 'Stok'] += s_qty
                
                # Update Kas
                new_cash = pd.DataFrame([{'Tanggal': datetime.now().strftime("%Y-%m-%d"), 'Barang': s_item, 'Tipe': s_type, 'Jumlah': s_qty, 'Total_IDR': price * s_qty}])
                st.session_state.ledger = pd.concat([st.session_state.ledger, new_cash], ignore_index=True)
                
                save_data(st.session_state.inventory, st.session_state.ledger, st.session_state.booking, st.session_state.rooms)
                st.success("Stok Diperbarui!"); st.rerun()

with tab_settings:
    st.subheader("Edit Master Data")
    edit_mode = st.radio("Pilih Data yang Ingin Diedit:", ["Daftar Kamar", "Daftar Produk/Stok", "Riwayat Booking", "Arus Kas"])
    
    if edit_mode == "Daftar Kamar":
        upd_rooms = st.data_editor(st.session_state.rooms, num_rows="dynamic", use_container_width=True)
        if st.button("Simpan Perubahan Kamar"):
            st.session_state.rooms = upd_rooms
            save_data(st.session_state.inventory, st.session_state.ledger, st.session_state.booking, st.session_state.rooms)
            st.rerun()
            
    elif edit_mode == "Daftar Produk/Stok":
        upd_inv = st.data_editor(st.session_state.inventory, num_rows="dynamic", use_container_width=True,
                                column_config={"Harga_Modal": st.column_config.NumberColumn(format="Rp %d"),
                                               "Harga_Jual": st.column_config.NumberColumn(format="Rp %d")})
        if st.button("Simpan Perubahan Produk"):
            st.session_state.inventory = upd_inv
            save_data(st.session_state.inventory, st.session_state.ledger, st.session_state.booking, st.session_state.rooms)
            st.rerun()

    elif edit_mode == "Riwayat Booking":
        upd_book = st.data_editor(st.session_state.booking, num_rows="dynamic", use_container_width=True,
                                 column_config={"Biaya": st.column_config.NumberColumn(format="Rp %d")})
        if st.button("Simpan Perubahan Booking"):
            st.session_state.booking = upd_book
            save_data(st.session_state.inventory, st.session_state.ledger, st.session_state.booking, st.session_state.rooms)
            st.rerun()

    elif edit_mode == "Arus Kas":
        upd_leg = st.data_editor(st.session_state.ledger, num_rows="dynamic", use_container_width=True,
                                column_config={"Total_IDR": st.column_config.NumberColumn(format="Rp %d")})
        if st.button("Simpan Perubahan Kas"):
            st.session_state.ledger = upd_leg
            save_data(st.session_state.inventory, st.session_state.ledger, st.session_state.booking, st.session_state.rooms)
            st.rerun()
