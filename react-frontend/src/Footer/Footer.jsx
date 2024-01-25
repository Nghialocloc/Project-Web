import "./Footer.css";
import logo from "../img/logo.png";
function Footer() {
  return (
    <footer className="section-p1">
      <div className="col">
        <img src={logo} alt="" />
        <h4>Contact</h4>
        <p>
          <strong>Address:</strong> Ha Noi Viet Nam
        </p>
        <p>
          <strong>Phone:</strong> 09001133113
        </p>
        <p>
          <strong>Hours:</strong> 08:00 - 18:00. Mon - Sat
        </p>
        <div className="follow">
          <h4>Follow us</h4>
          <div className="icon">
            <i className="fab fa-facebook-f"></i>
            <i className="fab fa-instagram"></i>
            <i className="fab fa-youtube"></i>
          </div>
        </div>
      </div>
      <div className="col">
        <h4>About</h4>
        <a href="#">Về chúng tôi</a>
        <a href="#">Chính sách</a>
        <a href="#">Liên hệ</a>
        <a href="#">Hỗ trợ khách hàng</a>
      </div>
      <div className="col">
        <h4>My Account</h4>
        <a href="#">Sign In</a>
        <a href="#">View Cart</a>
        <a href="#">Wishlist</a>
        <a href="#">Track my Order</a>
      </div>
      <div className="coppyright">
        <p>
          <a href="trangchu.jsx">Mike Shoes Store</a> - All rights reserved ©
          2023 - Designed by
          <span id="footer-G"> group 4th</span>
        </p>
      </div>
    </footer>
  );
}

export default Footer;
