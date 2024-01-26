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
      <section id="page-header" className="about-header">
        <h2>#Về chúng tôi</h2>
        <p>Hiểu rõ hơn về cửa tiệm</p>
      </section>
      <section id="about-head" className="section-p1">
        <img src={abouta6} alt="" />
        <div>
          <h2>MIKESTORE 👞</h2>
          <p>
            Thành lập từ năm 2023, chúng tôi là một trong những nhà phân phối
            Giày chính hãng xách tay uy tín tại Hà Nội ký hợp đồng phân phối lớn
            với nhiều hãng giày nổi tiếng trên thế giới Mặc dù là một cử hàng
            non trẻ nhưng với nhiệt huyết có thể đem tới những sản phẩm chất
            lượng cao nhất cho khách hàng, chúng tôi luôn cam kết chết lượng
            100% chính hãng tới từ sản phẩm của mình.
          </p>
          <br></br>
          <p>
            {" "}
            Chúng tôi mong muốn được đem lại cho khách hàng sự hài lòng và thỏa
            mãn với tất cả các sản phẩm của mình.
            <br />
            Bên cạnh đó là đội ngũ nhân viên nhiệt tình chu đáo và đầy kinh
            nghiệm của chúng tôi luôn đưa được ra cho khách hàng những thông tin
            có giá trị và giúp khách hàng lựa chọn được những sản phẩm phù hợp
            nhất
          </p>
          <br />
          Chúng tôi mong muốn sự đóng góp của khách hàng sẽ giúp chúng tôi ngày
          một phát triển để từ đó củng cố thêm lòng tin của khách hàng với chúng
          tôi. Chúng tôi rất biết ơn sự tin tưởng của khách hàng đã đến với Mike
          shoes store.
          <abbr title="">
            Mục tiêu của chúng tôi luôn tuân thủ những phương châm khách hàng là
            thượng đế và luôn làm mọi thứ phù hợp với yêu cầu khách hàng nhất
            trong tất cả mọi mặt
          </abbr>
          <br></br>
          <marquee bgcolor="#ccc" loop="-1">
            Cảm ơn đã tin tưởng và ủng hộ chúng tôi, các bạn là nguồn động lực
            lớn nhất để chúng tôi luôn cố gắng đem về các sản phẩm mới chất
            lượng nhất. Mike Shoes Store xin chân thành cảm ơn tất cả các khách
            hàng đã, đang và sẽ ủng hộ chúng tôi.
          </marquee>
        </div>
      </section>
      <Newsletter />
      <Footer />
    </>
  );
}
export default About;
