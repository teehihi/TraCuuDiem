
from flask import Flask, render_template, request, jsonify, session
import pandas as pd

app = Flask(__name__)
app.secret_key = '210505'  # Cần để sử dụng session, tạo một key ngẫu nhiên

# Đường dẫn file CSV
DATA_FILE1 = 'data/diemthi1.csv'
DATA_FILE2 = 'data/diemthi2.csv'
DIEM_CHUAN_FILE = 'data/diemchuan.csv'

# Đọc dữ liệu từ các file CSV
try:
    df1 = pd.read_csv(DATA_FILE1, encoding='utf-8')
    df2 = pd.read_csv(DATA_FILE2, encoding='utf-8')
    df_diem_chuan = pd.read_csv(DIEM_CHUAN_FILE, encoding='utf-8')
    # Gộp hai DataFrame điểm thi lại thành một
    df = pd.concat([df1, df2], ignore_index=True)
except FileNotFoundError as e:
    print(f"Lỗi: không tìm thấy file {e.filename}. Vui lòng kiểm tra lại đường dẫn.")
    exit()

# Tạo bảng ánh xạ tổ hợp -> các môn tương ứng
to_hop_map = {
    'A00': ['Toán', 'Lí', 'Hóa'], 'A01': ['Toán', 'Lí', 'Ngoại ngữ'],
    'B00': ['Toán', 'Hóa', 'Sinh'], 'C00': ['Văn', 'Sử', 'Địa'],
    'D01': ['Văn', 'Toán', 'Ngoại ngữ'], 'D07': ['Toán', 'Hóa', 'Ngoại ngữ'],
    'D08': ['Toán', 'Sinh', 'Ngoại ngữ'], 'D09': ['Toán', 'Sử', 'Ngoại ngữ'],
    'D10': ['Toán', 'Địa', 'Ngoại ngữ'], 'D14': ['Văn', 'Sử', 'Ngoại ngữ'],
    'D15': ['Văn', 'Địa', 'Ngoại ngữ'],
    'D66': ['Văn', 'Giáo dục kinh tế và pháp luật', 'Ngoại ngữ'],
    'T00': ['Toán', 'Sinh', 'Năng khiếu TDTT'], 'H01': ['Toán', 'Văn', 'Vẽ Mỹ thuật'],
    'M00': ['Văn', 'Toán', 'Hát'], 'N00': ['Văn', 'Năng khiếu Âm nhạc 1', 'Năng khiếu Âm nhạc 2']
}

# Ánh xạ mã tỉnh với tên tỉnh
ma_tinh_map = {
    '01': 'Hà Nội', '02': 'TP. Hồ Chí Minh', '03': 'Hải Phòng', '04': 'Đà Nẵng', '05': 'Hà Giang',
    '06': 'Cao Bằng', '07': 'Lai Châu', '08': 'Lào Cai', '09': 'Tuyên Quang', '10': 'Lạng Sơn',
    '11': 'Bắc Kạn', '12': 'Thái Nguyên', '13': 'Yên Bái', '14': 'Sơn La', '15': 'Phú Thọ',
    '16': 'Vĩnh Phúc', '17': 'Quảng Ninh', '18': 'Bắc Giang', '19': 'Bắc Ninh', '21': 'Hải Dương',
    '22': 'Hưng Yên', '23': 'Hòa Bình', '24': 'Hà Nam', '25': 'Nam Định', '26': 'Thái Bình',
    '27': 'Ninh Bình', '28': 'Thanh Hóa', '29': 'Nghệ An', '30': 'Hà Tĩnh', '31': 'Quảng Bình',
    '32': 'Quảng Trị', '33': 'Thừa Thiên Huế', '34': 'Quảng Nam', '35': 'Quảng Ngãi', '36': 'Kon Tum',
    '37': 'Bình Định', '38': 'Gia Lai', '39': 'Phú Yên', '40': 'Đắk Lắk', '41': 'Khánh Hòa',
    '42': 'Lâm Đồng', '43': 'Bình Phước', '44': 'Bình Dương', '45': 'Ninh Thuận', '46': 'Tây Ninh',
    '47': 'Bình Thuận', '48': 'Đồng Nai', '49': 'Long An', '50': 'Đồng Tháp', '51': 'An Giang',
    '52': 'Bà Rịa - Vũng Tàu', '53': 'Tiền Giang', '54': 'Kiên Giang', '55': 'Cần Thơ', '56': 'Bến Tre',
    '57': 'Vĩnh Long', '58': 'Trà Vinh', '59': 'Sóc Trăng', '60': 'Bạc Liêu', '61': 'Cà Mau',
    '62': 'Điện Biên', '63': 'Đăk Nông', '64': 'Hậu Giang'
}

def tinh_diem_tohop(row_dict):
    tohop_diem = {}
    for toh, mons in to_hop_map.items():
        # Kiểm tra xem tất cả các môn trong tổ hợp có trong điểm của thí sinh không
        valid_mons = [m for m in mons if m in row_dict and pd.notna(row_dict[m])]
        if len(valid_mons) == len(mons):
            tohop_diem[toh] = round(sum(row_dict[m] for m in mons), 2)
    return tohop_diem

