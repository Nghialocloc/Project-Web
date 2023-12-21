function addHeader() {
    const imgPosition = document.querySelectorAll("img")
    // console.log(imgPosition)

    const header = document.querySelector("header")
    window.addEventListener("scroll", function(){
        x=window.scrollY
        if(x>0){
            header.classList.add("sticky")
        }
        else{
            header.classList.remove("sticky")
        }
    });
    document.write(`
    <div class="logo">
        <a href="trangchu.html"><img src="img/logo.png"></a>
    </div>
        <div class="menu">
            <li><a href="">NỮ</a></li>
            <li><a href="">NAM</a></li>
            <li><a href="">TRẺ EM</a></li>
            <li><a href="">SALE</a></li>
            <li><a href="">KHẨU TRANG</a></li>
            <li><a href="">BST</a></li>
            <li><a href="">THÔNG TIN</a></li>
        </div>
        <div class="others">
            <li><input placeholder="Tìm kiếm" type="text"> <i class="fas fa-search"></i></li>
            <li> <a class="fa fa-paw" href=""></a></li>
            <li> <a class="fa fa-user" href=""></a></li>
            <li> <a class="fa fa-shopping-bag" href=""></a></li>
        </div>`);
    }