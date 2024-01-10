import "./style.css";
import Navigationbar from "../Navigationbar/Navbar";
import Productions from "../Productions/Products";
import Footer from "../Footer/Footer";
import Newsletter from "../Newsletter/Newsletter";

function Cart() {
  return (
    <>
      <Navigationbar />
      <section id="cart" class="section-p1">
        <table id="table" width="100%">
          <thead>
            <tr>
              <td>Remove</td>
              <td>Image</td>
              <td>Sản phẩm</td>
              <td>Giá cả</td>
              <td>Số lượng</td>
              <td>Tổng giá tiền</td>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <a href="#">
                  <i class="far fa-times-circle"></i>
                </a>
              </td>
              <td>
                <img src="img/products/f1.jpg" alt="" />
              </td>
              <td>Giày nike</td>
              <td>100$</td>
              <td>
                <input type="number" value="1" />
              </td>
              <td>$100$</td>
            </tr>
            <tr>
              <td>
                <a href="#">
                  <i class="far fa-times-circle"></i>
                </a>
              </td>
              <td>
                <img src="img/products/f1.jpg" alt="" />
              </td>
              <td>Giày nike</td>
              <td>100$</td>
              <td>
                <input type="number" value="1" />
              </td>
              <td>$100$</td>
            </tr>
            <tr>
              <td>
                <a href="#">
                  <i class="far fa-times-circle"></i>
                </a>
              </td>
              <td>
                <img src="img/products/f1.jpg" alt="" />
              </td>
              <td>Giày nike</td>
              <td>100$</td>
              <td>
                <input type="number" value="1" />
              </td>
              <td>$100$</td>
            </tr>
          </tbody>
        </table>
      </section>

      <section id="cart-add" class="section-p1">
        <div id="coupon">
          <h3>Aplly Coupon</h3>
          <div>
            <input type="text" placeholder="Nhập mã quà tặng" />
            <button class="normal">Apply</button>
          </div>
        </div>
        <div id="subtotal">
          <h3>Hóa đơn</h3>
          <table>
            <tr>
              <td>Số tiền</td>
              <td>300$</td>
            </tr>
            <tr>
              <td>Tiền ship</td>
              <td>Miễn Phí</td>
            </tr>
          </table>
          <button id="thanhtoan" class="normal" onclick="alerttest()">
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
