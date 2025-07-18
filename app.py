
# from flask import Flask, render_template, request, jsonify, session
# import pandas as pd

# app = Flask(__name__)
# app.secret_key = '210505'  # Cần để sử dụng session, tạo một key ngẫu nhiên

# # Đường dẫn file CSV
# DATA_FILE1 = 'data/diemthi1.csv'
# DATA_FILE2 = 'data/diemthi2.csv'
# DIEM_CHUAN_FILE = 'data/diemchuan.csv'

# # Đọc dữ liệu từ các file CSV
# try:
#     df1 = pd.read_csv(DATA_FILE1, encoding='utf-8')
#     df2 = pd.read_csv(DATA_FILE2, encoding='utf-8')
#     df_diem_chuan = pd.read_csv(DIEM_CHUAN_FILE, encoding='utf-8')
#     # Gộp hai DataFrame điểm thi lại thành một
#     df = pd.concat([df1, df2], ignore_index=True)
# except FileNotFoundError as e:
#     print(f"Lỗi: không tìm thấy file {e.filename}. Vui lòng kiểm tra lại đường dẫn.")
#     exit()

# # Tạo bảng ánh xạ tổ hợp -> các môn tương ứng
# to_hop_map = {
#     'A00': ['Toán', 'Lí', 'Hóa'], 'A01': ['Toán', 'Lí', 'Ngoại ngữ'],
#     'B00': ['Toán', 'Hóa', 'Sinh'], 'C00': ['Văn', 'Sử', 'Địa'],
#     'D01': ['Văn', 'Toán', 'Ngoại ngữ'], 'D07': ['Toán', 'Hóa', 'Ngoại ngữ'],
#     'D08': ['Toán', 'Sinh', 'Ngoại ngữ'], 'D09': ['Toán', 'Sử', 'Ngoại ngữ'],
#     'D10': ['Toán', 'Địa', 'Ngoại ngữ'], 'D14': ['Văn', 'Sử', 'Ngoại ngữ'],
#     'D15': ['Văn', 'Địa', 'Ngoại ngữ'],
#     'D66': ['Văn', 'Giáo dục kinh tế và pháp luật', 'Ngoại ngữ'],
#     'T00': ['Toán', 'Sinh', 'Năng khiếu TDTT'], 'H01': ['Toán', 'Văn', 'Vẽ Mỹ thuật'],
#     'M00': ['Văn', 'Toán', 'Hát'], 'N00': ['Văn', 'Năng khiếu Âm nhạc 1', 'Năng khiếu Âm nhạc 2']
# }

# # Ánh xạ mã tỉnh với tên tỉnh
# ma_tinh_map = {
#     '01': 'Hà Nội', '02': 'TP. Hồ Chí Minh', '03': 'Hải Phòng', '04': 'Đà Nẵng', '05': 'Hà Giang',
#     '06': 'Cao Bằng', '07': 'Lai Châu', '08': 'Lào Cai', '09': 'Tuyên Quang', '10': 'Lạng Sơn',
#     '11': 'Bắc Kạn', '12': 'Thái Nguyên', '13': 'Yên Bái', '14': 'Sơn La', '15': 'Phú Thọ',
#     '16': 'Vĩnh Phúc', '17': 'Quảng Ninh', '18': 'Bắc Giang', '19': 'Bắc Ninh', '21': 'Hải Dương',
#     '22': 'Hưng Yên', '23': 'Hòa Bình', '24': 'Hà Nam', '25': 'Nam Định', '26': 'Thái Bình',
#     '27': 'Ninh Bình', '28': 'Thanh Hóa', '29': 'Nghệ An', '30': 'Hà Tĩnh', '31': 'Quảng Bình',
#     '32': 'Quảng Trị', '33': 'Thừa Thiên Huế', '34': 'Quảng Nam', '35': 'Quảng Ngãi', '36': 'Kon Tum',
#     '37': 'Bình Định', '38': 'Gia Lai', '39': 'Phú Yên', '40': 'Đắk Lắk', '41': 'Khánh Hòa',
#     '42': 'Lâm Đồng', '43': 'Bình Phước', '44': 'Bình Dương', '45': 'Ninh Thuận', '46': 'Tây Ninh',
#     '47': 'Bình Thuận', '48': 'Đồng Nai', '49': 'Long An', '50': 'Đồng Tháp', '51': 'An Giang',
#     '52': 'Bà Rịa - Vũng Tàu', '53': 'Tiền Giang', '54': 'Kiên Giang', '55': 'Cần Thơ', '56': 'Bến Tre',
#     '57': 'Vĩnh Long', '58': 'Trà Vinh', '59': 'Sóc Trăng', '60': 'Bạc Liêu', '61': 'Cà Mau',
#     '62': 'Điện Biên', '63': 'Đăk Nông', '64': 'Hậu Giang'
# }

