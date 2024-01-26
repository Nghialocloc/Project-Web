import "./style.css";
import Navigationbar from "../Navigationbar/Navbar";
import Productions from "../Productions/Products";
import Footer from "../Footer/Footer";
import Newsletter from "../Newsletter/Newsletter";
import abouta6 from "../img/about/a6.jpg";

function Chinhsachthanhtoan() {
  return (
    <>
      <Navigationbar />
      <section id="page-header" className="about-header">
        <h2>Chính sách</h2>
      </section>
      <section id="about-head" className="section-p1">
        <img src="{abouta6}" alt="" />
        <div>
          <h2>Chính sách thanh toán</h2>
          <p>
            <strong>1./ Khách hàng thanh toán bằng tiền mặt</strong>
          </p>
          <br />
          <p>
            Khách hàng đặt hàng - Khách hàng kiểm tra hàng, kí biên bản nhận
            hàng và thanh toán tiền mặt cho nhân viên giao hàng
          </p>
          <br />
          <p>
            <strong>2./ Khách hàng thanh toán bằng Chuyển khoản:</strong>
          </p>
          <br />
          <ul>
            <li>Chủ tài khoản: AAAAAAAA</li>
            <li>STK: AAAAAAAAAA</li>
            <li>Ngân hàng Vietcombank ( VCB)</li>
          </ul>
          <br />
          <p>
            Lưu ý giá trên website: mikestore.com là giá chưa bao gồm thuế VAT
          </p>
          <br />
        </div>
      </section>
      <section id="pagination">
        <a href="chinhsach">1</a>
        <a href="chinhsachthanhtoan">2</a>
        <a href="chinhsachvanchuyen">3</a>
        <a href="chinhsachdoitra">4</a>
      </section>
      <Newsletter />
      <Footer />
    </>
  );
}
export default Chinhsachthanhtoan;
