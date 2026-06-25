# vay_online_app.py
import json
import os
from datetime import datetime, timedelta
import hashlib
import getpass

class NguoiDung:
    def __init__(self, ten_dang_nhap, mat_khau, ho_ten, so_dien_thoai):
        self.ten_dang_nhap = ten_dang_nhap
        self.mat_khau = self.ma_hoa_mat_khau(mat_khau)
        self.ho_ten = ho_ten
        self.so_dien_thoai = so_dien_thoai
        self.so_du = 0
        self.khoan_vay = []
    
    def ma_hoa_mat_khau(self, mat_khau):
        return hashlib.sha256(mat_khau.encode()).hexdigest()
    
    def kiem_tra_mat_khau(self, mat_khau):
        return self.mat_khau == self.ma_hoa_mat_khau(mat_khau)
    
    def to_dict(self):
        return {
            'ten_dang_nhap': self.ten_dang_nhap,
            'mat_khau': self.mat_khau,
            'ho_ten': self.ho_ten,
            'so_dien_thoai': self.so_dien_thoai,
            'so_du': self.so_du,
            'khoan_vay': self.khoan_vay
        }

class KhoanVay:
    def __init__(self, so_tien, lai_suat, ky_han, ngay_vay=None):
        self.so_tien = so_tien
        self.lai_suat = lai_suat
        self.ky_han = ky_han  # số tháng
        self.ngay_vay = ngay_vay if ngay_vay else datetime.now()
        self.trang_thai = 'Dang_vay'
        self.ngay_han_tra = self.ngay_vay + timedelta(days=ky_han*30)
        self.so_tien_con_lai = so_tien
    
    def tinh_lai(self):
        return self.so_tien * (self.lai_suat / 100) * (self.ky_han / 12)
    
    def tinh_tong_phai_tra(self):
        return self.so_tien + self.tinh_lai()
    
    def to_dict(self):
        return {
            'so_tien': self.so_tien,
            'lai_suat': self.lai_suat,
            'ky_han': self.ky_han,
            'ngay_vay': self.ngay_vay.strftime('%Y-%m-%d %H:%M:%S'),
            'trang_thai': self.trang_thai,
            'ngay_han_tra': self.ngay_han_tra.strftime('%Y-%m-%d'),
            'so_tien_con_lai': self.so_tien_con_lai
        }

