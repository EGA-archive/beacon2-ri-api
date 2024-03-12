import './SignInOptions.css'
import { NavLink } from 'react-router-dom'

function SignInOptions () {
  return (
    <div className='container'>
      <div className='screen'>
        <div className='screen__content'>
          <form className='login2'>
            <div className='login__field2'>
              <NavLink
                exact
                to='/sign-in'
                className={({ isActive }) =>
                  isActive ? 'Sign-in2' : 'Sign-inLS'
                }
              >
                <img
                  className='ls-login-image'
                  src='/../ls-login.png'
                  alt='ls-login-image'
                />
              </NavLink>
            </div>
      
            <div className='login__field2'>
              <NavLink
                exact
                to='/sign-in-noLS'
                className={({ isActive }) =>
                  isActive ? 'Sign-in2' : 'Sign-inNoLs'
                }
              >
                <h6>Beacon Network IDP Login</h6>
              </NavLink>
            </div>
          </form>
        </div>
        <div className='screen__background'>
          <span className='screen__background__shape screen__background__shape6'></span>
          <span className='screen__background__shape screen__background__shape2'></span>
          <span className='screen__background__shape screen__background__shape5'></span>
        </div>
      </div>
    </div>
  )
}
export default SignInOptions
