import Navigationbar from "./Navigationbar/Navbar";
import Productions from "./Productions/Products";
import Recommmened from "./Recommended/Recommmened";
import Sidebar from "./Sidebar/Sidebar";
import Trangchu from "./Pages/Trangchu";
import Cart from "./Pages/Cart";
import About from "./Pages/About";
import Shopping from "./Pages/Shopping";
import Blog from "./Pages/Blog";
import Contact from "./Pages/Contact";
import Details from "./Pages/Details";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
function App() {
  return (
    <>
      {/* <Trangchu /> */}
      {/* <Cart /> */}
      {/* <Shopping /> */}
      {/* <About /> */}
      {/* <Blog /> */}
      {/* <Contact /> */}
      <Details />
    </>
  );
}

export default App;
