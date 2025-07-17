from flask import Flask, render_template, request, session
import pandas as pd

app = Flask(__name__)
app.secret_key = '210505'  # Cần để sử dụng session, tạo một key ngẫu nhiên

import pandas as pd

# Đường dẫn file CSV
DATA_FILE1 = 'data/diemthi1.csv'
DATA_FILE2 = 'data/diemthi2.csv'

# Đọc hai file CSV
df1 = pd.read_csv(DATA_FILE1, encoding='utf-8')
df2 = pd.read_csv(DATA_FILE2, encoding='utf-8')

# Gộp hai DataFrame lại thành một
df = pd.concat([df1, df2], ignore_index=True)
# Tạo bảng ánh xạ tổ hợp -> các môn tương ứng
to_hop_map = {
    'A00': ['Toán', 'Lí', 'Hóa'],
    'A01': ['Toán', 'Lí', 'Ngoại ngữ'],
    'B00': ['Toán', 'Hóa', 'Sinh'],
    'C00': ['Văn', 'Sử', 'Địa'],
    'D01': ['Văn', 'Toán', 'Ngoại ngữ'],
    'D07': ['Toán', 'Hóa', 'Ngoại ngữ'],
    'D08': ['Toán', 'Sinh', 'Ngoại ngữ'],
    'D09': ['Toán', 'Sử', 'Ngoại ngữ'],
    'D10': ['Toán', 'Địa', 'Ngoại ngữ'],
    'D14': ['Văn', 'Sử', 'Ngoại ngữ'],
    'D15': ['Văn', 'Địa', 'Ngoại ngữ'],
    'D66': ['Văn', 'Giáo dục kinh tế và pháp luật', 'Ngoại ngữ'],
    'T00': ['Toán', 'Sinh', 'Năng khiếu TDTT'],
    'H01': ['Toán', 'Văn', 'Vẽ Mỹ thuật'],
    'M00': ['Văn', 'Toán', 'Hát'],
    'N00': ['Văn', 'Năng khiếu Âm nhạc 1', 'Năng khiếu Âm nhạc 2']
}

# Ánh xạ mã tỉnh với tên tỉnh
ma_tinh_map = {
    '01': 'Hà Nội',
    '03': 'Hải Phòng',
    '05': 'Hà Giang',
    '06': 'Cao Bằng',
    '07': 'Lai Châu',
    '08': 'Lào Cai',
    '09': 'Tuyên Quang',
    '10': 'Lạng Sơn',
    '11': 'Bắc Kạn',
    '12': 'Thái Nguyên',
    '13': 'Yên Bái',
    '14': 'Sơn La',
    '15': 'Phú Thọ',
    '16': 'Vĩnh Phúc',
    '17': 'Quảng Ninh',
    '18': 'Bắc Giang',
    '19': 'Bắc Ninh',
    '21': 'Hải Dương',
    '22': 'Hưng Yên',
    '23': 'Hòa Bình',
    '24': 'Hà Nam',
    '25': 'Nam Định',
    '26': 'Thái Bình',
    '27': 'Ninh Bình',
    '62': 'Điện Biên',
    '28': 'Thanh Hóa',
    '29': 'Nghệ An',
    '30': 'Hà Tĩnh',
    '31': 'Quảng Bình',
    '32': 'Quảng Trị',
    '33': 'Thừa Thiên Huế',
    '04': 'Đà Nẵng',
    '34': 'Quảng Nam',
    '35': 'Quảng Ngãi',
    '37': 'Bình Định',
    '39': 'Phú Yên',
    '41': 'Khánh Hòa',
    '45': 'Ninh Thuận',
    '47': 'Bình Thuận',
    '40': 'Đắk Lắk',
    '63': 'Đăk Nông',
    '38': 'Gia Lai',
    '36': 'Kon Tum',
    '42': 'Lâm Đồng',
    '02': 'TP. Hồ Chí Minh',
    '43': 'Bình Phước',
    '44': 'Bình Dương',
    '48': 'Đồng Nai',
    '46': 'Tây Ninh',
    '49': 'Long An',
    '50': 'Đồng Tháp',
    '51': 'An Giang',
    '52': 'Bà Rịa - Vũng Tàu',
    '53': 'Tiền Giang',
    '54': 'Kiên Giang',
    '55': 'Cần Thơ',
    '56': 'Bến Tre',
    '57': 'Vĩnh Long',
    '58': 'Trà Vinh',
    '59': 'Sóc Trăng',
    '60': 'Bạc Liêu',
    '61': 'Cà Mau',
    '64': 'Hậu Giang'
}

def tinh_diem_tohop(row_dict):
    tohop_diem = {}
    for toh, mons in to_hop_map.items():
        if all(m in row_dict and pd.notna(row_dict[m]) for m in mons):
            tohop_diem[toh] = round(sum(row_dict[m] for m in mons), 2)
    return tohop_diem

@app.route('/', methods=['GET', 'POST'])
def index():
    # Xóa session nếu có
    session.pop('result', None)
    session.pop('error', None)
    
    result = None
    error = None

    if request.method == 'POST':
        sbd = request.form.get('sbd')

        try:
            sbd_int = int(sbd)
            row = df[df['SOBAODANH'] == sbd_int]

            if row.empty:
                error = f"Không tìm thấy SBD {sbd}"
            else:
                row_data = row.iloc[0].to_dict()

                # Chỉ lấy các môn có điểm > 0 hoặc khác NaN
                diem_mon = {mon: diem for mon, diem in row_data.items() if isinstance(diem, (int, float)) and pd.notna(diem) and mon not in ['SOBAODANH']}

                # Tính điểm các tổ hợp
                tohop_diem = tinh_diem_tohop(diem_mon)

                # Lấy mã tỉnh từ 2 chữ số đầu của SBD
                ma_tinh = str(sbd)[:2]
                ten_tinh = ma_tinh_map.get(ma_tinh, 'Không xác định')

                result = {
                    'sbd': sbd,
                    'ten_tinh': ten_tinh,
                    'diem': diem_mon,
                    'tohop_diem': tohop_diem
                }

        except ValueError:
            error = "Số báo danh không hợp lệ. Vui lòng nhập số."

    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)