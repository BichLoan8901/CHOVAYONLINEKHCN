import streamlit as st
st.image("logo.jpg")
# Tiêu đề app
st.title("APP CHO VAY ONLINE KHÁCH HÀNG CÁ NHÂN_VÕ THỊ BÍCH LOAN")
# loan_app.py
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import uuid

class User:
    """Lớp đại diện cho người dùng"""
    def __init__(self, user_id: str, name: str, email: str, phone: str, credit_score: int = 700):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.credit_score = credit_score
        self.loans = []
        
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'credit_score': self.credit_score
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data['user_id'],
            data['name'],
            data['email'],
            data['phone'],
            data['credit_score']
        )

class Loan:
    """Lớp đại diện cho khoản vay"""
    def __init__(self, loan_id: str, user_id: str, amount: float, interest_rate: float, 
                 term_months: int, purpose: str = ""):
        self.loan_id = loan_id
        self.user_id = user_id
        self.amount = amount
        self.interest_rate = interest_rate
        self.term_months = term_months
        self.purpose = purpose
        self.status = 'pending'  # pending, approved, rejected, active, completed, defaulted
        self.created_date = datetime.now()
        self.approved_date = None
        self.due_date = None
        self.payments = []
        self.total_paid = 0
        self.remaining_balance = amount
        
    def approve_loan(self):
        """Phê duyệt khoản vay"""
        self.status = 'approved'
        self.approved_date = datetime.now()
        self.due_date = self.created_date + timedelta(days=self.term_months * 30)
        
    def make_payment(self, amount: float) -> bool:
        """Thực hiện thanh toán"""
        if self.status not in ['active', 'approved']:
            return False
        
        if amount > self.remaining_balance:
            return False
            
        self.total_paid += amount
        self.remaining_balance -= amount
        self.payments.append({
            'date': datetime.now().isoformat(),
            'amount': amount,
            'balance_remaining': self.remaining_balance
        })
        
        if self.remaining_balance <= 0:
            self.status = 'completed'
            self.remaining_balance = 0
            
        return True
    
    def calculate_monthly_payment(self) -> float:
        """Tính số tiền phải trả hàng tháng"""
        if self.interest_rate == 0:
            return self.amount / self.term_months
        
        monthly_rate = self.interest_rate / 100 / 12
        if self.term_months == 0:
            return self.amount
            
        factor = (1 + monthly_rate) ** self.term_months
        return self.amount * monthly_rate * factor / (factor - 1)
    
    def get_remaining_payments(self) -> int:
        """Số tháng còn lại cần thanh toán"""
        if self.status in ['completed', 'defaulted']:
            return 0
        if self.due_date:
            days_remaining = (self.due_date - datetime.now()).days
            return max(0, days_remaining // 30)
        return self.term_months
    
    def to_dict(self):
        return {
            'loan_id': self.loan_id,
            'user_id': self.user_id,
            'amount': self.amount,
            'interest_rate': self.interest_rate,
            'term_months': self.term_months,
            'purpose': self.purpose,
            'status': self.status,
            'created_date': self.created_date.isoformat(),
            'approved_date': self.approved_date.isoformat() if self.approved_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'total_paid': self.total_paid,
            'remaining_balance': self.remaining_balance,
            'payments': self.payments
        }
    
    @classmethod
    def from_dict(cls, data):
        loan = cls(
            data['loan_id'],
            data['user_id'],
            data['amount'],
            data['interest_rate'],
            data['term_months'],
            data.get('purpose', '')
        )
        loan.status = data['status']
        loan.created_date = datetime.fromisoformat(data['created_date'])
        loan.approved_date = datetime.fromisoformat(data['approved_date']) if data['approved_date'] else None
        loan.due_date = datetime.fromisoformat(data['due_date']) if data['due_date'] else None
        loan.total_paid = data['total_paid']
        loan.remaining_balance = data['remaining_balance']
        loan.payments = data['payments']
        return loan

class LoanApp:
    """Ứng dụng quản lý cho vay"""
    def __init__(self, data_file='loan_data.json'):
        self.data_file = data_file
        self.users: Dict[str, User] = {}
        self.loans: Dict[str, Loan] = {}
        self.current_user: Optional[User] = None
        self.load_data()
        
    def save_data(self):
        """Lưu dữ liệu vào file"""
        data = {
            'users': {uid: user.to_dict() for uid, user in self.users.items()},
            'loans': {lid: loan.to_dict() for lid, loan in self.loans.items()}
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
            
    def load_data(self):
        """Tải dữ liệu từ file"""
        if not os.path.exists(self.data_file):
            return
            
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                
            self.users = {uid: User.from_dict(user_data) for uid, user_data in data.get('users', {}).items()}
            self.loans = {lid: Loan.from_dict(loan_data) for lid, loan_data in data.get('loans', {}).items()}
            
        except (json.JSONDecodeError, KeyError):
            print("Lỗi khi tải dữ liệu. Bắt đầu với dữ liệu trống.")
            
    def register_user(self, name: str, email: str, phone: str) -> User:
        """Đăng ký người dùng mới"""
        user_id = str(uuid.uuid4())[:8]
        user = User(user_id, name, email, phone)
        self.users[user_id] = user
        self.save_data()
        return user
    
    def login(self, user_id: str) -> Optional[User]:
        """Đăng nhập người dùng"""
        if user_id in self.users:
            self.current_user = self.users[user_id]
            return self.current_user
        return None
        
    def apply_loan(self, user_id: str, amount: float, interest_rate: float, 
                   term_months: int, purpose: str = "") -> Optional[Loan]:
        """Đăng ký khoản vay mới"""
        if user_id not in self.users:
            print("Người dùng không tồn tại!")
            return None
            
        user = self.users[user_id]
        
        # Kiểm tra credit score
        if user.credit_score < 600:
            print(f"Điểm tín dụng {user.credit_score} quá thấp. Không thể vay!")
            return None
            
        # Kiểm tra số nợ hiện tại
        active_loans = [loan for loan in self.loans.values() 
                       if loan.user_id == user_id and loan.status in ['active', 'approved']]
        total_debt = sum(loan.remaining_balance for loan in active_loans)
        
        if total_debt > 50000000:  # Giới hạn nợ tối đa 50 triệu
            print("Số nợ hiện tại vượt quá giới hạn cho phép!")
            return None
            
        loan_id = str(uuid.uuid4())[:8]
        loan = Loan(loan_id, user_id, amount, interest_rate, term_months, purpose)
        self.loans[loan_id] = loan
        self.save_data()
        print(f"Đã tạo đơn vay thành công! Mã khoản vay: {loan_id}")
        return loan
    
    def approve_loan(self, loan_id: str):
        """Phê duyệt khoản vay"""
        if loan_id not in self.loans:
            print("Không tìm thấy khoản vay!")
            return
            
        loan = self.loans[loan_id]
        if loan.status != 'pending':
            print("Khoản vay này đã được xử lý!")
            return
            
        # Kiểm tra credit score của người vay
        user = self.users.get(loan.user_id)
        if user and user.credit_score < 600:
            print("Điểm tín dụng thấp. Không thể phê duyệt!")
            loan.status = 'rejected'
            self.save_data()
            return
            
        loan.approve_loan()
        loan.status = 'active'
        self.save_data()
        print(f"Khoản vay {loan_id} đã được phê duyệt!")
        print(f"Số tiền phải trả hàng tháng: {loan.calculate_monthly_payment():,.0f} VND")
        
    def make_payment(self, loan_id: str, amount: float) -> bool:
        """Thanh toán khoản vay"""
        if loan_id not in self.loans:
            print("Không tìm thấy khoản vay!")
            return False
            
        loan = self.loans[loan_id]
        result = loan.make_payment(amount)
        if result:
            self.save_data()
            print(f"Đã thanh toán {amount:,.0f} VND. Còn nợ: {loan.remaining_balance:,.0f} VND")
        else:
            print("Thanh toán thất bại!")
        return result
        
    def view_loans(self, user_id: str = None):
        """Xem danh sách khoản vay"""
        if user_id:
            loans = [loan for loan in self.loans.values() if loan.user_id == user_id]
        else:
            loans = list(self.loans.values())
            
        if not loans:
            print("Không có khoản vay nào!")
            return
            
        print("\n" + "="*80)
        print(f"{'Mã vay':<10} {'Người vay':<15} {'Số tiền':<15} {'Lãi suất':<10} {'Trạng thái':<12} {'Còn nợ':<15}")
        print("-"*80)
        for loan in loans:
            user = self.users.get(loan.user_id)
            user_name = user.name if user else "Không xác định"
            status_vi = {
                'pending': 'Chờ duyệt',
                'approved': 'Đã duyệt',
                'rejected': 'Từ chối',
                'active': 'Đang vay',
                'completed': 'Đã trả',
                'defaulted': 'Quá hạn'
            }.get(loan.status, loan.status)
            
            print(f"{loan.loan_id:<10} {user_name:<15} {loan.amount:>13,} VND {loan.interest_rate:>9.1f}% "
                  f"{status_vi:<12} {loan.remaining_balance:>13,} VND")
        print("="*80)
        
    def get_loan_details(self, loan_id: str):
        """Xem chi tiết khoản vay"""
        if loan_id not in self.loans:
            print("Không tìm thấy khoản vay!")
            return
            
        loan = self.loans[loan_id]
        user = self.users.get(loan.user_id)
        
        print("\n" + "="*60)
        print(f"CHI TIẾT KHOẢN VAY: {loan_id}")
        print("="*60)
        print(f"Người vay: {user.name if user else 'Không xác định'}")
        print(f"Số tiền vay: {loan.amount:,.0f} VND")
        print(f"Lãi suất: {loan.interest_rate}%/năm")
        print(f"Thời hạn: {loan.term_months} tháng")
        print(f"Mục đích: {loan.purpose if loan.purpose else 'Không có'}")
        print(f"Trạng thái: {loan.status}")
        print(f"Ngày tạo: {loan.created_date.strftime('%d/%m/%Y %H:%M')}")
        if loan.approved_date:
            print(f"Ngày duyệt: {loan.approved_date.strftime('%d/%m/%Y %H:%M')}")
        if loan.due_date:
            print(f"Hạn thanh toán: {loan.due_date.strftime('%d/%m/%Y')}")
        print(f"Số tiền đã trả: {loan.total_paid:,.0f} VND")
        print(f"Số tiền còn nợ: {loan.remaining_balance:,.0f} VND")
        print(f"Tháng còn lại: {loan.get_remaining_payments()} tháng")
        print(f"Số tiền phải trả mỗi tháng: {loan.calculate_monthly_payment():,.0f} VND")
        
        if loan.payments:
            print("\nLỊCH SỬ THANH TOÁN:")
            print("-"*40)
            for payment in loan.payments:
                date = datetime.fromisoformat(payment['date'])
                print(f"{date.strftime('%d/%m/%Y')}: {payment['amount']:,.0f} VND - "
                      f"Còn nợ: {payment['balance_remaining']:,.0f} VND")
        print("="*60)
        
    def view_user_info(self):
        """Xem thông tin người dùng hiện tại"""
        if not self.current_user:
            print("Chưa đăng nhập!")
            return
            
        user = self.current_user
        print("\n" + "="*50)
        print("THÔNG TIN NGƯỜI DÙNG")
        print("="*50)
        print(f"Mã số: {user.user_id}")
        print(f"Tên: {user.name}")
        print(f"Email: {user.email}")
        print(f"SĐT: {user.phone}")
        print(f"Điểm tín dụng: {user.credit_score}")
        
        # Tổng hợp khoản vay
        user_loans = [loan for loan in self.loans.values() if loan.user_id == user.user_id]
        total_loans = len(user_loans)
        active_loans = len([l for l in user_loans if l.status == 'active'])
        total_debt = sum(l.remaining_balance for l in user_loans if l.status in ['active', 'approved'])
        completed_loans = len([l for l in user_loans if l.status == 'completed'])
        
        print(f"\nTổng số khoản vay: {total_loans}")
        print(f"Đang vay: {active_loans}")
        print(f"Đã trả: {completed_loans}")
        print(f"Tổng nợ: {total_debt:,.0f} VND")
        print("="*50)

def main():
    app = LoanApp()
    
    # Tạo dữ liệu mẫu
    if not app.users:
        demo_user = app.register_user("Nguyễn Văn A", "a@email.com", "0901234567")
        demo_user.credit_score = 750
        app.save_data()
    
    while True:
        print("\n" + "="*50)
        print("ỨNG DỤNG VAY ONLINE CÁ NHÂN")
        print("="*50)
        print("1. Đăng nhập")
        print("2. Đăng ký tài khoản mới")
        print("3. Xem danh sách khoản vay")
        print("4. Đăng ký vay")
        print("5. Phê duyệt khoản vay (Admin)")
        print("6. Thanh toán khoản vay")
        print("7. Xem chi tiết khoản vay")
        print("8. Xem thông tin cá nhân")
        print("9. Thoát")
        print("="*50)
        
        if app.current_user:
            print(f"Đang đăng nhập: {app.current_user.name}")
        else:
            print("Chưa đăng nhập")
        
        choice = input("Chọn chức năng (1-9): ").strip()
        
        if choice == '1':
            if app.current_user:
                print("Bạn đã đăng nhập!")
                continue
            user_id = input("Nhập mã người dùng: ").strip()
            user = app.login(user_id)
            if user:
                print(f"Đăng nhập thành công! Xin chào {user.name}")
            else:
                print("Đăng nhập thất bại! Mã người dùng không tồn tại.")
                
        elif choice == '2':
            name = input("Họ và tên: ").strip()
            email = input("Email: ").strip()
            phone = input("Số điện thoại: ").strip()
            if name and email and phone:
                user = app.register_user(name, email, phone)
                print(f"Đăng ký thành công! Mã người dùng của bạn: {user.user_id}")
                # Tự động đăng nhập
                app.current_user = user
                print(f"Chào mừng {user.name}!")
            else:
                print("Vui lòng điền đầy đủ thông tin!")
                
        elif choice == '3':
            if app.current_user:
                app.view_loans(app.current_user.user_id)
            else:
                print("Vui lòng đăng nhập để xem khoản vay của bạn!")
                if input("Xem tất cả khoản vay? (y/n): ").lower() == 'y':
                    app.view_loans()
                    
        elif choice == '4':
            if not app.current_user:
                print("Vui lòng đăng nhập trước!")
                continue
                
            try:
                amount = float(input("Số tiền vay (VND): ").strip())
                interest = float(input("Lãi suất (%/năm): ").strip())
                term = int(input("Thời hạn (tháng): ").strip())
                purpose = input("Mục đích vay (không bắt buộc): ").strip()
                
                app.apply_loan(app.current_user.user_id, amount, interest, term, purpose)
            except ValueError:
                print("Dữ liệu không hợp lệ! Vui lòng nhập số.")
                
        elif choice == '5':
            # Admin chỉ có thể phê duyệt nếu là admin (trong demo này cho phép tất cả)
            loan_id = input("Nhập mã khoản vay cần phê duyệt: ").strip()
            app.approve_loan(loan_id)
            
        elif choice == '6':
            if not app.current_user:
                print("Vui lòng đăng nhập trước!")
                continue
                
            loan_id = input("Nhập mã khoản vay: ").strip()
            try:
                amount = float(input("Số tiền thanh toán (VND): ").strip())
                app.make_payment(loan_id, amount)
            except ValueError:
                print("Số tiền không hợp lệ!")
                
        elif choice == '7':
            loan_id = input("Nhập mã khoản vay: ").strip()
            app.get_loan_details(loan_id)
            
        elif choice == '8':
            app.view_user_info()
            
        elif choice == '9':
            print("Cảm ơn bạn đã sử dụng ứng dụng!")
            break
            
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn từ 1-9.")

if __name__ == "__main__":
    main()
