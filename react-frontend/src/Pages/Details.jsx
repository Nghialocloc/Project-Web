import "./style.css";
import Navigationbar from "../Navigationbar/Navbar";
import Productions from "../Productions/Products";
import Footer from "../Footer/Footer";
import Newsletter from "../Newsletter/Newsletter";
import { useParams } from "react-router-dom";
import data from "../db/data";
import f1 from "../img/products/af107white.webp";
import f2 from "../img/products/af107black.png";
import f3 from "../img/products/af107skincolor.webp";
import f4 from "../img/products/af107brown.png";
import f5 from "../img/products/af107womanblack.webp";
function Details() {
  const params = useParams();
  let productData = null;

  return (
    <>
      <Navigationbar />
      <section id="page-header">
        <h2>super value deals</h2>
        <p>Save more with coupons &up to 70% off! {params.id}</p>
      </section>
      {/* {data.map((data, index) => {
        return();})} */}
      <section id="prodetails" className="section-p1">
        <div className="single-pro-image">
          <img src={f1} width="100%" id="MainImg" alt="" />
          <div className="small-img-group">
            <div className="small-img-col">
              <img src={f2} width="100%" className="small-img" alt="" />
            </div>
            <div className="small-img-col">
              <img src={f3} width="100%" className="small-img" alt="" />
            </div>
            <div className="small-img-col">
              <img src={f4} width="100%" className="small-img" alt="" />
            </div>
            <div className="small-img-col">
              <img src={f5} width="100%" className="small-img" alt="" />
            </div>
          </div>
        </div>
        <div className="single-pro-details">
          <h6>Home/Shoes/Nike</h6>
          <h4>Nike Air Force 1'07 trắng</h4>
          <h2>2.000.000 dong</h2>
          <select name="" id="select-s">
            <option value="">Select Size</option>
            <option value="">40</option>
            <option value="">41</option>
            <option value="">42</option>
            <option value="">43</option>
            <option value="">44</option>
            <option value="">47</option>
          </select>
          <input type="number" value="1" />
          <button className="normal">Thêm vào giỏ hàng</button>
          <h4>Product Details</h4>
          <br />
          <span>Giới tính: NAM</span>
          <br />
          <span>Màu sắc: trắng</span>
          <br />
          <span>Chất liệu: Cao su</span>
          <br />
          <span>Năm sản xuất: 2024</span>
          <br />
          <br />
          <span>
            Ra mắt lần đầu tiên vào năm 1982, AF-1 là đôi giày bóng rổ đầu tiên
            có Nike Air, tạo nên một cuộc cách mạng trong môn thể thao này đồng
            thời nhanh chóng thu hút được sự chú ý trên toàn thế giới. Ngày nay,
            Air Force 1 vẫn giữ nguyên nguồn gốc của nó với lớp đệm mềm mại và
            đàn hồi đã làm thay đổi lịch sử giày thể thao.
          </span>
        </div>
      </section>

      <Productions />
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
export default Details;
