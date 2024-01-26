import "./style.css";
import Navigationbar from "../Navigationbar/Navbar";
import Productions from "../Productions/Products";
import Footer from "../Footer/Footer";
import Newsletter from "../Newsletter/Newsletter";
import f1 from "../img/products/f1.jpg";

function Cart() {
  return (
    <>
      <Navigationbar />
      <section id="cart" className="section-p1">
        <table id="table" width="100%">
          <thead>
            <tr>
              <th>Remove</th>
              <th>Image</th>
              <th>Sản phẩm</th>
              <th>Giá cả</th>
              <th>Số lượng</th>
              <th>Tổng giá tiền</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <a href="#">
                  <i className="far fa-times-circle"></i>
                </a>
              </td>
              <td>
                <img src={f1} alt="" />
              </td>
              <td>PUMA BLACK-OCE</td>
              <td>140$</td>
              <td>
                <input type="number" defaultValue="1" />
              </td>
              <td>$140$</td>
            </tr>
            <tr>
              <td>
                <a href="#">
                  <i className="far fa-times-circle"></i>
                </a>
              </td>
              <td>
                <img src={f1} alt="" />
              </td>
              <td>PUMA BLACK-OCE</td>
              <td>140$</td>
              <td>
                <input type="number" defaultValue="1" />
              </td>
              <td>$140$</td>
            </tr>
            <tr>
              <td>
                <a href="#">
                  <i className="far fa-times-circle"></i>
                </a>
              </td>
              <td>
                <img src={f1} alt="" />
              </td>
              <td>PUMA BLACK-OCE </td>
              <td>140$</td>
              <td>
                <input type="number" defaultValue="1" />
              </td>
              <td>$140$</td>
            </tr>
          </tbody>
        </table>
      </section>

      <section id="cart-add" className="section-p1">
        <div id="coupon">
          <h3>Apply Coupon</h3>
          <div>
            <input type="text" placeholder="Nhập mã quà tặng" />
            <button className="normal">Apply</button>
          </div>
        </div>
        <div id="subtotal">
          <h3>Hóa đơn</h3>
          <table>
            <thead>
              <tr>
                <td>Số tiền</td>
                <td>520$</td>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Tiền ship</td>
                <td>Miễn Phí</td>
              </tr>
            </tbody>
          </table>
          <button id="thanhtoan" className="normal">
            Thanh toán
          </button>
        </div>
      </section>
      <Newsletter />
      <Footer />
    </>
  );
}
export default Cart;
