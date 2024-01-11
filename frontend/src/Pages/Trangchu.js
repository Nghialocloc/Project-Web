import "./style.css";
import Navigationbar from "../Navigationbar/Navbar";
import Productions from "../Productions/Products";
import Footer from "../Footer/Footer";
import Newsletter from "../Newsletter/Newsletter";
import Recommmened from "../Recommended/Recommmened";
import Sidebar from "../Sidebar/Sidebar";

function trangChu() {
  return (
    <>
      <Navigationbar />
      <section id="hero">
        <h4>trade-in-offer</h4>
        <h2>super value deals</h2>
        <h1>On all Products</h1>
        <p>Save more with coupons &up to 70% off!</p>
        <button>Shop Now</button>
      </section>

      <section id="feature" class="section-p1">
        <div class="fe-box">
          <img src="img/features/f1.png" />
          <h6>Super fast</h6>
        </div>
        <div class="fe-box">
          <img src="img/features/f2.png" />
          <h6>Online order</h6>
        </div>
        <div class="fe-box">
          <img src="img/features/f3.png" />
          <h6>Save money</h6>
        </div>
        <div class="fe-box">
          <img src="img/features/f4.png" />
          <h6>Promotions</h6>
        </div>
        <div class="fe-box">
          <img src="img/features/f5.png" />
          <h6>Happy Sell</h6>
        </div>
        <div class="fe-box">
          <img src="img/features/f6.png" />
          <h6>Always support</h6>
        </div>
      </section>
      <section id="banner" class="section-m1">
        <h4>Repair Servieces</h4>
        <h2>
          Winter is comming <span>30%</span> OFF
        </h2>
        <button class="normal">Explore More</button>
      </section>

      <section id="banner3">
        <div class="banner-box">
          <h2>Upcomming season</h2>
          <h3>Winteer Collection -30% OFF</h3>
        </div>
        <div class="banner-box banner-box2">
          <h2>News Everyday</h2>
          <h3>Fashion yourself</h3>
        </div>
        <div class="banner-box banner-box3">
          <h2>Trendy</h2>
          <h3>Catch off the trend</h3>
        </div>
      </section>
      <Productions />
      <Newsletter />
      <Footer />
    </>
  );
}

export default trangChu;
