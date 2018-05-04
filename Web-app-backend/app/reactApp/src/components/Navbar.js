import React from 'react'

const Navbar = props => {
    const listItems = props.items.map((d) => <a className="nav-item nav-link" href={d.link}>{d.name}</a>)
    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            {listItems}
        </nav>
    )
}
// <li>
//     {props.data}
// </li>
export default Navbar
