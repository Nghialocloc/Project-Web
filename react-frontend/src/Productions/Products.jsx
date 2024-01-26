import "./Products.css";
import data from "../db/data";
function Products() {
  return (
    <>
      <script
        src="https://kit.fontawesome.com/1147679ae7.jsx"
        crossOrigin="anonymous"
      />
      <link
        rel="stylesheet"
        href="https://use.fontawesome.com/releases/v5.15.4/css/all.css"
      />
      <section id="product1" className="section-p1">
        <h2>Featured Products</h2>
        <p>Winter Collection New Model</p>
        <div className="pro-container">
          {data.map((data, index) => {
            if (data.feature == true) {
              return (
                <div className="pro" key={index}>
                  {/* <data feature={true} /> */}
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
            }
          })}
        </div>
      </section>
      {/* <div className="pro">
            <img src="img/products/f1.jpg" />
            <div className="des">
              <span>adidas</span>
              <h5>Cartoon Astronaut</h5>
              <div className="star">
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
              </div>
              <h4>$78</h4>
            </div>
            <a href="#">
              <i className="fa fa-shopping-cart cart"></i>
            </a>
          </div>
          <div className="pro">
            <img src="img/products/f1.jpg" />
            <div className="des">
              <span>adidas</span>
              <h5>Cartoon Astronaut</h5>
              <div className="star">
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
              </div>
              <h4>$78</h4>
            </div>
            <a href="#">
              <i className="fa fa-shopping-cart cart"></i>
            </a>
          </div>
          <div className="pro">
            <img src="img/products/f1.jpg" />
            <div className="des">
              <span>adidas</span>
              <h5>Cartoon Astronaut</h5>
              <div className="star">
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
              </div>
              <h4>$78</h4>
            </div>
            <a href="#">
              <i className="fa fa-shopping-cart cart"></i>
            </a>
          </div>
          <div className="pro">
            <img src="img/products/f1.jpg" />
            <div className="des">
              <span>adidas</span>
              <h5>Cartoon Astronaut</h5>
              <div className="star">
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
              </div>
              <h4>$78</h4>
            </div>
            <a href="#">
              <i className="fa fa-shopping-cart cart"></i>
            </a>
          </div>
          <div className="pro">
            <img src="img/products/f1.jpg" />
            <div className="des">
              <span>adidas</span>
              <h5>Cartoon Astronaut</h5>
              <div className="star">
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
              </div>
              <h4>$78</h4>
            </div>
            <a href="#">
              <i className="fa fa-shopping-cart cart"></i>
            </a>
          </div>
          <div className="pro">
            <img src="img/products/f1.jpg" />
            <div className="des">
              <span>adidas</span>
              <h5>Cartoon Astronaut</h5>
              <div className="star">
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
              </div>
              <h4>$78</h4>
            </div>
            <a href="#">
              <i className="fa fa-shopping-cart cart"></i>
            </a>
          </div>
          <div className="pro">
            <img src="img/products/f1.jpg" />
            <div className="des">
              <span>adidas</span>
              <h5>Cartoon Astronaut</h5>
              <div className="star">
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
              </div>
              <h4>$78</h4>
            </div>
            <a href="#">
              <i className="fa fa-shopping-cart cart"></i>
            </a>
          </div>
          <div className="pro">
            <img src="img/products/f1.jpg" />
            <div className="des">
              <span>adidas</span>
              <h5>Cartoon Astronaut</h5>
              <div className="star">
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
              </div>
              <h4>$78</h4>
            </div>
            <a href="#">
              <i className="fa fa-shopping-cart cart"></i>
            </a>
          </div>
          <div className="pro">
            <img src="img/products/f1.jpg" />
            <div className="des">
              <span>adidas</span>
              <h5>Cartoon Astronaut</h5>
              <div className="star">
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
              </div>
              <h4>$78</h4>
            </div>
            <a href="#">
              <i className="fa fa-shopping-cart cart"></i>
            </a>
          </div>
          <div className="pro">
            <img src="img/products/f1.jpg" />
            <div className="des">
              <span>adidas</span>
              <h5>Cartoon Astronaut</h5>
              <div className="star">
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
                <i className="far fa-star"></i>
              </div>
              <h4>$78</h4>
            </div>
            <a href="#">
              <i className="fa fa-shopping-cart cart"></i>
            </a>
          </div>
        </div>
      </section> */}
    </>
  );
}

export default Products;