# def tinh_diem_tohop(row_dict):
#     tohop_diem = {}
#     for toh, mons in to_hop_map.items():
#         # Kiểm tra xem tất cả các môn trong tổ hợp có trong điểm của thí sinh không
#         valid_mons = [m for m in mons if m in row_dict and pd.notna(row_dict[m])]
#         if len(valid_mons) == len(mons):
#             tohop_diem[toh] = round(sum(row_dict[m] for m in mons), 2)
#     return tohop_diem

# def tim_truong_phu_hop(tohop_diem):
#     suitable_schools = []
#     for _, row in df_diem_chuan.iterrows():
#         to_hop_list = str(row.get('Tổ hợp môn', '')).split('; ')
#         diem_chuan = row.get('Điểm chuẩn 2024')
#         truong = row.get('Trường đào tạo')
#         nganh = row.get('Tên ngành')

#         # Bỏ qua nếu thiếu thông tin quan trọng
#         if not all([to_hop_list, isinstance(diem_chuan, (int, float)), truong, nganh]):
#             continue

#         for toh, diem in tohop_diem.items():
#             if toh in to_hop_list and diem >= diem_chuan:
#                 suitable_schools.append({
#                     'truong': truong, 'nganh': nganh, 'toh': toh,
#                     'diem_chuan': diem_chuan, 'diem': diem
#                 })
#     # Sắp xếp mặc định theo điểm chuẩn giảm dần
#     return sorted(suitable_schools, key=lambda x: x['diem_chuan'], reverse=True)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     # Lấy dữ liệu từ session nếu có
#     result = session.get('result', None)
#     error = None
    
#     # Các biến này sẽ được xác định trong khối POST
#     filtered_schools = None
#     selected_school = ''
#     selected_major = ''

#     # Luôn lấy danh sách đầy đủ cho datalist
#     schools_list = sorted(df_diem_chuan['Trường đào tạo'].dropna().unique().tolist())
#     majors_list = sorted(df_diem_chuan['Tên ngành'].dropna().unique().tolist())

#     if request.method == 'POST':
#         action = request.form.get('action')

#         if action == 'lookup':
#             session.clear()
#             sbd = request.form.get('sbd')
            
#             try:
#                 row = df[df['SOBAODANH'] == int(sbd)]
#                 if row.empty:
#                     error = f"Không tìm thấy SBD {sbd}"
#                     result = None
#                 else:
#                     row_data = row.iloc[0].to_dict()
#                     diem_mon = {mon: diem for mon, diem in row_data.items()
#                                 if isinstance(diem, (int, float)) and pd.notna(diem) and mon != 'SOBAODANH'}
#                     tohop_diem = tinh_diem_tohop(diem_mon)
#                     ma_tinh = str(sbd)[:2]
                    
#                     # CHỈ LƯU KẾT QUẢ ĐIỂM VÀO SESSION (nhỏ gọn)
#                     result = {
#                         'sbd': sbd,
#                         'ten_tinh': ma_tinh_map.get(ma_tinh, 'Không xác định'),
#                         'diem': diem_mon,
#                         'tohop_diem': tohop_diem
#                     }
#                     session['result'] = result
                    
#                     # Tính toán danh sách trường phù hợp để hiển thị lần đầu
#                     filtered_schools = tim_truong_phu_hop(tohop_diem)

#             except (ValueError, TypeError):
#                 error = "Số báo danh không hợp lệ. Vui lòng nhập số."
#                 result = None
        
#         elif action == 'filter':
#             # Lấy lại điểm của sinh viên từ session
#             result = session.get('result', None)
            
#             if result:
#                 # TÍNH TOÁN LẠI danh sách trường phù hợp từ đầu
#                 all_suitable = tim_truong_phu_hop(result['tohop_diem'])

#                 filter_truong = request.form.get('filter_truong', '').strip()
#                 filter_nganh = request.form.get('filter_nganh', '').strip()

#                 # Lưu lại lựa chọn để hiển thị trên form
#                 selected_school = filter_truong
#                 selected_major = filter_nganh

#                 # Áp dụng bộ lọc trên danh sách vừa tính toán
#                 filtered_schools = all_suitable
#                 if filter_truong:
#                     filtered_schools = [s for s in filtered_schools if filter_truong.lower() in s['truong'].lower()]
#                 if filter_nganh:
#                     filtered_schools = [s for s in filtered_schools if filter_nganh.lower() in s['nganh'].lower()]
#             else:
#                 error = "Phiên làm việc đã hết hạn. Vui lòng tra cứu lại SBD."

