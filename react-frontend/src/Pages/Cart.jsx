import "./style.css";
import Navigationbar from "../Navigationbar/Navbar";
import Productions from "../Productions/Products";
import Footer from "../Footer/Footer";
import Newsletter from "../Newsletter/Newsletter";
import f1 from "../img/products/Nike-air-force-107-LB.webp";
import { useState } from "react";

function handleDelete(){
  return null;
}

function handleEdit(){
  return null;
}



function Cart() {


  return (
    <>
      <Navigationbar />
      <section id="cart" className="section-p1">
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
                <button type="button" onClick={handleDelete}>
                  <i className="far fa-times-circle"></i>
                </button>
              </td>
              <td>
                <img src={f1} alt="" />
              </td>
              <td>Giày nike</td>
              <td>100$</td>
              <td>
                <input type="number" defaultValue="1" onChange={handleEdit}/>
              </td>
              <td>$100$</td>
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
              <td>Giày nike</td>
              <td>100$</td>
              <td>
                <input type="number" defaultValue="1" onChange={handleEdit} />
              </td>
              <td>$100$</td>
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
              <td>Giày nike</td>
              <td>100$</td>
              <td>
                <input type="number" defaultValue="1" />
              </td>
              <td>$100$</td>
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
            <tbody>
              <tr>
                <th>Số tiền</th>
                <td>300$</td>
              </tr>
              <tr>
                <th>Tiền ship</th>
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
