import streamlit as st
import pandas as pd
from datetime import date
import json
import os

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
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background: #667eea;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    .stButton>button:hover {
        background: #5a67d8;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    /* 改善文字陰影效果 */
    h1, h2, h3, h4, h5, h6 {
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    .metric-card h3 {
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        color: #333;
    }
    .form-section h2, .form-section h3 {
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
        color: #333;
    }
    .main-header h1 {
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# 主標題
st.markdown("""
<div class="main-header">
    <h1>🏥 醫院物品租借管理系統</h1>
    <p>💾 資料持久化 • 自動保存 • 簡化版本</p>
</div>
""", unsafe_allow_html=True)

# 資料持久化函數
def load_data():
    """從本地檔案載入資料"""
    try:
        if os.path.exists('hospital_loan_data.json'):
            with open('hospital_loan_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        return []
    except Exception as e:
        st.error(f"載入資料失敗：{str(e)}")
        return []

def save_data(data):
    """儲存資料到本地檔案"""
    try:
        with open('hospital_loan_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"儲存資料失敗：{str(e)}")
        return False

# 初始化資料
if 'records' not in st.session_state:
    st.session_state.records = load_data()

# 建立側邊欄導覽
st.sidebar.markdown("### 📋 功能選單")
menu = ["📝 新增租借紀錄", "📊 查看所有紀錄", "📈 數據統計", "⚙️ 系統設定"]
choice = st.sidebar.selectbox("", menu)

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
    
    # 主管資訊 (簡化版本 - 無簽名)
    st.markdown('<div class="form-section"><h3>👤 主管資訊</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**👤 借用部門主管**")
        st.markdown("*Borrow Dept. / Ward i/c*")
        borrow_manager = st.text_input("Borrow Manager Name", placeholder="請輸入姓名")
    
    with col2:
        st.markdown("**👤 借出部門主管**")
        st.markdown("*Loan Dept. / Ward i/c*")
        loan_manager = st.text_input("Loan Manager Name", placeholder="請輸入姓名")
    
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
                    "狀態": "租借中",
                    "建立時間": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # 檢查是否已有相同表單編號
                existing_record = next((r for r in st.session_state.records if r["表單編號"] == form_no), None)
                if existing_record:
                    st.error(f"❌ 表單編號 {form_no} 已存在！")
                else:
                    # 儲存到 session state
                    st.session_state.records.append(new_record)
                    
                    # 儲存到檔案
                    if save_data(st.session_state.records):
                        st.markdown('<div class="success-message">✅ 紀錄已成功儲存！資料已持久化保存。</div>', unsafe_allow_html=True)
                        st.balloons()
                    else:
                        st.warning("⚠️ 紀錄已新增到記憶體，但檔案儲存失敗")
            else:
                st.error("❌ 請填寫必填欄位：表單編號、領用部門、物品編號、摘要")

elif choice == "📊 查看所有紀錄":
    st.markdown('<div class="form-section"><h2>📋 租借紀錄總覽</h2></div>', unsafe_allow_html=True)
    
    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        
        # 狀態篩選
        status_filter = st.selectbox("🔍 篩選狀態", ["全部", "租借中", "已歸還"])
        if status_filter != "全部":
            filtered_df = df[df["狀態"] == status_filter]
        else:
            filtered_df = df
        
        # 快速歸還功能
        if '狀態' in filtered_df.columns:
            rental_records = filtered_df[filtered_df['狀態'] == '租借中']
            if not rental_records.empty:
                st.markdown("---")
                st.markdown("### 🔄 快速歸還")
                st.write("點擊按鈕快速確認物品歸還：")
                
                # 創建一個更好的快速歸還界面
                for idx, row in rental_records.iterrows():
                    original_idx = filtered_df.index.get_loc(idx)
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    with col1:
                        st.write(f"**{row['表單編號']}** - {row['摘要']}")
                    with col2:
                        st.write(f"📅 {row['借用日期']}")
                    with col3:
                        st.write(f"👤 {row['借用部門主管']}")
                    with col4:
                        if st.button(f"🔄 確認歸還", key=f"return_{original_idx}"):
                            # 找到原始記錄的索引
                            for i, record in enumerate(st.session_state.records):
                                if record['表單編號'] == row['表單編號']:
                                    # 更新狀態和歸還日期
                                    st.session_state.records[i]['狀態'] = '已歸還'
                                    st.session_state.records[i]['實際歸還日期'] = date.today().strftime("%Y-%m-%d")
                                    save_data(st.session_state.records)
                                    st.success(f"✅ 表單 {row['表單編號']} 已確認歸還！")
                                    st.rerun()
                                    break
        
        # 顯示資料表格
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
            return_rate = (len(df[df["狀態"] == "已歸還"]) / len(df) * 100 if len(df) > 0 else 0)
            st.markdown(f'<div class="metric-card">📈 歸還率<br><h3>{return_rate:.1f}%</h3></div>', unsafe_allow_html=True)
        
        # 狀態更新功能
        st.markdown("---")
        st.markdown("### 🔄 更新紀錄狀態")
        
        if not filtered_df.empty:
            selected_record = st.selectbox(
                "選擇要更新的紀錄",
                options=filtered_df.index,
                format_func=lambda x: f"{filtered_df.loc[x, '表單編號']} - {filtered_df.loc[x, '摘要']} - {filtered_df.loc[x, '狀態']}"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                new_status = st.selectbox("新狀態", ["租借中", "已歸還"])
            with col2:
                if st.button("🔄 更新狀態"):
                    st.session_state.records[selected_record]["狀態"] = new_status
                    save_data(st.session_state.records)
                    st.success("✅ 狀態已更新！")
                    st.rerun()
        
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
    
    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        
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
        
        # 詳細統計表格
        st.markdown("### 📊 詳細統計")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**部門借用統計**")
            dept_table = pd.DataFrame({
                '部門': dept_stats.index,
                '借用次數': dept_stats.values
            })
            st.dataframe(dept_table, use_container_width=True)
        
        with col2:
            st.write("**物品借用統計**")
            item_table = pd.DataFrame({
                '物品編號': item_stats.head(5).index,
                '借用次數': item_stats.head(5).values
            })
            st.dataframe(item_table, use_container_width=True)
    else:
        st.info("📝 目前尚無任何紀錄。")

elif choice == "⚙️ 系統設定":
    st.markdown('<div class="form-section"><h2>⚙️ 系統設定</h2></div>', unsafe_allow_html=True)
    
    # 連接狀態
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔗 系統狀態")
        st.success("✅ 本地系統運行正常")
        st.metric("📊 總資料數", len(st.session_state.records))
        
        # 檢查資料檔案
        if os.path.exists('hospital_loan_data.json'):
            st.success("✅ 資料檔案存在")
            file_size = os.path.getsize('hospital_loan_data.json')
            st.metric("📁 檔案大小", f"{file_size} bytes")
        else:
            st.warning("⚠️ 資料檔案不存在")
    
    with col2:
        st.markdown("### 💾 資料持久化")
        st.info("ℹ️ 本地檔案儲存")
        st.write("🔐 資料儲存於 `hospital_loan_data.json`")
        st.write("🔄 自動保存所有操作")
        st.write("📱 支援多裝置同步")
        st.write("☁️ 簡化版本 - 無簽名")
    
    # 資料管理
    st.markdown("---")
    st.markdown("### 🗂️ 資料管理")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 重新載入資料"):
            st.session_state.records = load_data()
            st.success("✅ 資料已重新載入")
            st.rerun()
    
    with col2:
        if st.button("💾 強制保存資料"):
            if save_data(st.session_state.records):
                st.success("✅ 資料已保存")
            else:
                st.error("❌ 保存失敗")
    
    with col3:
        if st.button("🗑️ 清除所有資料"):
            if st.session_state.records:
                st.session_state.records = []
                save_data([])
                st.success("✅ 所有資料已清除")
                st.rerun()
    
    # 備份功能
    st.markdown("---")
    st.markdown("### 📦 備份與還原")
    
    if st.session_state.records:
        # 備份下載
        backup_json = json.dumps(st.session_state.records, ensure_ascii=False, indent=2)
        st.download_button(
            label="📦 下載備份檔案 (JSON)",
            data=backup_json,
            file_name=f"hospital_loan_backup_{date.today().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    
    # 還原功能
    st.markdown("#### 🔄 還原備份")
    uploaded_file = st.file_uploader("上傳備份檔案 (JSON)", type=['json'])
    
    if uploaded_file is not None:
        try:
            backup_data = json.loads(uploaded_file.read().decode('utf-8'))
            if st.button("🔄 還原備份"):
                st.session_state.records = backup_data
                save_data(backup_data)
                st.success("✅ 備份已還原")
                st.rerun()
        except Exception as e:
            st.error(f"❌ 還原失敗：{str(e)}")

# 側邊欄資訊
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 系統資訊")
st.sidebar.metric("🔄 租借中", len([r for r in st.session_state.records if r.get('狀態') == '租借中']))
st.sidebar.metric("📊 總紀錄", len(st.session_state.records))

# 檢查資料檔案狀態
if os.path.exists('hospital_loan_data.json'):
    st.sidebar.success("✅ 資料已持久化")
else:
    st.sidebar.warning("⚠️ 資料檔案不存在")

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 使用提示")
st.sidebar.write("• 資料自動保存到本地檔案")
st.sidebar.write("• 刷新網頁不會遺失資料")
st.sidebar.write("• 支援備份與還原")
st.sidebar.write("• 可隨時匯出資料")
st.sidebar.write("• 手機友好界面")
st.sidebar.write("• 簡化版本 - 無簽名")

# 頁腳
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #667eea; padding: 2rem;'>
    <p>🏥 醫院物品租借管理系統 v12.0</p>
    <p>💡 最終簡化版本 - 無電子簽名</p>
    <p>🌐 基於 Streamlit 的解決方案</p>
</div>
""", unsafe_allow_html=True)
