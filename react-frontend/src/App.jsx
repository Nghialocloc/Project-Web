import Navigationbar from "./Navigationbar/Navbar";
import Productions from "./Productions/Products";
import Recommmened from "./Recommended/Recommmened";
import Sidebar from "./Sidebar/Sidebar";
import Trangchu from "./Pages/Trangchu";
import Cart from "./Pages/Cart";
import About from "./Pages/About";
import Chinhsach from "./Pages/Chinhsach";
import Chinhsachdoitra from "./Pages/Chinhsachdoitra";
import Chinhsachvanchuyen from "./Pages/Chinhsachvanchuyen";
import Chinhsachthanhtoan from "./Pages/Chinhsachthanhtoan";
import Shopping from "./Pages/Shopping";
import Blog from "./Pages/Blog";
import Contact from "./Pages/Contact";
import Details from "./Pages/Details";
import Dashboard from "./Admin/DashBoard";
import { Fragment } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useParams,
} from "react-router-dom";
import LoginPage from "./Pages/LoginPage";
import SignUp from "./Pages/SignUp";
import data from "./db/data";

function App() {
  // const [count, setCount] = useState(0)
  return (
    <>
      {/* <Trangchu /> */}
      {/* <Cart /> */}
      {/* <Shopping /> */}
      {/* <About /> */}
      {/* <Blog /> */}
      {/* <Contact /> */}
      {/* <Details /> */}
      {/* <Dashboard /> */}

      <Router>
        <Fragment>
          <Routes>
            <Route path="" element={<Trangchu />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/dashboard" element={<Dashboard />}></Route>
            <Route path="/trangchu" element={<Trangchu />} />
            <Route path="/shoping" element={<Shopping />} />
            <Route path="/blog" element={<Blog />} />
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="/cart" element={<Cart />} />
            <Route path="/detail" element={<Details />} />
            <Route path="/chinhsach" element={<Chinhsach />} />
            <Route
              path="/chinhsachthanhtoan"
              element={<Chinhsachthanhtoan />}
            />
            <Route
              path="/chinhsachvanchuyen"
              element={<Chinhsachvanchuyen />}
            />
            <Route path="/chinhsachdoitra" element={<Chinhsachdoitra />} />
          </Routes>
        </Fragment>
      </Router>
    </>
  );
}

export default App;
