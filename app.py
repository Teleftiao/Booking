import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Sistem Manajemen Terpadu", layout="wide")

# File paths for storage
INV_FILE = "data_inventaris.csv"
LEDGER_FILE = "data_transaksi.csv"
BOOKING_FILE = "data_booking.csv"

# --- 2. DATA ENGINE (LOAD/SAVE) ---
def load_data():
    # Load or create Inventory
    if os.path.exists(INV_FILE):
        inv = pd.read_csv(INV_FILE)
    else:
        inv = pd.DataFrame(columns=['Barang', 'Stok', 'Harga_Modal', 'Harga_Jual'])
    
    # Load or create Ledger (Cashflow)
    if os.path.exists(LEDGER_FILE):
        leg = pd.read_csv(LEDGER_FILE)
    else:
        leg = pd.DataFrame(columns=['Tanggal', 'Barang', 'Tipe', 'Jumlah', 'Total_IDR'])
    
    # Load or create Booking List
    if os.path.exists(BOOKING_FILE):
        book = pd.read_csv(BOOKING_FILE)
    else:
        book = pd.DataFrame(columns=['Tanggal', 'Customer', 'Jml_Kamar', 'Total_Kamar', 'Biaya', 'Status', 'Ket'])
    
    return inv, leg, book

def save_data(inv, leg, book):
    inv.to_csv(INV_FILE, index=False)
    leg.to_csv(LEDGER_FILE, index=False)
    book.to_csv(BOOKING_FILE, index=False)

# Initialize Session State
if 'inventory' not in st.session_state:
    st.session_state.inventory, st.session_state.ledger, st.session_state.booking = load_data()

# --- 3. UI - HEADER & METRICS ---
st.title("🏨 Manajer Bisnis: Stok, Booking & Kas")
st.caption("Aplikasi pencatatan stok barang, reservasi kamar, dan arus kas otomatis.")

# Calculations
cash_in = st.session_state.ledger[st.session_state.ledger['Tipe'].isin(['Penjualan', 'Booking'])]['Total_IDR'].sum()
cash_out = st.session_state.ledger[st.session_state.ledger['Tipe'] == 'Stok Masuk']['Total_IDR'].sum()
net_balance = cash_in - cash_out

# Metric Cards
m1, m2, m3 = st.columns(3)
m1.metric("Pendapatan (Uang Masuk)", f"Rp {cash_in:,.0f}".replace(",", "."))
m2.metric("Pengeluaran (Modal/Stok)", f"Rp {cash_out:,.0f}".replace(",", "."))
m3.metric("Saldo Bersih", f"Rp {net_balance:,.0f}".replace(",", "."), delta=f"Rp {net_balance:,.0f}".replace(",", "."))

st.divider()

# --- 4. UI - INPUT AREA ---
st.subheader("➕ Tambah Data Baru")
tab_stok, tab_book = st.tabs(["🛒 Transaksi Barang", "📅 Booking Kamar"])

with tab_stok:
    with st.expander("Catat Penjualan atau Restock"):
        c1, c2, c3, c4 = st.columns([2, 2, 1, 2])
        t_type = c1.selectbox("Tipe Transaksi", ["Penjualan", "Stok Masuk"])
        t_item = c2.selectbox("Pilih Produk", st.session_state.inventory['Barang'].tolist() if not st.session_state.inventory.empty else ["Belum Ada Produk"])
        t_qty = c3.number_input("Jumlah", min_value=1, step=1)
        
        if c4.button("Konfirmasi Transaksi", use_container_width=True):
            if not st.session_state.inventory.empty and t_item != "Belum Ada Produk":
                idx = st.session_state.inventory.index[st.session_state.inventory['Barang'] == t_item][0]
                price = st.session_state.inventory.at[idx, 'Harga_Jual'] if t_type == "Penjualan" else st.session_state.inventory.at[idx, 'Harga_Modal']
                total = price * t_qty
                
                # Logic Update Stok
                if t_type == "Penjualan":
                    if st.session_state.inventory.at[idx, 'Stok'] >= t_qty:
                        st.session_state.inventory.at[idx, 'Stok'] -= t_qty
                    else:
                        st.error("Stok Tidak Mencukupi!"); st.stop()
                else:
                    st.session_state.inventory.at[idx, 'Stok'] += t_qty

                # Record to Ledger
                new_leg = pd.DataFrame([{'Tanggal': datetime.now().strftime("%Y-%m-%d %H:%M"), 'Barang': t_item, 'Tipe': t_type, 'Jumlah': t_qty, 'Total_IDR': total}])
                st.session_state.ledger = pd.concat([st.session_state.ledger, new_leg], ignore_index=True)
                
                save_data(st.session_state.inventory, st.session_state.ledger, st.session_state.booking)
                st.success(f"Berhasil mencatat {t_type} {t_item}"); st.rerun()

