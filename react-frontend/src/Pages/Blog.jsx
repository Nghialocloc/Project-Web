import "./style.css";
import Navigationbar from "../Navigationbar/Navbar";
import Productions from "../Productions/Products";
import Footer from "../Footer/Footer";
import Newsletter from "../Newsletter/Newsletter";
import b1 from "../img/blog/k1.jpg";
import b2 from "../img/blog/k2.jpg";
import b3 from "../img/blog/k3.jpg";
import b4 from "../img/blog/k4.jpg";

function Blog() {
  return (
    <>
      <Navigationbar />
      <section id="page-header">
        <h2>#News</h2>
        <p>Fashion yourself with mews everyday!</p>
      </section>
      <section id="blog">
        <div className="blog-box">
          <div className="blog-img">
            <img src={b1} alt="" />
          </div>
          <div className="blog-details">
            <h4>Kobe 8 Court Purple & Radiant Emerald sắp ra mắt!</h4>
            <p>
              Chẳng phải bạn chỉ thích khi những hình bóng tuyệt vời có màu sắc
              và câu chuyện thậm chí còn hay hơn sao? Chà, dường như không ai
              làm điều đó tốt hơn Nike, và lần này dòng sản phẩm được đề cập là
              của Kobe Bryant! Chúng tôi rất vui vì những cú bật nhảy đặc trưng
              đã hoạt động trở lại và phát huy tác dụng vì dường như họ không
              bao giờ trượt với đôi giày tuyệt vời này.
            </p>
            <a href="https://www.nikeshoebot.com/kobe-8-court-purple-radiant-emerald/">
              CONTINUE READING
            </a>
          </div>
          <h1>24/01</h1>
        </div>

        <div className="blog-box">
          <div className="blog-img">
            <img src={b2} alt="" />
          </div>
          <div className="blog-details">
            <h4>Travis Scott Jordan 1 Canary – Diện mạo mới!</h4>
            <p>
              Đúng, chúng tôi biết rằng tông màu đất là màu lựa chọn không chính
              thức của Travis Scott. Và họ đã làm theo phương châm “nếu nó không
              bị hỏng thì tại sao phải sửa nó?” Tuy nhiên, bạn chỉ có thể làm
              được rất nhiều điều với các sắc thái khác nhau của ô liu và nâu.
              Và có vẻ như Jordan Brand và Cactus Jack cũng đã nhận ra sự thật
              đó. Đây có lẽ là lý do tại sao bây giờ chúng ta có tin tức về
              Travis Scott Jordan 1 Canary! Vậy thực chất chiếc giày này là gì?
            </p>
            <a href="https://www.nikeshoebot.com/travis-scott-jordan-1-canary/">
              CONTINUE READING
            </a>
          </div>
          <h1>23/01</h1>
        </div>

        <div className="blog-box">
          <div className="blog-img">
            <img src={b3} alt="" />
          </div>
          <div className="blog-details">
            <h4>Tết Nguyên Đán Jordan 2 – Sức nóng tuyệt vời!</h4>
            <p>
              Nike và Jordan Brand đều vượt lên chính mình mỗi năm khi phát hành
              sản phẩm vào dịp Tết Nguyên đán. Và năm nay cũng không có gì khác
              biệt với một số cách phối màu độc đáo trên các kiểu dáng khác
              nhau. Nhưng JB thực sự đã nỗ lực hết mình trong năm nay để chào
              mừng Năm con Rồng!
            </p>
            <a href="https://www.nikeshoebot.com/jordan-2-chinese-new-year/">
              CONTINUE READING
            </a>
          </div>
          <h1>19/01</h1>
        </div>

        <div className="blog-box">
          <div className="blog-img">
            <img src={b4} alt="" />
          </div>
          <div className="blog-details">
            <h4>Cách tìm giày khi bạn có bàn chân rộng</h4>
            <p>
              Tìm một đôi giày thoải mái khi bàn chân của bạn rộng hơn mức trung
              bình có thể không phải lúc nào cũng là một việc dễ dàng. Những đôi
              giày bạn có thể tìm thấy trong các cửa hàng thường vừa vặn với bàn
              chân có kích thước tiêu chuẩn và một số mẫu chỉ thoải mái hơn cho
              những người có bàn chân hẹp hơn.
            </p>
            <a href="https://www.vanhoecks.com/how-to-find-shoes-when-you-have-wide-feet.php">
              CONTINUE READING
            </a>
          </div>
          <h1>1/01</h1>
        </div>
      </section>
      <section id="pagination">
        <a href="#">1</a>
        <a href="#">2</a>
        <a href="#">
          <i className="fa fa-long-arrow-alt-right"></i>
        </a>
      </section>
      <Newsletter />
      <Footer />
    </>
  );
}
export default Blog;
