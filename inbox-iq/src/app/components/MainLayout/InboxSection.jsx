// "use client";
// import React, { useState, useEffect } from "react";
// import EmailCard from "./EmailCard"; // Import the new component
// import { fetchEmails, fetchStats } from "@/app/api";

// const InboxSection = () => {
//   const [emails, setEmails] = useState([]);
//   const [stats, setStats] = useState({
//     total: 0,
//     urgent: 0,
//     resolved: 0,
//     pending: 0,
//   });

//   useEffect(() => {
//     fetchEmails().then(setEmails).catch(console.error);
//     fetchStats().then(setStats).catch(console.error);
//   }, []);

//   return (
//     <div className="w-full h-[calc(100vh-80px)] overflow-y-auto p-4 space-y-4 bg-gray-50 dark:bg-gray-900">
//       {/* Inbox Overview Row */}
//       <div className="grid grid-cols-4 gap-4 mb-4">
//         <div className="p-4 bg-white rounded-lg shadow text-center">
//           <h3 className="text-lg font-semibold">Total Emails</h3>
//           <p className="text-xl text-blue-600">{stats.total}</p>
//         </div>
//         <div className="p-4 bg-white rounded-lg shadow text-center">
//           <h3 className="text-lg font-semibold">Urgent</h3>
//           <p className="text-xl text-red-600">{stats.urgent}</p>
//         </div>
//         <div className="p-4 bg-white rounded-lg shadow text-center">
//           <h3 className="text-lg font-semibold">Resolved</h3>
//           <p className="text-xl text-green-600">{stats.resolved}</p>
//         </div>
//         <div className="p-4 bg-white rounded-lg shadow text-center">
//           <h3 className="text-lg font-semibold">Pending</h3>
//           <p className="text-xl text-yellow-600">{stats.pending}</p>
//         </div>
//       </div>

//       {/* Email Cards */}
//       {emails.map((email) => (
//         <EmailCard key={email.id} email={email} />
//       ))}
//     </div>
//   );
// };

// export default InboxSection;

// InboxSection.jsx
"use client";
import React, { useState, useEffect, useCallback } from "react";
import EmailCard from "./EmailCard";
// NEW: Import the syncEmails function
import { fetchEmails, fetchStats, syncEmails } from "@/app/api";

const InboxSection = () => {
  const [emails, setEmails] = useState([]);
  const [stats, setStats] = useState({ /* ...initial stats... */ });
  // NEW: State to hold the user's ID
  const [userGoogleId, setUserGoogleId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // This function will load all necessary data
  const loadUserData = useCallback(async (userId) => {
    if (!userId) return;
    try {
      // Pass the user ID to the API calls
      const [emailsData, statsData] = await Promise.all([
        fetchEmails(userId),
        fetchStats(userId),
      ]);
      setEmails(emailsData);
      setStats(statsData);
    } catch (error) {
      console.error("Failed to load user data:", error);
      // Optional: Handle error, e.g., redirect to login if unauthorized
    }
  }, []);

  // On component mount, get the user ID from localStorage
  useEffect(() => {
    const userId = localStorage.getItem("currentUserGoogleId");
    if (userId) {
      setUserGoogleId(userId);
      loadUserData(userId);
    } else {
      console.log("No user is logged in.");
      // In a real app, you might redirect to a login page here
    }
  }, [loadUserData]);
  
  // NEW: Handler for the sync button
  const handleSync = async () => {
    if (!userGoogleId) return;
    setIsLoading(true);
    try {
      await syncEmails(userGoogleId);
      // After syncing, refresh the data on the screen
      await loadUserData(userGoogleId);
    } catch (error) {
      console.error("Failed to sync emails:", error);
      alert("Error syncing emails. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  // NEW: A simple refresh function to be passed to children if needed
  const refreshData = () => {
    if (userGoogleId) {
      loadUserData(userGoogleId);
    }
  };

  return (
    <div className="w-full h-[calc(100vh-80px)] overflow-y-auto p-4 space-y-4 bg-gray-50 dark:bg-gray-900">
      {/* NEW: Header with Sync Button */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Inbox</h2>
        <button
          onClick={handleSync}
          disabled={isLoading}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-blue-300"
        >
          {isLoading ? "Syncing..." : "Sync Emails"}
        </button>
      </div>

      {/* Inbox Overview Row (No changes here) */}
      <div className="grid grid-cols-4 gap-4 mb-4">
        <div className="p-4 bg-white rounded-lg shadow text-center">
           <h3 className="text-lg font-semibold">Total Emails</h3>
           <p className="text-xl text-blue-600">{stats.total}</p>
         </div>
         <div className="p-4 bg-white rounded-lg shadow text-center">
           <h3 className="text-lg font-semibold">Urgent</h3>
           <p className="text-xl text-red-600">{stats.urgent}</p>
         </div>
         <div className="p-4 bg-white rounded-lg shadow text-center">
           <h3 className="text-lg font-semibold">Resolved</h3>
           <p className="text-xl text-green-600">{stats.resolved}</p>
         </div>
         <div className="p-4 bg-white rounded-lg shadow text-center">
           <h3 className="text-lg font-semibold">Pending</h3>
           <p className="text-xl text-yellow-600">{stats.pending}</p>
         </div>
        {/* ...your stat cards... */}
      </div>

      {/* Email Cards */}
      {/* MODIFIED: Pass userGoogleId and refreshData function as props to each card */}
      {emails.map((email) => (
        <EmailCard 
          key={email.id} 
          email={email} 
          userGoogleId={userGoogleId}
          onReplySent={refreshData} // Pass the refresh function
        />
      ))}
    </div>
  );
};

export default InboxSection;