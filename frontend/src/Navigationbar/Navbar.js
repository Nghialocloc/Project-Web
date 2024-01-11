import { FiHeart } from "react-icons/fi";
import { AiOutlineShoppingCart, AiOutlineUserAdd } from "react-icons/ai";
import "./Navbar.css";

const active = () => {
  return "active";
};
var defaultA = true;
var defaultB = false;
const defaultActive = (activate) => {
  if (activate == true) {
    return "active";
  } else {
    return "0";
  }
};

function navBar() {
  return (
    <nav>
      <script
        src="https://kit.fontawesome.com/1147679ae7.js"
        crossorigin="anonymous"
      />
      <link
        rel="stylesheet"
        href="https://use.fontawesome.com/releases/v5.15.4/css/all.css"
      />
      {/* <div className="profile-container">
        <a href="#">
          <FiHeart className="nav-icons" />
        </a>
        <a href="#">
          <AiOutlineShoppingCart className="nav-icons" />
        </a>
        <a href="#">
          <AiOutlineUserAdd className="nav-icons" />
        </a>
      </div> */}
      <section id="header">
        <a href="#">
          <img src="#" class="logo" />
        </a>
        <div className="nav-container">
          <li>
            <input
              type="text"
              className="search-input"
              placeholder="Nhập tên/hãng giày cần tìm."
            />
          </li>
        </div>
        <div>
          <ul id="navbar">
            <li>
              <a className="active" href="trangchu.html">
                Home
              </a>
            </li>
            <li>
              <a href="shoping.html">Shopping</a>
            </li>
            <li>
              <a href="blog.html">Blog</a>
            </li>
            <li>
              <a href="about.html">About</a>
            </li>
            <li>
              <a href="contact.html">Contact</a>
            </li>
            <li>
              <a href="cart.html">
                <i class="fa fa-shopping-bag"></i>
              </a>
            </li>
            <li>
              <a href="nguoidung.html" onclick="checkTaiKhoan()">
                <i class="fa fa-user"></i>
              </a>
            </li>
          </ul>
        </div>
      </section>
      {/*icons*/}
    </nav>
  );
}

export default navBar;
