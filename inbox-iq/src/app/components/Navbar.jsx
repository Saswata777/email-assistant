// 'use client';
// import React, { useState } from 'react';

// const Navbar = () => {
//   const [isOpen, setIsOpen] = useState(false);

//   const toggleMenu = () => {
//     setIsOpen(!isOpen);
//   };

//   return (
//     <nav className="bg-blue-700 border-gray-200 dark:bg-gray-900">
//       <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
//         {/* Logo */}
//         <a
//           href="#"
//           className="flex items-center space-x-2 text-white font-semibold text-xl"
//         >
//           <span className="text-lg md:text-xl">Inbox IQ </span>
//         </a>

//         {/* Mobile Menu Button */}
//         <button
//           onClick={toggleMenu}
//           type="button"
//           className="inline-flex items-center p-2 w-10 h-10 justify-center text-sm 
//             text-white rounded-lg md:hidden hover:bg-blue-600 focus:outline-none 
//             focus:ring-2 focus:ring-blue-300"
//           aria-controls="navbar-menu"
//           aria-expanded={isOpen}
//         >
//           <span className="sr-only">Open main menu</span>
//           <svg
//             className="w-6 h-6"
//             aria-hidden="true"
//             xmlns="http://www.w3.org/2000/svg"
//             fill="none"
//             viewBox="0 0 17 14"
//           >
//             <path
//               stroke="currentColor"
//               strokeLinecap="round"
//               strokeLinejoin="round"
//               strokeWidth="2"
//               d="M1 1h15M1 7h15M1 13h15"
//             />
//           </svg>
//         </button>

//         {/* Nav Links */}
//         <div
//           className={`w-full md:flex md:w-auto ${isOpen ? 'block' : 'hidden'}`}
//           id="navbar-menu"
//         >
//           <ul
//             className="flex flex-col p-4 md:p-0 mt-4 font-medium 
//               rounded-lg bg-blue-600 md:bg-transparent md:space-x-8 md:flex-row md:mt-0"
//           >
//             <li>
//               <a
//                 href="#"
//                 className="block py-2 px-3 text-white hover:text-gray-200"
//               >
//                 Logout
//               </a>
//             </li>
//           </ul>
//         </div>
//       </div>
//     </nav>
//   );
// };

// export default Navbar;


'use client';
import React, { useState, useEffect } from 'react';

// For consistency, you might want to import this from your api.js file
const API_URL = "http://127.0.0.1:8000";

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  // NEW: State to track if the user is logged in or not.
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // NEW: Check the user's login status when the component first loads.
  useEffect(() => {
    const userId = localStorage.getItem('currentUserGoogleId');
    if (userId) {
      setIsLoggedIn(true);
    }
  }, []); // The empty array ensures this runs only once on mount.

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  // NEW: A function to handle logging out.
  const handleLogout = () => {
    // 1. Remove the user's ID from storage
    localStorage.removeItem('currentUserGoogleId');
    // 2. Update the state to reflect the change
    setIsLoggedIn(false);
    // 3. Redirect to the home/login page to refresh the app state
    window.location.href = '/';
  };

  return (
    <nav className="bg-blue-700 border-gray-200 dark:bg-gray-900">
      <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
        {/* Logo */}
        <a
          href="/" // Link to the home page
          className="flex items-center space-x-2 text-white font-semibold text-xl"
        >
          <span className="text-lg md:text-xl">Inbox IQ </span>
        </a>

        {/* Mobile Menu Button */}
        <button
          onClick={toggleMenu}
          type="button"
          className="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-white rounded-lg md:hidden hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300"
          aria-controls="navbar-menu"
          aria-expanded={isOpen}
        >
          <span className="sr-only">Open main menu</span>
          <svg
            className="w-6 h-6"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 17 14"
          >
            <path
              stroke="currentColor"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M1 1h15M1 7h15M1 13h15"
            />
          </svg>
        </button>

        {/* Nav Links */}
        <div
          className={`w-full md:flex md:w-auto ${isOpen ? 'block' : 'hidden'}`}
          id="navbar-menu"
        >
          <ul
            className="flex flex-col p-4 md:p-0 mt-4 font-medium rounded-lg bg-blue-600 md:bg-transparent md:space-x-8 md:flex-row md:mt-0 items-center"
          >
            {/* NEW: Conditionally render Login or Logout button */}
            {isLoggedIn ? (
              // If user IS logged in, show the Logout button
              <li>
                <button
                  onClick={handleLogout}
                  className="block py-2 px-3 text-white hover:text-gray-200"
                >
                  Logout
                </button>
              </li>
            ) : (
              // If user is NOT logged in, show the Login button
              <li>
                <a
                  href={`${API_URL}/login`} // This link kicks off the entire Google login flow
                  className="block py-2 px-3 text-white bg-green-500 rounded hover:bg-green-600"
                >
                  Login with Google
                </a>
              </li>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;