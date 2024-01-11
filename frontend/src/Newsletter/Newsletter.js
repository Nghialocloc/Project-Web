import "./Newsletter.css";
function Newsletter() {
  return (
    <section id="newsletter" class="section-p1 section-m1">
      <div class="newstext">
        <h4>Sign Up for Newsletter</h4>
        <p>
          Get email update about our <span>special offers</span>
        </p>
      </div>
      <div class="form">
        <input type="text" placeholder="Enter your email address" />
        <button class="normal">Sign Up</button>
      </div>
    </section>
  );
}
export default Newsletter;
