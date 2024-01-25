import "./style.css";
import Navigationbar from "../Navigationbar/Navbar";
import Productions from "../Productions/Products";
import Footer from "../Footer/Footer";
import Newsletter from "../Newsletter/Newsletter";
import b1 from "../img/blog/b1.jpg";

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
            <h4>TT ve giay</h4>
            <p>tom tat noi dung...</p>
            <a href="https://google.com">CONTINUE READING</a>
          </div>
          <h1>13/01</h1>
        </div>

        <div className="blog-box">
          <div className="blog-img">
            <img src={b1} alt="" />
          </div>
          <div className="blog-details">
            <h4>TT ve giay</h4>
            <p>tom tat noi dung...</p>
            <a href="#">CONTINUE READING</a>
          </div>
          <h1>13/01</h1>
        </div>

        <div className="blog-box">
          <div className="blog-img">
            <img src={b1} alt="" />
          </div>
          <div className="blog-details">
            <h4>TT ve giay</h4>
            <p>tom tat noi dung...</p>
            <a href="#">CONTINUE READING</a>
          </div>
          <h1>13/01</h1>
        </div>

        <div className="blog-box">
          <div className="blog-img">
            <img src={b1} alt="" />
          </div>
          <div className="blog-details">
            <h4>TT ve giay</h4>
            <p>tom tat noi dung...</p>
            <a href="#">CONTINUE READING</a>
          </div>
          <h1>13/01</h1>
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
