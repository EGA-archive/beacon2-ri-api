import React from 'react';
import { useAuth } from 'oidc-react';

const LoggedIn = () => {
  const auth = useAuth();
  if (auth && auth.userData) {
    return (
      <div>
        <strong>Logged in! 🎉</strong><br />
        <button onClick={() => auth.signOut()}>Log out!</button>
      </div>
    );
  }
  return <div>Not logged in! Try to refresh to be redirected to LifeScience.</div>;
};

export default LoggedIn;