class HeThongVayOnline:
    def __init__(self):
        self.nguoi_dung_hien_tai = None
        self.nguoi_dung_dict = {}
        self.lai_suat_mac_dinh = 12  # 12%/năm
        self.ky_han_toi_da = 36  # 36 tháng
        self.so_tien_toi_da = 100000000  # 100 triệu
        self.duong_dan_du_lieu = 'du_lieu_vay.json'
        self.tai_du_lieu()
    
    def tai_du_lieu(self):
        if os.path.exists(self.duong_dan_du_lieu):
            try:
                with open(self.duong_dan_du_lieu, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for username, user_data in data.items():
                        user = NguoiDung(
                            user_data['ten_dang_nhap'],
                            user_data['mat_khau'],
                            user_data['ho_ten'],
                            user_data['so_dien_thoai']
                        )
                        user.so_du = user_data['so_du']
                        # Khôi phục các khoản vay
                        for loan_data in user_data.get('khoan_vay', []):
                            ngay_vay = datetime.strptime(loan_data['ngay_vay'], '%Y-%m-%d %H:%M:%S')
                            loan = KhoanVay(
                                loan_data['so_tien'],
                                loan_data['lai_suat'],
                                loan_data['ky_han'],
                                ngay_vay
                            )
                            loan.trang_thai = loan_data['trang_thai']
                            loan.so_tien_con_lai = loan_data['so_tien_con_lai']
                            user.khoan_vay.append(loan)
                        self.nguoi_dung_dict[username] = user
            except Exception as e:
                print(f"Lỗi khi tải dữ liệu: {e}")
    
    def luu_du_lieu(self):
        try:
            data = {}
            for username, user in self.nguoi_dung_dict.items():
                user_dict = user.to_dict()
                user_dict['khoan_vay'] = [loan.to_dict() for loan in user.khoan_vay]
                data[username] = user_dict
            
            with open(self.duong_dan_du_lieu, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu: {e}")
    
    def dang_ky(self):
        print("\n" + "="*50)
        print("ĐĂNG KÝ TÀI KHOẢN")
        print("="*50)
        
        ten_dang_nhap = input("Tên đăng nhập: ").strip()
        if ten_dang_nhap in self.nguoi_dung_dict:
            print("Tên đăng nhập đã tồn tại!")
            return False
        
        mat_khau = getpass.getpass("Mật khẩu: ")
        xac_nhan_mat_khau = getpass.getpass("Xác nhận mật khẩu: ")
        
        if mat_khau != xac_nhan_mat_khau:
            print("Mật khẩu không khớp!")
            return False
        
        ho_ten = input("Họ và tên: ").strip()
        so_dien_thoai = input("Số điện thoại: ").strip()
        
        user = NguoiDung(ten_dang_nhap, mat_khau, ho_ten, so_dien_thoai)
        self.nguoi_dung_dict[ten_dang_nhap] = user
        self.luu_du_lieu()
        
        print("\n✅ Đăng ký thành công!")
        return True
    
    def dang_nhap(self):
        print("\n" + "="*50)
        print("ĐĂNG NHẬP")
        print("="*50)
        
        ten_dang_nhap = input("Tên đăng nhập: ").strip()
        mat_khau = getpass.getpass("Mật khẩu: ")
        
        if ten_dang_nhap in self.nguoi_dung_dict:
            user = self.nguoi_dung_dict[ten_dang_nhap]
            if user.kiem_tra_mat_khau(mat_khau):
                self.nguoi_dung_hien_tai = user
                print(f"\n✅ Chào mừng, {user.ho_ten}!")
                return True
        print("❌ Tên đăng nhập hoặc mật khẩu không đúng!")
        return False
    
    def dang_xuat(self):
        self.nguoi_dung_hien_tai = None
        print("Đã đăng xuất thành công!")
    
    def hien_thi_thong_tin(self):
        user = self.nguoi_dung_hien_tai
        print("\n" + "="*50)
        print("THÔNG TIN CÁ NHÂN")
        print("="*50)
        print(f"Họ tên: {user.ho_ten}")
        print(f"Số điện thoại: {user.so_dien_thoai}")
        print(f"Số dư: {user.so_du:,.0f} VND")
        print("-"*50)
    
    def tao_khoan_vay(self):
        user = self.nguoi_dung_hien_tai
        
        print("\n" + "="*50)
        print("TẠO KHOẢN VAY")
        print("="*50)
        
        try:
            so_tien = float(input(f"Số tiền muốn vay (tối đa {self.so_tien_toi_da:,.0f} VND): "))
            if so_tien <= 0:
                print("❌ Số tiền phải lớn hơn 0!")
                return
            if so_tien > self.so_tien_toi_da:
                print(f"❌ Số tiền vượt quá hạn mức tối đa ({self.so_tien_toi_da:,.0f} VND)!")
                return
            
            ky_han = int(input(f"Kỳ hạn vay (tháng, tối đa {self.ky_han_toi_da} tháng): "))
            if ky_han <= 0 or ky_han > self.ky_han_toi_da:
                print(f"❌ Kỳ hạn không hợp lệ! Vui lòng nhập từ 1 đến {self.ky_han_toi_da} tháng")
                return
            
            print(f"\nLãi suất mặc định: {self.lai_suat_mac_dinh}%/năm")
            dieu_chinh_lai = input("Bạn có muốn điều chỉnh lãi suất? (y/n): ").lower()
            
            if dieu_chinh_lai == 'y':
                lai_suat = float(input("Nhập lãi suất mong muốn (%/năm): "))
                if lai_suat < 0:
                    print("❌ Lãi suất không được âm!")
                    return
            else:
                lai_suat = self.lai_suat_mac_dinh
            
            # Tạo khoản vay
            khoan_vay = KhoanVay(so_tien, lai_suat, ky_han)
            
            # Xác nhận thông tin
            print("\n" + "-"*50)
            print("THÔNG TIN KHOẢN VAY:")
            print(f"Số tiền: {so_tien:,.0f} VND")
            print(f"Lãi suất: {lai_suat}%/năm")
            print(f"Kỳ hạn: {ky_han} tháng")
            print(f"Ngày vay: {khoan_vay.ngay_vay.strftime('%d/%m/%Y')}")
            print(f"Ngày đến hạn: {khoan_vay.ngay_han_tra.strftime('%d/%m/%Y')}")
            print(f"Tiền lãi: {khoan_vay.tinh_lai():,.0f} VND")
            print(f"Tổng phải trả: {khoan_vay.tinh_tong_phai_tra():,.0f} VND")
            print("-"*50)
            
            xac_nhan = input("\nXác nhận vay? (y/n): ").lower()
            if xac_nhan == 'y':
                user.khoan_vay.append(khoan_vay)
                user.so_du += so_tien
                self.luu_du_lieu()
                print("\n✅ Vay thành công! Tiền đã được chuyển vào tài khoản.")
                print(f"Số dư hiện tại: {user.so_du:,.0f} VND")
            else:
                print("Đã hủy giao dịch vay.")
                
        except ValueError:
            print("❌ Vui lòng nhập số hợp lệ!")
    
    def tra_no(self):
        user = self.nguoi_dung_hien_tai
        
        # Lọc các khoản vay đang còn nợ
        khoan_vay_dang_no = [v for v in user.khoan_vay if v.trang_thai == 'Dang_vay']
        
        if not khoan_vay_dang_no:
            print("\n❌ Bạn không có khoản vay nào đang cần trả!")
            return
        
        print("\n" + "="*50)
        print("DANH SÁCH KHOẢN VAY ĐANG NỢ")
        print("="*50)
        
        for i, vay in enumerate(khoan_vay_dang_no, 1):
            tong_phai_tra = vay.tinh_tong_phai_tra()
            print(f"{i}. Số tiền: {vay.so_tien:,.0f} VND")
            print(f"   Lãi suất: {vay.lai_suat}%/năm")
            print(f"   Kỳ hạn: {vay.ky_han} tháng")
            print(f"   Ngày đến hạn: {vay.ngay_han_tra.strftime('%d/%m/%Y')}")
            print(f"   Tổng phải trả: {tong_phai_tra:,.0f} VND")
            print("-"*40)
        
        try:
            lua_chon = int(input("\nChọn khoản vay cần trả (nhập số thứ tự): "))
            if lua_chon < 1 or lua_chon > len(khoan_vay_dang_no):
                print("❌ Lựa chọn không hợp lệ!")
                return
            
            khoan_vay_chon = khoan_vay_dang_no[lua_chon - 1]
            tong_phai_tra = khoan_vay_chon.tinh_tong_phai_tra()
            
            print(f"\nSố tiền phải trả: {tong_phai_tra:,.0f} VND")
            print(f"Số dư hiện tại: {user.so_du:,.0f} VND")
            
            if user.so_du < tong_phai_tra:
                print(f"❌ Số dư không đủ! Cần thêm {tong_phai_tra - user.so_du:,.0f} VND")
                return
            
            xac_nhan = input("\nXác nhận thanh toán? (y/n): ").lower()
            if xac_nhan == 'y':
                user.so_du -= tong_phai_tra
                khoan_vay_chon.trang_thai = 'Da_tra'
                khoan_vay_chon.so_tien_con_lai = 0
                self.luu_du_lieu()
                print("\n✅ Thanh toán thành công!")
                print(f"Số dư còn lại: {user.so_du:,.0f} VND")
            else:
                print("Đã hủy thanh toán.")
                
        except ValueError:
            print("❌ Vui lòng nhập số hợp lệ!")
    
    def xem_lich_su_vay(self):
        user = self.nguoi_dung_hien_tai
        
        if not user.khoan_vay:
            print("\n❌ Bạn chưa có khoản vay nào!")
            return
        
        print("\n" + "="*50)
        print("LỊCH SỬ VAY")
        print("="*50)
        
        for i, vay in enumerate(user.khoan_vay, 1):
            trang_thai_str = "🟢 Đang vay" if vay.trang_thai == 'Dang_vay' else "✅ Đã trả"
            print(f"{i}. Số tiền: {vay.so_tien:,.0f} VND")
            print(f"   Trạng thái: {trang_thai_str}")
            print(f"   Ngày vay: {vay.ngay_vay.strftime('%d/%m/%Y')}")
            print(f"   Ngày đến hạn: {vay.ngay_han_tra.strftime('%d/%m/%Y')}")
            print(f"   Lãi suất: {vay.lai_suat}%/năm")
            print(f"   Số tiền còn lại: {vay.so_tien_con_lai:,.0f} VND")
            print("-"*40)
    
    def menu_chinh(self):
        while True:
            print("\n" + "="*50)
            print("🏦 HỆ THỐNG VAY ONLINE")
            print("="*50)
            print("1. Đăng nhập")
            print("2. Đăng ký")
            print("3. Thoát")
            print("="*50)
            
            lua_chon = input("Chọn chức năng: ")
            
            if lua_chon == '1':
                if self.dang_nhap():
                    self.menu_nguoi_dung()
            elif lua_chon == '2':
                self.dang_ky()
            elif lua_chon == '3':
                self.luu_du_lieu()
                print("Cảm ơn bạn đã sử dụng hệ thống!")
                break
            else:
                print("❌ Lựa chọn không hợp lệ!")
    
    def menu_nguoi_dung(self):
        while True:
            print("\n" + "="*50)
            print(f"👤 {self.nguoi_dung_hien_tai.ho_ten} - MENU")
            print("="*50)
            print("1. Xem thông tin cá nhân")
            print("2. Vay tiền")
            print("3. Trả nợ")
            print("4. Xem lịch sử vay")
            print("5. Đăng xuất")
            print("="*50)
            
            lua_chon = input("Chọn chức năng: ")
            
            if lua_chon == '1':
                self.hien_thi_thong_tin()
            elif lua_chon == '2':
                self.tao_khoan_vay()
            elif lua_chon == '3':
                self.tra_no()
            elif lua_chon == '4':
                self.xem_lich_su_vay()
            elif lua_chon == '5':
                self.dang_xuat()
                break
            else:
                print("❌ Lựa chọn không hợp lệ!")

# Chạy ứng dụng
if __name__ == "__main__":
    he_thong = HeThongVayOnline()
    he_thong.menu_chinh()
