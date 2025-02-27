from flask import Flask
from upload import upload_bp
from get_sales import sales_bp

app = Flask(__name__)

# Đăng ký các blueprint
app.register_blueprint(upload_bp)
app.register_blueprint(sales_bp)

if __name__ == '__main__':
    app.run(debug=True, port=8000) 