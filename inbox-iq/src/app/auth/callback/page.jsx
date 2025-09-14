"use client";

import { useEffect } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';

const AuthCallbackPage = () => {
  const searchParams = useSearchParams();
  const router = useRouter();

  useEffect(() => {
    // 1. Get the user ID from the URL parameter
    const userGoogleId = searchParams.get('user_google_id');

    if (userGoogleId) {
      // 2. Save the ID to localStorage
      localStorage.setItem('currentUserGoogleId', userGoogleId);
      
      // 3. Redirect to the main dashboard page
      router.push('/'); // Or '/dashboard' or wherever your main page is
    } else {
      // Handle the case where the ID is missing, maybe redirect to an error page
      console.error("Authentication failed: No user ID provided in callback.");
      router.push('/login-error'); // Example error page
    }
    
    // We only want this effect to run once when the page loads.
  }, [searchParams, router]);

  // This page can just show a simple loading message while it processes.
  return (
    <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        backgroundColor: '#111827', // dark theme
        color: 'white',
        fontFamily: 'sans-serif'
    }}>
      <p>Please wait, logging you in...</p>
    </div>
  );
};

export default AuthCallbackPage;