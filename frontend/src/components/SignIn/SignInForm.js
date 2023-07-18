import './SignInForm.css'

import LoggedIn from './LoggedIn';
import { useAuth } from 'oidc-react';

export default function SignInForm() {


    const auth = useAuth();
    console.log(auth)

    const isAuthenticated = auth.userData?.id_token ? true : false;
    if(!isAuthenticated){
    auth.userManager?.signinRedirect();}

    return (
        <div className="App">
          <header className="App-header">
            <p>OIDC React</p>
            <LoggedIn />
          </header>
        </div>

    )

}