#     return render_template('index.html', result=result, error=error, 
#                            filtered_schools=filtered_schools,
#                            schools_list=schools_list, majors_list=majors_list,
#                            selected_school=selected_school, selected_major=selected_major)

# # Các route API để cập nhật datalist không thay đổi
# @app.route('/get_majors')
# def get_majors():
#     school = request.args.get('school', '')
#     if school:
#         majors = df_diem_chuan[df_diem_chuan['Trường đào tạo'] == school]['Tên ngành'].dropna().unique().tolist()
#     else:
#         majors = df_diem_chuan['Tên ngành'].dropna().unique().tolist()
#     return jsonify(sorted(majors))

# @app.route('/get_schools')
# def get_schools():
#     major = request.args.get('major', '')
#     if major:
#         schools = df_diem_chuan[df_diem_chuan['Tên ngành'] == major]['Trường đào tạo'].dropna().unique().tolist()
#     else:
#         schools = df_diem_chuan['Trường đào tạo'].dropna().unique().tolist()
#     return jsonify(sorted(schools))


# if __name__ == '__main__':
#     app.run( host='0.0.0.0', port=10000)

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

# === SỬA LỖI: NGĂN TRÌNH DUYỆT LƯU BỘ NHỚ ĐỆM (CACHE) ===
@app.after_request
def add_no_cache_headers(response):
    """
    Thêm các header vào mỗi response để yêu cầu trình duyệt
    không cache trang, đảm bảo dữ liệu luôn mới nhất khi F5.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Tạo bảng ánh xạ tổ hợp -> các môn tương ứng
to_hop_map = {
    'A00': ['Toán', 'Lí', 'Hóa'], 'A01': ['Toán', 'Lí', 'Ngoại ngữ'], 'A02': ['Toán', 'Lí', 'Sinh'],
    'A03': ['Toán', 'Lí', 'Sử'], 'A04': ['Toán', 'Lí', 'Địa'], 'A05': ['Toán', 'Hóa', 'Sử'],
    'A06': ['Toán', 'Hóa', 'Địa'], 'A07': ['Toán', 'Sử', 'Địa'], 'A08': ['Toán', 'Sử', 'GDCD'],
    'A09': ['Toán', 'Địa', 'GDCD'], 'A10': ['Toán', 'Lí', 'GDCD'], 'A11': ['Toán', 'Hóa', 'GDCD'],

    'B00': ['Toán', 'Hóa', 'Sinh'], 'B02': ['Toán', 'Sinh', 'Địa'], 'B03': ['Toán', 'Sinh', 'Văn'],
    'B04': ['Toán', 'Sinh', 'GDCD'], 'B08': ['Toán', 'Sinh', 'Ngoại ngữ'],

    'C00': ['Văn', 'Sử', 'Địa'], 'C01': ['Văn', 'Toán', 'Lí'], 'C02': ['Văn', 'Toán', 'Hóa'],
    'C03': ['Văn', 'Toán', 'Sử'], 'C04': ['Văn', 'Toán', 'Địa'], 'C05': ['Văn', 'Lí', 'Hóa'],
    'C08': ['Văn', 'Hóa', 'Sinh'], 'C12': ['Văn', 'Sử', 'Sinh'], 'C13': ['Văn', 'Sinh', 'Địa'],
    'C14': ['Văn', 'Toán', 'GDCD'], 'C17': ['Văn', 'Hóa', 'GDCD'], 'C19': ['Văn', 'Sử', 'GDCD'],
    'C20': ['Văn', 'Địa', 'GDCD'],

    'D01': ['Văn', 'Toán', 'Ngoại ngữ'], 'D02': ['Văn', 'Toán', 'Tiếng Nga'], 'D03': ['Văn', 'Toán', 'Tiếng Pháp'],
    'D04': ['Văn', 'Toán', 'Tiếng Trung'], 'D05': ['Văn', 'Toán', 'Tiếng Đức'], 'D06': ['Văn', 'Toán', 'Tiếng Nhật'],
    'D07': ['Toán', 'Hóa', 'Ngoại ngữ'], 'D08': ['Toán', 'Sinh', 'Ngoại ngữ'], 'D09': ['Toán', 'Sử', 'Ngoại ngữ'],
    'D10': ['Toán', 'Địa', 'Ngoại ngữ'], 'D11': ['Văn', 'Lí', 'Ngoại ngữ'], 'D12': ['Văn', 'Hóa', 'Ngoại ngữ'],
    'D13': ['Văn', 'Sinh', 'Ngoại ngữ'], 'D14': ['Văn', 'Sử', 'Ngoại ngữ'], 'D15': ['Văn', 'Địa', 'Ngoại ngữ'],
    'D66': ['Văn', 'Giáo dục kinh tế và pháp luật', 'Ngoại ngữ'], 'D84': ['Toán', 'GDCD', 'Ngoại ngữ'],

    'H01': ['Toán', 'Văn', 'Vẽ Mỹ thuật'], 'H02': ['Toán', 'Vẽ HHMT', 'Vẽ trang trí màu'],
    'H04': ['Toán', 'Ngoại ngữ', 'Vẽ Năng khiếu'], 'H06': ['Văn', 'Ngoại ngữ', 'Vẽ Mỹ thuật'],
    'H07': ['Toán', 'Hình họa', 'Trang trí'], 'H08': ['Văn', 'Sử', 'Vẽ Mỹ thuật'],

    'M00': ['Văn', 'Toán', 'Hát'], 'M01': ['Văn', 'Sử', 'Năng khiếu'],
    'M02': ['Toán', 'Năng khiếu 1', 'Năng khiếu 2'], 'M03': ['Văn', 'Năng khiếu 1', 'Năng khiếu 2'],
    'M09': ['Toán', 'NK Mầm non 1', 'NK Mầm non 2'],

    'N00': ['Văn', 'Năng khiếu Âm nhạc 1', 'Năng khiếu Âm nhạc 2'],
    'N01': ['Văn', 'Xướng âm', 'Biểu diễn'], 'N02': ['Văn', 'Ký xướng âm', 'Hát hoặc nhạc cụ'],

    'T00': ['Toán', 'Sinh', 'Năng khiếu TDTT'], 'T01': ['Toán', 'Văn', 'Năng khiếu TDTT'],
    'T02': ['Văn', 'Sinh', 'Năng khiếu TDTT'], 'T05': ['Văn', 'GDCD', 'Năng khiếu TDTT'],

    'V00': ['Toán', 'Lí', 'Vẽ HHMT'], 'V01': ['Toán', 'Văn', 'Vẽ Mỹ thuật'], 'V02': ['Toán', 'Ngoại ngữ', 'Vẽ Mỹ thuật'],

    'K00': ['Toán', 'Đọc hiểu', 'Tư duy Khoa học'], 'S00': ['Văn', 'NK Sân khấu 1', 'NK Sân khấu 2'],

    'TA_Tin': ['Toán', 'Ngoại ngữ', 'Tin'], 'TV_Tin': ['Toán', 'Văn', 'Tin'], 'TL_Tin': ['Toán', 'Lí', 'Tin'],
    'TL_CN': ['Toán', 'Lí', 'Công nghệ'], 'TH_CN': ['Toán', 'Hóa', 'Công nghệ'], 'TA_CN': ['Toán', 'Ngoại ngữ', 'Công nghệ']
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

        if not all([to_hop_list, isinstance(diem_chuan, (int, float)), truong, nganh]):
            continue

        for toh, diem in tohop_diem.items():
            if toh in to_hop_list and diem >= diem_chuan:
                suitable_schools.append({
                    'truong': truong, 'nganh': nganh, 'toh': toh,
                    'diem_chuan': diem_chuan, 'diem': diem
                })
    return sorted(suitable_schools, key=lambda x: x['diem_chuan'], reverse=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        session.clear()

    result = session.get('result', None)
    error = None
    
    filtered_schools = None
    selected_school = ''
    selected_major = ''

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
                    
                    result = {
                        'sbd': sbd,
                        'ten_tinh': ma_tinh_map.get(ma_tinh, 'Không xác định'),
                        'diem': diem_mon,
                        'tohop_diem': tohop_diem
                    }
                    session['result'] = result
                    
                    filtered_schools = tim_truong_phu_hop(tohop_diem)

            except (ValueError, TypeError):
                error = "Số báo danh không hợp lệ. Vui lòng nhập số."
                result = None
        
        elif action == 'filter':
            result = session.get('result', None)
            
            if result:
                all_suitable = tim_truong_phu_hop(result['tohop_diem'])
                filter_truong = request.form.get('filter_truong', '').strip()
                filter_nganh = request.form.get('filter_nganh', '').strip()

                selected_school = filter_truong
                selected_major = filter_nganh

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
    app.run(host='0.0.0.0', port=10000)
