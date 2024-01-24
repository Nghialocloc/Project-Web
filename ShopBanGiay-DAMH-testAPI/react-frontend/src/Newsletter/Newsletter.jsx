import "./Newsletter.css";
function Newsletter() {
  return (
    <section id="newsletter" className="section-p1 section-m1">
      <div className="newstext">
        <h4>Sign Up for Newsletter</h4>
        <p>
          Get email update about our <span>special offers</span>
        </p>
      </div>
      <div className="form">
        <input type="text" placeholder="Enter your email address" />
        <button className="normal">Sign Up</button>
      </div>
    </section>
  );
}
export default Newsletter;
