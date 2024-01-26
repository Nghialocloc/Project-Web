import "./style.css";
import "../Productions/Products.css";
import Navigationbar from "../Navigationbar/Navbar";
import Productions from "../Productions/Products";
import Footer from "../Footer/Footer";
import Newsletter from "../Newsletter/Newsletter";
import data from "../db/data";
function Shopping() {
  return (
    <>
      <Navigationbar />
      <section id="page-header">
        <h2>super value deals</h2>
        <p>Save more with coupons &up to 70% off!</p>
      </section>
      <section id="product1" className="section-p1">
        <div className="pro-container">
          {data.map((data, index) => {
            return (
              <div className="pro" key={index}>
                <a href={"detail"}>
                  <div className="padding-img">
                    <img src={data.img}></img>
                  </div>
                  <div className="des">
                    <span>{data.company}</span>
                    <h5>{data.title}</h5>
                    <div className="star">
                      <i className="far fa-star"></i>
                      <i className="far fa-star"></i>
                      <i className="far fa-star"></i>
                      <i className="far fa-star"></i>
                      <i className="far fa-star"></i>
                    </div>
                    <h4>{data.price}</h4>
                  </div>
                  <button href="cart">
                    <i className="fa fa-shopping-cart cart"></i>
                  </button>
                </a>
              </div>
            );
          })}
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
export default Shopping;