def tim_truong_phu_hop(tohop_diem):
    suitable_schools = []
    for _, row in df_diem_chuan.iterrows():
        to_hop_list = str(row.get('Tổ hợp môn', '')).split('; ')
        diem_chuan = row.get('Điểm chuẩn 2024')
        truong = row.get('Trường đào tạo')
        nganh = row.get('Tên ngành')

        # Bỏ qua nếu thiếu thông tin quan trọng
        if not all([to_hop_list, isinstance(diem_chuan, (int, float)), truong, nganh]):
            continue

        for toh, diem in tohop_diem.items():
            if toh in to_hop_list and diem >= diem_chuan:
                suitable_schools.append({
                    'truong': truong, 'nganh': nganh, 'toh': toh,
                    'diem_chuan': diem_chuan, 'diem': diem
                })
    # Sắp xếp mặc định theo điểm chuẩn giảm dần
    return sorted(suitable_schools, key=lambda x: x['diem_chuan'], reverse=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Lấy dữ liệu từ session nếu có
    result = session.get('result', None)
    error = None
    
    # Các biến này sẽ được xác định trong khối POST
    filtered_schools = None
    selected_school = ''
    selected_major = ''

    # Luôn lấy danh sách đầy đủ cho datalist
    schools_list = sorted(df_diem_chuan['Trường đào tạo'].dropna().unique().tolist())
    majors_list = sorted(df_diem_chuan['Tên ngành'].dropna().unique().tolist())

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'lookup':
            session.clear()
            sbd = request.form.get('sbd')
            
            try:
                row = df[df['SOBAODANH'] == int(sbd)]
                if row.empty:
                    error = f"Không tìm thấy SBD {sbd}"
                    result = None
                else:
                    row_data = row.iloc[0].to_dict()
                    diem_mon = {mon: diem for mon, diem in row_data.items()
                                if isinstance(diem, (int, float)) and pd.notna(diem) and mon != 'SOBAODANH'}
                    tohop_diem = tinh_diem_tohop(diem_mon)
                    ma_tinh = str(sbd)[:2]
                    
                    # CHỈ LƯU KẾT QUẢ ĐIỂM VÀO SESSION (nhỏ gọn)
                    result = {
                        'sbd': sbd,
                        'ten_tinh': ma_tinh_map.get(ma_tinh, 'Không xác định'),
                        'diem': diem_mon,
                        'tohop_diem': tohop_diem
                    }
                    session['result'] = result
                    
                    # Tính toán danh sách trường phù hợp để hiển thị lần đầu
                    filtered_schools = tim_truong_phu_hop(tohop_diem)

            except (ValueError, TypeError):
                error = "Số báo danh không hợp lệ. Vui lòng nhập số."
                result = None
        
        elif action == 'filter':
            # Lấy lại điểm của sinh viên từ session
            result = session.get('result', None)
            
            if result:
                # TÍNH TOÁN LẠI danh sách trường phù hợp từ đầu
                all_suitable = tim_truong_phu_hop(result['tohop_diem'])

                filter_truong = request.form.get('filter_truong', '').strip()
                filter_nganh = request.form.get('filter_nganh', '').strip()

                # Lưu lại lựa chọn để hiển thị trên form
                selected_school = filter_truong
                selected_major = filter_nganh

                # Áp dụng bộ lọc trên danh sách vừa tính toán
                filtered_schools = all_suitable
                if filter_truong:
                    filtered_schools = [s for s in filtered_schools if filter_truong.lower() in s['truong'].lower()]
                if filter_nganh:
                    filtered_schools = [s for s in filtered_schools if filter_nganh.lower() in s['nganh'].lower()]
            else:
                error = "Phiên làm việc đã hết hạn. Vui lòng tra cứu lại SBD."

    return render_template('index.html', result=result, error=error, 
                           filtered_schools=filtered_schools,
                           schools_list=schools_list, majors_list=majors_list,
                           selected_school=selected_school, selected_major=selected_major)

# Các route API để cập nhật datalist không thay đổi
@app.route('/get_majors')
def get_majors():
    school = request.args.get('school', '')
    if school:
        majors = df_diem_chuan[df_diem_chuan['Trường đào tạo'] == school]['Tên ngành'].dropna().unique().tolist()
    else:
        majors = df_diem_chuan['Tên ngành'].dropna().unique().tolist()
    return jsonify(sorted(majors))

@app.route('/get_schools')
def get_schools():
    major = request.args.get('major', '')
    if major:
        schools = df_diem_chuan[df_diem_chuan['Tên ngành'] == major]['Trường đào tạo'].dropna().unique().tolist()
    else:
        schools = df_diem_chuan['Trường đào tạo'].dropna().unique().tolist()
    return jsonify(sorted(schools))


if __name__ == '__main__':
    app.run( host='0.0.0.0', port=10000)