with tab_book:
    with st.expander("Input Reservasi Kamar"):
        with st.form("form_booking", clear_on_submit=True):
            bc1, bc2, bc3 = st.columns(3)
            b_date = bc1.date_input("Tanggal Reservasi")
            b_name = bc2.text_input("Nama Customer")
            b_cost = bc3.number_input("Biaya / DP (Rp)", min_value=0, step=50000)
            
            bc4, bc5, bc6 = st.columns(3)
            b_qty_room = bc4.number_input("Jumlah Kamar", min_value=1)
            b_cap = bc5.number_input("Total Kapasitas Kamar", min_value=1)
            b_status = bc6.selectbox("Status Pembayaran", ["DP", "Lunas"])
            
            b_note = st.text_area("Catatan (Optional)")
            
            if st.form_submit_button("Simpan Booking"):
                if b_name:
                    # Save to Booking
                    new_b = pd.DataFrame([{
                        'Tanggal': str(b_date), 'Customer': b_name, 'Jml_Kamar': b_qty_room, 
                        'Total_Kamar': b_cap, 'Biaya': b_cost, 'Status': b_status, 'Ket': b_note
                    }])
                    st.session_state.booking = pd.concat([st.session_state.booking, new_b], ignore_index=True)
                    
                    # Save to Ledger
                    new_l = pd.DataFrame([{
                        'Tanggal': datetime.now().strftime("%Y-%m-%d %H:%M"), 
                        'Barang': f"Booking: {b_name}", 'Tipe': 'Booking', 'Jumlah': b_qty_room, 'Total_IDR': b_cost
                    }])
                    st.session_state.ledger = pd.concat([st.session_state.ledger, new_l], ignore_index=True)
                    
                    save_data(st.session_state.inventory, st.session_state.ledger, st.session_state.booking)
                    st.success("Booking Berhasil Disimpan!"); st.rerun()

st.divider()

# --- 5. UI - DATA TABLES (EDITABLE) ---
st.subheader("📝 Kelola & Edit Data (Klik sel untuk mengubah)")

edit_book, edit_stok, edit_kas = st.tabs(["📅 Daftar Booking", "📦 Stok & Produk", "🧾 Riwayat Kas"])

with edit_book:
    # Editable Booking Table
    upd_book = st.data_editor(
        st.session_state.booking, 
        use_container_width=True, 
        num_rows="dynamic",
        key="edit_book_table",
        column_config={
            "Biaya": st.column_config.NumberColumn("Biaya (Rp)", format="Rp %d"),
        }
    )
    if st.button("💾 Simpan Perubahan Booking"):
        st.session_state.booking = upd_book
        save_data(st.session_state.inventory, st.session_state.ledger, st.session_state.booking)
        st.success("Data Booking Diperbarui!"); st.rerun()

with edit_stok:
    # Editable Inventory Table
    upd_inv = st.data_editor(
        st.session_state.inventory, 
        use_container_width=True, 
        num_rows="dynamic",
        key="edit_inv_table",
        column_config={
            "Harga_Modal": st.column_config.NumberColumn("Harga Modal", format="Rp %d"),
            "Harga_Jual": st.column_config.NumberColumn("Harga Jual", format="Rp %d"),
        }
    )
    if st.button("💾 Simpan Perubahan Stok"):
        st.session_state.inventory = upd_inv
        save_data(st.session_state.inventory, st.session_state.ledger, st.session_state.booking)
        st.success("Data Stok Diperbarui!"); st.rerun()

with edit_kas:
    # Editable Ledger Table
    upd_leg = st.data_editor(
        st.session_state.ledger, 
        use_container_width=True, 
        num_rows="dynamic",
        key="edit_leg_table",
        column_config={
            "Total_IDR": st.column_config.NumberColumn("Total (Rp)", format="Rp %d"),
        }
    )
    if st.button("💾 Simpan Perubahan Kas"):
        st.session_state.ledger = upd_leg
        save_data(st.session_state.inventory, st.session_state.ledger, st.session_state.booking)
        st.success("Data Kas Diperbarui!"); st.rerun()