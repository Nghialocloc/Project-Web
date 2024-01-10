import "./style.css";
import Navigationbar from "../Navigationbar/Navbar";
import Productions from "../Productions/Products";
import Footer from "../Footer/Footer";
import Newsletter from "../Newsletter/Newsletter";

function Shopping() {
  return (
    <>
      <Navigationbar />
      <section id="page-header">
        <h2>super value deals</h2>
        <p>Save more with coupons &up to 70% off!</p>
      </section>
      <Productions />
      <section id="pagination">
        <a href="#">1</a>
        <a href="#">2</a>
        <a href="#">
          <i class="fa fa-long-arrow-alt-right"></i>
        </a>
      </section>
      <Newsletter />
      <Footer />
    </>
  );
}
export default Shopping;
