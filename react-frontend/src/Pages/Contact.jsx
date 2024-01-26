import "./style.css";
import Navigationbar from "../Navigationbar/Navbar";
import Productions from "../Productions/Products";
import Footer from "../Footer/Footer";
import Newsletter from "../Newsletter/Newsletter";
import p1 from "../img/people/1.png";
import p2 from "../img/people/2.png";
import p3 from "../img/people/3.png";

function Contact() {
  return (
    <>
      <Navigationbar />
      <section id="page-header" className="about-header">
        <h2>#Liên hệ</h2>
        <p>Luôn luôn sẵn sàng</p>
      </section>
      <section id="contact-details">
        <div className="details">
          <h2></h2>
          <h3></h3>
          <div className="spacecing-20px">
            <span>Liên hệ</span>
            <li>
              <i className="fa fa-map"></i>
              <p>Hà Nội Việt Nam</p>
            </li>
            <li>
              <i className="far fa-envelope"></i>
              <p>Mike_store@gmail.com</p>
            </li>
            <li>
              <i className="fas fa-phone-alt"></i>
              <p>0900113113</p>
            </li>
            <li>
              <i className="far fa-clock"></i>
              <p>Thứ 2 - thứ 7 hàng tuần: 8.00am - 18.00pm</p>
            </li>
          </div>
        </div>
      </section>
      <section id="form-details">
        <form action="">
          <span>Yêu cầu hỗ trợ</span>
          <h2>Chúng tôi luôn sẵn sàng lắng nghe</h2>
          <input type="text" placeholder="Email của bạn" />
          <input type="text" placeholder="Tiêu đề" />
          <textarea
            name=""
            id=""
            cols="30"
            rows="10"
            placeholder="Mike Store cảm ơn phản hồi của bạn..."
          ></textarea>
          <button className="normal">Gửi</button>
        </form>
        <div className="people">
          <div>
            <img src={p1} alt="" />
            <p>
              <span>Minh Nghĩa</span>
              Chuyên viên tư vấn khách hàng
              <br></br>
              Số điện thoại: +0900115115
              <br></br>
              Liên hệ: Nghia@gmail.com
            </p>
          </div>
          <div>
            <img src={p2} alt="" />
            <p>
              <span>Đức Phúc</span> Đối tác quảng cáo
              <br></br>
              Số điện thoại: +0900114114
              <br></br>
              Liên hệ: Phuc@gmail.com
            </p>
          </div>
          <div>
            <img src={p3} alt="" />
            <p>
              <span>Minh Đức</span> Quản lý
              <br></br>
              Số điện thoại: +0900116116
              <br></br>
              Liên hệ: Duc@gmail.com
            </p>
          </div>
        </div>
      </section>
      <Footer />
    </>
  );
}
export default Contact;
