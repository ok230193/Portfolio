import React from 'react';
import logoImage from '../image/logo.PNG';

class Header extends React.Component {
  render() {
    return (
      <div className='header'>
        <div className='header-logo'>
          <img src={logoImage} />
        </div>
      </div>
    );
  }
}

export default Header;
