import {Link, NavLink} from 'react-router-dom'

import { AiOutlineFileSearch } from "react-icons/ai";
import "./Header.scss";

const Header = () => {
    return (
        <header>
            <h1 className="logo"><Link to="/"><AiOutlineFileSearch className='icon'/></Link></h1>
            {/* 서치바 넣을 곳 */}
            {/* <nav>
                <ul>
                    <li><Link to="./Login">Login</Link></li>
                    <li><Link to="./Join">Join</Link></li>
                </ul>
            </nav> */}
        </header>
    )
}
export default Header;