import pandas as pd
import streamlit as st

# คำสั่งที่ใช้ในการrun code => streamlit run app.py

# อ่านชุดข้อมูลจากไฟล์ CSV
df = pd.read_csv(r"สถานที่ท่องเที่ยวในจังหวัดขอนแก่น1.csv")

# title
st.title('TOURIST ATTRACTIONS🚩')

# เส้นแบ่ง
st.markdown('<div style="background-color: #FFE5D9; border-radius: 5px; padding: 1px; margin-bottom: 5px;"></div>', unsafe_allow_html=True)

# แทนที่ค่า NaN ด้วย "ไม่มีการระบุ"
df.fillna("ไม่มีการระบุ", inplace=True)
# ให้รหัสไปรษณีย์เป็นสตริง
df['postalcode'] = df['postalcode'].astype(str)
# ตัดช่องว่างนำหน้าและต่อท้ายออกจากชื่อคอลัมน์
df.columns = df.columns.str.strip()

# สร้างตัวเลือกสำหรับ Category
category_options = df['Category'].unique()
selected_categories = st.multiselect('เลือกประเภทสถานที่ท่องเที่ยว', category_options)

# สร้างตัวเลือกสำหรับ Target Group
target_group_options = ['กลุ่มครอบครัว', 'กลุ่มวัยทำงาน', 'กลุ่มนักเรียนนักศึกษา', 'เยาวชน', 'วัยรุ่น', 'กลุ่มคู่รัก', 'คู่แต่งงาน', 'ทุกช่วงวัย']
selected_target_groups = st.multiselect('เลือกกลุ่มเป้าหมาย', target_group_options)

# Input ของ budget
budget = st.number_input('ป้อนงบประมาณของคุณ', min_value=0.0, format='%f')

# Input age และตรวจสอบ age
age = st.number_input('ป้อนอายุ', min_value=0, max_value=150, value=0)

# เลือก ticket price ที่จะแสดงโดยขึ้นอยู่กับอายุ
if age >= 18:
    ticket_price_column = 'ticketPrice ThaiAdult'
else:
    ticket_price_column = 'ticketPrice ThaiChild'

# กรองข้อมูลตาม Category และ Target Group
filtered_df = df[df['Category'].isin(selected_categories) & df['Target Group'].apply(lambda x: any(target in x for target in selected_target_groups))]

# แสดงข้อมูลที่กรอง
# ใช้ st.container() ร่วมกับการกำหนดสไตล์ CSS
count = st.number_input('จำนวนสถานที่ที่ต้องการแสดง', min_value=1, value=1)
if len(filtered_df) >= count:
    filtered_df = filtered_df.head(count)
for index, row in filtered_df.iterrows():
    # ใช้ st.container() เพื่อสร้างบล็อกที่สามารถกำหนดสไตล์ได้
    with st.container():
        # กำหนดสไตล์ CSS ด้วย st.markdown() และใช้ unsafe_allow_html=True เพื่อให้ HTML ทำงาน
        st.markdown(f"""
            <style>
            .block{index} {{
                border: 2px solid #b07d62;  /* กำหนดสีขอบ */
                border-radius: 10px;  /* กำหนดรูปแบบขอบให้มน */
                padding: 10px;  /* กำหนดระยะห่างภายใน */
                margin: 10px 0;  /* กำหนดระยะห่างภายนอก */
            }}
            </style>
            <div class="block{index}">
                <h4>{row['Name']}</h4>
                <p>ประเภท: {row["Category"]}</p>
                <p>{row["detail"]}</p>
                <p>ที่อยู่: {row["province"]} {row["district"]} {row["subdistrict"]} {row["postalcode"]}</p>
                <p>ค่าเข้าชม: {row[ticket_price_column]}</p>
                <p>เหมาะสำหรับ: {row["Target Group"]}</p>
                <p>การขนส่ง: {row["transportation"]}</p>
                <p>สิ่งอำนวยความสะดวก: {row["facility"]}</p>
                <p>ติดต่อ: {row["telephone"]}</p>
                <p>eMail: {row["eMail"]}</p>
                <p>Website: {row["Website"]}</p>
                <p>ช่วงเวลาเปิดทำการ: {row["businessHour"]}</p>
            </div>
        """, unsafe_allow_html=True)
    count -= 1
    if count == 0:
        break
# แสดงจำนวนสถานที่ที่ต้องการแนะนำเพียงพอต่อความต้องการหรือไม่
if len(filtered_df) < count:
    st.warning('มีสถานที่ที่ต้องการแนะนำไม่เพียงพอต่อความต้องการ')
    count = len(filtered_df)
st.info(f'มีสถานที่แนะนำ {count} สถานที่')

# เส้นแบ่ง
st.markdown('<div style="background-color: #FFE5D9; border-radius: 5px; padding: 1px; margin-bottom: 5px;"></div>', unsafe_allow_html=True)

# คำนวณผลรวมของ ticket price
total_ticket_price = filtered_df[ticket_price_column].sum()

# แสดงงบประมาณของผู้ใช้
st.markdown(f'<div style="border: 2px solid #9d6b53; border-radius: 5px; padding: 10px; margin-bottom: 10px;">งบประมาณของคุณ: {budget}</div>', unsafe_allow_html=True)

# แสดงค่าเข้าชมของแต่ละสถานที่ท่องเที่ยว
st.write("ค่าเข้าชมแต่ละสถานที่")
for index, row in filtered_df.iterrows():
    st.write(f"{row['Name']}: {row[ticket_price_column]}")

# แสดงผลรวมของราคาตั๋ว
st.markdown(f'<div style="border: 2px solid #774936; border-radius: 5px; padding: 10px;">ผลรวมค่าเข้าชมทั้งหมด: {total_ticket_price}</div>', unsafe_allow_html=True)

# เช็คว่าค่าใช้จ่ายเกินงบประมาณหรือไม่และแสดงข้อความ
if total_ticket_price > budget:
    st.error('ค่าใช้จ่ายเกินงบประมาณของคุณ')
else:
    st.success('ค่าใช้จ่ายยังไม่เกินงบประมาณของคุณ')


