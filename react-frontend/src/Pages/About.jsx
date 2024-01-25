import "./style.css";
import Navigationbar from "../Navigationbar/Navbar";
import Productions from "../Productions/Products";
import Footer from "../Footer/Footer";
import Newsletter from "../Newsletter/Newsletter";
import abouta6 from "../img/about/a6.jpg";

function About() {
  return (
    <>
      <Navigationbar />
      <section id="page-header" class="about-header">
        <h2>#Về chúng tôi</h2>
        <p>Hiểu rõ hơn về cửa tiệm</p>
      </section>
      <section id="about-head" className="section-p1">
        <img src={abouta6} alt="" />
        <div>
          <h2>Chúng tôi là ai?</h2>
          <p>Giới thiệu cửa hàng....</p>
          <abbr title="">Mục tiêu...</abbr>
          <br></br>
          <marquee bgcolor="#ccc" loop="-1">
            Cảm ơn đã tin tưởng và ủng hộ chúng tôi, các bạn là nguồn động lực
            lớn nhất để chúng tôi luôn cố gắng đem về các sản phẩm mới chất
            lượng nhất.
          </marquee>
        </div>
      </section>
      <Newsletter />
      <Footer />
    </>
  );
}
export default About;
