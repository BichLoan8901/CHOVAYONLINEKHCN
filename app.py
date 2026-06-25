<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vay Online Cá Nhân</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 500px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header h1 {
            color: #333;
            font-size: 28px;
            margin-bottom: 5px;
        }

        .header p {
            color: #666;
            font-size: 14px;
        }

        .loan-amount {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 25px;
        }

        .loan-amount h2 {
            font-size: 14px;
            font-weight: 400;
            opacity: 0.9;
        }

        .loan-amount .amount {
            font-size: 36px;
            font-weight: bold;
            margin: 5px 0;
        }

        .loan-amount .info {
            font-size: 13px;
            opacity: 0.9;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            color: #555;
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 14px;
        }

        .form-group input,
        .form-group select {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s;
        }

        .form-group input:focus,
        .form-group select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .range-slider {
            width: 100%;
            margin: 10px 0;
        }

        .range-values {
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            color: #888;
        }

        .btn {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }

        .btn:active {
            transform: translateY(0);
        }

        .result {
            margin-top: 25px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 15px;
            display: none;
        }

        .result.active {
            display: block;
            animation: fadeIn 0.5s;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .result-item {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
        }

        .result-item:last-child {
            border-bottom: none;
        }

        .result-item .label {
            color: #666;
        }

        .result-item .value {
            font-weight: 600;
            color: #333;
        }

        .result-item .value.highlight {
            color: #667eea;
            font-size: 18px;
        }

        .warning {
            background: #fff3cd;
            color: #856404;
            padding: 12px;
            border-radius: 10px;
            font-size: 13px;
            margin-top: 15px;
            border-left: 4px solid #ffc107;
        }

        .footer {
            text-align: center;
            margin-top: 25px;
            color: #999;
            font-size: 12px;
        }

        .footer a {
            color: #667eea;
            text-decoration: none;
        }

        @media (max-width: 480px) {
            .container {
                padding: 20px;
            }
            
            .loan-amount .amount {
                font-size: 28px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💰 Vay Online</h1>
            <p>Đăng ký vay nhanh chóng - Giải ngân trong 24h</p>
        </div>

        <div class="loan-amount">
            <h2>Số tiền bạn có thể vay</h2>
            <div class="amount" id="displayAmount">5,000,000đ</div>
            <div class="info">Lãi suất từ 1.5%/tháng</div>
        </div>

        <form id="loanForm">
            <div class="form-group">
                <label>Họ và tên</label>
                <input type="text" id="fullName" placeholder="Nhập họ tên của bạn" required>
            </div>

            <div class="form-group">
                <label>Số điện thoại</label>
                <input type="tel" id="phone" placeholder="Nhập số điện thoại" required>
            </div>

            <div class="form-group">
                <label>Email</label>
                <input type="email" id="email" placeholder="Nhập email của bạn">
            </div>

            <div class="form-group">
                <label>Số tiền muốn vay</label>
                <input type="range" id="loanAmount" min="1000000" max="50000000" step="100000" value="5000000" class="range-slider">
                <div class="range-values">
                    <span>1,000,000đ</span>
                    <span>50,000,000đ</span>
                </div>
            </div>

            <div class="form-group">
                <label>Kỳ hạn vay</label>
                <select id="loanTerm">
                    <option value="1">1 tháng</option>
                    <option value="3" selected>3 tháng</option>
                    <option value="6">6 tháng</option>
                    <option value="12">12 tháng</option>
                    <option value="24">24 tháng</option>
                </select>
            </div>

            <button type="submit" class="btn">Đăng ký vay ngay</button>
        </form>

        <div class="result" id="result">
            <h3 style="margin-bottom: 15px; color: #333;">📋 Thông tin khoản vay</h3>
            <div class="result-item">
                <span class="label">Họ tên</span>
                <span class="value" id="resultName">-</span>
            </div>
            <div class="result-item">
                <span class="label">Số điện thoại</span>
                <span class="value" id="resultPhone">-</span>
            </div>
            <div class="result-item">
                <span class="label">Số tiền vay</span>
                <span class="value highlight" id="resultAmount">-</span>
            </div>
            <div class="result-item">
                <span class="label">Kỳ hạn</span>
                <span class="value" id="resultTerm">-</span>
            </div>
            <div class="result-item">
                <span class="label">Lãi suất</span>
                <span class="value" id="resultRate">1.5%/tháng</span>
            </div>
            <div class="result-item">
                <span class="label">Tổng tiền phải trả</span>
                <span class="value highlight" id="resultTotal">-</span>
            </div>
            <div class="result-item">
                <span class="label">Gốc + Lãi mỗi tháng</span>
                <span class="value" id="resultMonthly">-</span>
            </div>
            <div class="warning">
                ⚠️ Vui lòng đọc kỹ điều khoản trước khi vay. Lãi suất có thể thay đổi tùy theo hồ sơ của bạn.
            </div>
        </div>

        <div class="footer">
            <p>Bảo mật thông tin 100% | Hotline: <a href="tel:19001009">1900 1009</a></p>
        </div>
    </div>

    <script>
        // Cập nhật số tiền hiển thị khi kéo slider
        document.getElementById('loanAmount').addEventListener('input', function() {
            const amount = parseInt(this.value);
            document.getElementById('displayAmount').textContent = formatCurrency(amount);
        });

        // Format tiền tệ
        function formatCurrency(amount) {
            return amount.toLocaleString('vi-VN') + 'đ';
        }

        // Xử lý form đăng ký
        document.getElementById('loanForm').addEventListener('submit', function(e) {
            e.preventDefault();

            // Lấy dữ liệu
            const name = document.getElementById('fullName').value.trim();
            const phone = document.getElementById('phone').value.trim();
            const email = document.getElementById('email').value.trim();
            const amount = parseInt(document.getElementById('loanAmount').value);
            const term = parseInt(document.getElementById('loanTerm').value);

            // Validate
            if (!name || !phone) {
                alert('Vui lòng nhập đầy đủ họ tên và số điện thoại!');
                return;
            }

            if (phone.length < 10) {
                alert('Số điện thoại không hợp lệ!');
                return;
            }

            // Tính toán khoản vay
            const interestRate = 0.015; // 1.5%/tháng
            const totalInterest = amount * interestRate * term;
            const totalPayable = amount + totalInterest;
            const monthlyPayment = totalPayable / term;

            // Hiển thị kết quả
            document.getElementById('resultName').textContent = name;
            document.getElementById('resultPhone').textContent = phone;
            document.getElementById('resultAmount').textContent = formatCurrency(amount);
            document.getElementById('resultTerm').textContent = term + ' tháng';
            document.getElementById('resultTotal').textContent = formatCurrency(Math.round(totalPayable));
            document.getElementById('resultMonthly').textContent = formatCurrency(Math.round(monthlyPayment));

            // Hiện kết quả với animation
            const result = document.getElementById('result');
            result.classList.add('active');
            result.scrollIntoView({ behavior: 'smooth', block: 'center' });

            // Lưu vào localStorage (mô phỏng database)
            const loanData = {
                name,
                phone,
                email,
                amount,
                term,
                totalPayable: Math.round(totalPayable),
                monthlyPayment: Math.round(monthlyPayment),
                date: new Date().toISOString()
            };

            // Lưu vào localStorage
            let loans = JSON.parse(localStorage.getItem('loans') || '[]');
            loans.push(loanData);
            localStorage.setItem('loans', JSON.stringify(loans));

            console.log('Đã lưu thông tin vay:', loanData);
        });

        // Kiểm tra nếu có dữ liệu vay trước đó
        window.addEventListener('load', function() {
            const loans = JSON.parse(localStorage.getItem('loans') || '[]');
            if (loans.length > 0) {
                console.log(`Tổng số khoản vay đã đăng ký: ${loans.length}`);
            }
        });
    </script>
</body>
</html>
