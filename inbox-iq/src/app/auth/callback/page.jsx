'use client';

import { useEffect, Suspense } from 'react'; // Import Suspense from React
import { useSearchParams, useRouter } from 'next/navigation';

// Component that contains the actual logic using the hooks
function CallbackProcessor() {
  const searchParams = useSearchParams();
  const router = useRouter();

  useEffect(() => {
    // 1. Get the user ID from the URL parameter
    const userGoogleId = searchParams.get('user_google_id');

    if (userGoogleId) {
      // 2. Save the ID to localStorage
      localStorage.setItem('currentUserGoogleId', userGoogleId);
      
      // 3. Redirect to the main dashboard page
      router.push('/'); // Or '/dashboard'
    } else {
      // Handle the case where the ID is missing
      console.error("Authentication failed: No user ID provided in callback.");
      router.push('/login-error'); // Example error page
    }
  }, [searchParams, router]);

  // This component doesn't need to render anything itself, it just handles logic
  return null;
}

// The main page component that will be rendered
const AuthCallbackPage = () => {
  return (
    // Your loading UI
    <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        backgroundColor: '#111827',
        color: 'white',
        fontFamily: 'sans-serif'
    }}>
      <p>Please wait, logging you in...</p>
      
      {/* Wrap the logic component in a Suspense boundary */}
      <Suspense fallback={null}>
        <CallbackProcessor />
      </Suspense>
    </div>
  );
};

export default AuthCallbackPage;