import streamlit as st
import pandas as pd
from datetime import date
import gspread
import os
import json

# 設定網頁標題和樣式
st.set_page_config(
    page_title="醫院物品租借管理系統", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定義 CSS 樣式
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .form-section {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        font-weight: bold;
    }
    .stButton>button {
        background: #667eea;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: #5a67d8;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# 主標題
st.markdown("""
<div class="main-header">
    <h1>🏥 醫院物品租借管理系統</h1>
    <p>🌐 雲端協作 • 即時同步 • 紙上管理</p>
</div>
""", unsafe_allow_html=True)

# 建立側邊欄導覽
st.sidebar.markdown("### 📋 功能選單")
menu = ["📝 新增租借紀錄", "📊 查看所有紀錄", "📈 數據統計", "⚙️ 系統設定"]
choice = st.sidebar.selectbox("", menu)

# Google Sheets 連接函數
def connect_to_google_sheets():
    try:
        # 從環境變數讀取認證
        credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
        
        if not credentials_json:
            st.sidebar.error("❌ 環境變數未設定")
            return None
        
        # 清理 JSON 字符串
        credentials_json = credentials_json.strip()
        
        # 處理換行字符
        credentials_json = credentials_json.replace('\\n', '\n')
        
        # 測試 JSON 解析
        try:
            parsed_credentials = json.loads(credentials_json)
            st.sidebar.success("✅ JSON 解析成功")
        except json.JSONDecodeError as e:
            st.sidebar.error(f"❌ JSON 解析失敗：{str(e)}")
            return None
        
        # 建立 Google 認證
        from google.oauth2.service_account import Credentials
        creds = Credentials.from_service_account_info(parsed_credentials, scopes=[
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ])
        
        # 授權 gspread
        client = gspread.authorize(creds)
        
        # 嘗試開啟試算表
        try:
            sheet = client.open('醫院物品租借系統')
            worksheet = sheet.worksheet('租借紀錄')
            st.sidebar.success("✅ Google Sheets 連接成功")
            return worksheet
        except gspread.SpreadsheetNotFound:
            # 自動建立試算表
            sheet = client.create('醫院物品租借系統')
            worksheet = sheet.add_worksheet('租借紀錄', rows=1000, cols=20)
            # 建立標題
            headers = ["表單編號", "領用部門", "日期", "物品編號", "摘要", "數量", 
                      "借用日期", "歸還日期", "備註", "借用部門主管", "借出部門主管", "狀態"]
            worksheet.append_row(headers)
            st.sidebar.success("✅ 試算表建立成功")
            return worksheet
            
    except Exception as e:
        st.sidebar.error(f"❌ 連接失敗：{str(e)}")
        return None

# 初始化 Google Sheets 連接
if 'google_worksheet' not in st.session_state:
    st.session_state.google_worksheet = connect_to_google_sheets()

# 初始化本地資料
if 'local_records' not in st.session_state:
    st.session_state.local_records = []

if choice == "📝 新增租借紀錄":
    st.markdown('<div class="form-section"><h2>📝 暫借物品表 (Temporary Transfer Form)</h2></div>', unsafe_allow_html=True)
    
    # 表單基本資訊
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**📋 表單編號**")
        form_no = st.text_input("No.", placeholder="例: 008913")
    
    with col2:
        st.markdown("**📅 日期**")
        form_date = st.date_input("Date", value=date.today())
    
    with col3:
        st.markdown("**🏢 領用部門**")
        dept = st.text_input("Borrow Department / Ward", placeholder="例: 內科")
    
    # 物品明細
    st.markdown('<div class="form-section"><h3>📦 物品明細</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🏷️ 物品編號**")
        item_code = st.text_input("Code No.", placeholder="例: MED-001")
        
        st.markdown("**📊 數量**")
        quantity = st.number_input("Quantity", min_value=1, step=1)
        
    with col2:
        st.markdown("**📝 摘要**")
        description = st.text_area("Description", placeholder="例: 血壓計", height=100)
        
        st.markdown("**📝 備註**")
        remark = st.text_area("Remark", placeholder="特殊需求或說明...", height=80)
    
    # 日期資訊
    st.markdown('<div class="form-section"><h3>📅 借用/歸還日期</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📤 借用日期**")
        loan_date = st.date_input("Date Loan", value=date.today())
    
    with col2:
        st.markdown("**📤 歸還日期**")
        return_date = st.date_input("Date Return")
    
    # 主管簽名
    st.markdown('<div class="form-section"><h3>✍️ 主管簽名</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**👤 借用部門主管**")
        st.markdown("*Borrow Dept. / Ward i/c*")
        st.markdown("*(簽名請用正楷)*")
        borrow_manager = st.text_input("Name", placeholder="請輸入姓名")
    
    with col2:
        st.markdown("**👤 借出部門主管**")
        st.markdown("*Loan Dept. / Ward i/c*")
        st.markdown("*(簽名請用正楷)*")
        loan_manager = st.text_input("Name", placeholder="請輸入姓名")
    
    # 提交按鈕
    st.markdown("---")
    submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
    with submit_col2:
        if st.button("📤 提交申請", use_container_width=True):
            if form_no and dept and item_code and description:
                new_record = {
                    "表單編號": form_no,
                    "領用部門": dept,
                    "日期": form_date.strftime("%Y-%m-%d"),
                    "物品編號": item_code,
                    "摘要": description,
                    "數量": str(quantity),
                    "借用日期": loan_date.strftime("%Y-%m-%d"),
                    "歸還日期": return_date.strftime("%Y-%m-%d"),
                    "備註": remark,
                    "借用部門主管": borrow_manager,
                    "借出部門主管": loan_manager,
                    "狀態": "租借中"
                }
                
                # 嘗試儲存到 Google Sheets
                if st.session_state.google_worksheet:
                    try:
                        worksheet = st.session_state.google_worksheet
                        worksheet.append_row([
                            form_no, dept, form_date.strftime("%Y-%m-%d"), 
                            item_code, description, str(quantity),
                            loan_date.strftime("%Y-%m-%d"), return_date.strftime("%Y-%m-%d"),
                            remark, borrow_manager, loan_manager, "租借中"
                        ])
                        st.markdown('<div class="success-message">✅ 紀錄已成功儲存至 Google Sheets！</div>', unsafe_allow_html=True)
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Google Sheets 儲存失敗：{str(e)}")
                        # 儲存到本地
                        st.session_state.local_records.append(new_record)
                        st.warning("⚠️ 已儲存至本地，請檢查 Google Sheets 連接")
                else:
                    # 儲存到本地
                    st.session_state.local_records.append(new_record)
                    st.warning("⚠️ 已儲存至本地，請檢查 Google Sheets 連接")
            else:
                st.error("❌ 請填寫必填欄位：表單編號、領用部門、物品編號、摘要")

elif choice == "📊 查看所有紀錄":
    st.markdown('<div class="form-section"><h2>📋 租借紀錄總覽</h2></div>', unsafe_allow_html=True)
    
    # 從 Google Sheets 讀取資料
    google_data = []
    if st.session_state.google_worksheet:
        try:
            worksheet = st.session_state.google_worksheet
            google_data = worksheet.get_all_records()
            st.success(f"✅ 從 Google Sheets 讀取了 {len(google_data)} 筆資料")
        except Exception as e:
            st.error(f"❌ Google Sheets 讀取失敗：{str(e)}")
    
    # 合併本地資料
    all_data = google_data + st.session_state.local_records
    
    if all_data:
        df = pd.DataFrame(all_data)
        
        # 狀態篩選
        status_filter = st.selectbox("🔍 篩選狀態", ["全部", "租借中", "已歸還"])
        if status_filter != "全部":
            filtered_df = df[df["狀態"] == status_filter]
        else:
            filtered_df = df
        
        st.dataframe(filtered_df, use_container_width=True)
        
        # 統計卡片
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="metric-card">📊 總紀錄數<br><h3>{}</h3></div>'.format(len(df)), unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card">🔄 租借中<br><h3>{}</h3></div>'.format(len(df[df["狀態"] == "租借中"])), unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-card">✅ 已歸還<br><h3>{}</h3></div>'.format(len(df[df["狀態"] == "已歸還"])), unsafe_allow_html=True)
        with col4:
            return_rate = (len(df[df["狀態"] == "已歸還"]) / len(df) * 100 if len(df) > 0 else 0
            st.markdown(f'<div class="metric-card">📈 歸還率<br><h3>{return_rate:.1f}%</h3></div>', unsafe_allow_html=True)
        
        # 匯出功能
        st.markdown("---")
        csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 下載紀錄 (CSV)",
            data=csv,
            file_name=f"hospital_loan_records_{date.today().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )
    else:
        st.info("📝 目前尚無任何紀錄。")

elif choice == "📈 數據統計":
    st.markdown('<div class="form-section"><h2>📈 數據統計分析</h2></div>', unsafe_allow_html=True)
    
    # 從 Google Sheets 讀取資料
    google_data = []
    if st.session_state.google_worksheet:
        try:
            worksheet = st.session_state.google_worksheet
            google_data = worksheet.get_all_records()
        except Exception as e:
            st.error(f"❌ Google Sheets 讀取失敗：{str(e)}")
    
    # 合併本地資料
    all_data = google_data + st.session_state.local_records
    
    if all_data:
        df = pd.DataFrame(all_data)
        
        # 部門統計
        dept_stats = df['領用部門'].value_counts()
        st.markdown("### 🏢 領用部門統計")
        st.bar_chart(dept_stats)
        
        # 物品統計
        item_stats = df['物品編號'].value_counts()
        st.markdown("### 📦 物品借用排行")
        st.bar_chart(item_stats.head(10))
        
        # 時間趨勢
        df['日期'] = pd.to_datetime(df['日期'])
        monthly_stats = df.groupby(df['日期'].dt.to_period('M')).size()
        st.markdown("### 📅 月度借用趨勢")
        st.line_chart(monthly_stats)
    else:
        st.info("📝 目前尚無任何紀錄。")

elif choice == "⚙️ 系統設定":
    st.markdown('<div class="form-section"><h2>⚙️ 系統設定</h2></div>', unsafe_allow_html=True)
    
    # 連接狀態
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔗 雲端連接狀態")
        if st.session_state.google_worksheet:
            st.success("✅ Google Sheets 連接正常")
            try:
                worksheet = st.session_state.google_worksheet
                data = worksheet.get_all_records()
                st.metric("📊 雲端資料數", len(data))
            except:
                st.write("📊 無法讀取統計")
        else:
            st.error("❌ Google Sheets 連接失敗")
    
    with col2:
        st.markdown("### 📊 本地資料狀態")
        st.metric("📊 本地資料數", len(st.session_state.local_records))
        credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
        if credentials_json:
            st.success("✅ 環境變數已設定")
        else:
            st.error("❌ 環境變數未設定")
    
    # 重新連接按鈕
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 重新連接 Google Sheets"):
            st.session_state.google_worksheet = connect_to_google_sheets()
            st.rerun()
    with col2:
        if st.button("🗑️ 清除本地資料"):
            st.session_state.local_records = []
            st.rerun()

# 側邊欄資訊
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 系統資訊")
if st.session_state.google_worksheet:
    try:
        worksheet = st.session_state.google_worksheet
        data = worksheet.get_all_records()
        st.sidebar.metric("🔄 租借中", len([d for d in data if d.get('狀態') == '租借中']))
        st.sidebar.metric("📊 雲端紀錄", len(data))
    except:
        st.sidebar.metric("📊 雲端紀錄", "N/A")
st.sidebar.metric("📊 本地紀錄", len(st.session_state.local_records))

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 使用提示")
st.sidebar.write("• 資料同步至 Google Sheets")
st.sidebar.write("• 支援本地備份")
st.sidebar.write("• 可隨時匯出資料")
st.sidebar.write("• 手機友好界面")

# 頁腳
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #667eea; padding: 2rem;'>
    <p>🏥 醫院物品租借管理系統 v12.0</p>
    <p>💡 Google 認證重新啟用版本</p>
    <p>🌐 本地備份 + 雲端同步</p>
</div>
""", unsafe_allow_html=True)
