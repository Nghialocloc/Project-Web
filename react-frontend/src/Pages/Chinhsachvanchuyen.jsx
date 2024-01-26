import "./style.css";
import Navigationbar from "../Navigationbar/Navbar";
import Productions from "../Productions/Products";
import Footer from "../Footer/Footer";
import Newsletter from "../Newsletter/Newsletter";
import abouta6 from "../img/about/a6.jpg";

function Chinhsachvanchuyen() {
  return (
    <>
      <Navigationbar />
      <section id="page-header" className="about-header">
        <h2>Chính sách vận chuyển</h2>
      </section>
      <section id="about-head" className="section-p1">
        <img src="{abouta6}" alt="" />
        <div>
          <p>
            <strong>1./ Hình thức vận chuyển bao gồm: </strong>
            <br />
            &#8211; Qua các đơn vị vận chuyển chuyên nghiệp như: Viettel post,
            J&amp;T, Giaohangnhanh, Giaohangtietkiem&#8230; áp dụng cho các đơn
            hàng khách lẻ, cộng tác viên
            <br />
            &#8211; Qua các chành xe tải : áp dụng đối với các khách hàng đại
            lý, sỉ với số lượng lớn
          </p>
          <br />
          <p>
            <strong>2./ Biểu phí vận chuyển:</strong>
            <br />
            &#8211; Đối với khách hàng khu vực Hà Nội: Miễn phí cho đơn hàng từ
            150.000vnđ trở lên
            <br />
            &#8211; Đối với khách hàng liên tỉnh: Phí giao hàng dao động từ
            20.000vnđ &#8211; 50.000vnđ tùy theo cân nặng và số lượng hàng đặt.
            <br />
            &#8211; Hiện nay Giày thể thao Mike Store đang áp dụng miễn phí ship
            trên toàn quốc đối với khách hàng đã là khách hàng thân thiết của
            Giày Mike Store. ( cho tới khi có thông báo mới)
          </p>
          <br />
          <p>
            <strong>3./ Thời gian giao hàng:</strong>
            <br />
            &#8211; Nội thành Hà Nội : giao trong ngày hoặc hỏa tốc nếu khách
            hàng yêu cầu ( phí vận chuyển thỏa thuận)
            <br />
            &#8211; Ngoại thành Hà Nội và các tỉnh lân cận: giao trong 2-3 ngày
            làm việc
            <br />
            &#8211; Ngoại tỉnh : 3-5 ngày làm việc
          </p>
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
export default Chinhsachvanchuyen;
