// "use client";
// import React from "react";
// import {
//   ResponsiveContainer,
//   PieChart,
//   Pie,
//   Cell,
//   Legend,
//   Tooltip,
// } from "recharts";

// import { fetchStats } from "@/app/api";
// import { useEffect, useState } from "react";


// const EmailsByPriorityChart = () => {
  
//   // const [emails, setEmails] = useState([]);
//   const [stats, setStats] = useState({
//       normal: 0,
//       urgent: 0,
//       resolved: 0,
//       pending: 0,
//     });
    
//     useEffect(() => {
//       fetchStats().then(setStats).catch(console.error);
//     }, []);
    

//     const data = [
//       { name: "Urgent", value: stats.urgent },
//       { name: "Normal", value: stats.normal },
//       { name: "Pending", value: stats.pending },
//       { name: "Resolved", value: stats.resolved },
//     ];
    
//     const COLORS = ["#ef4444", "#3b82f6", "#facc15", "#22c55e"];

//   return (
//     <div className="bg-white dark:bg-gray-800 shadow rounded-2xl p-4">
//       <h2 className="text-lg font-semibold mb-4">Emails by Priority</h2>
//       <ResponsiveContainer width="100%" height={190}>
//         <PieChart>
//           <Pie
//             data={data}
//             cx="50%"
//             cy="50%"
//             outerRadius={40}
//             dataKey="value"
//             label
//           >
//             {data.map((entry, index) => (
//               <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
//             ))}
//           </Pie>
//           <Tooltip />
//           <Legend />
//         </PieChart>
//       </ResponsiveContainer>
//     </div>
//   );
// };

// export default EmailsByPriorityChart;



// EmailsByPriorityChart.jsx
"use client";
import React, { useEffect, useState } from "react";
import { ResponsiveContainer, PieChart, Pie, Cell, Legend, Tooltip } from "recharts";
import { fetchStats } from "@/app/api";

const EmailsByPriorityChart = () => {
  const [stats, setStats] = useState({ /* ...initial stats... */ 
          normal: 0,
          urgent: 0,
          resolved: 0,
          pending: 0,
  });
  
  useEffect(() => {
    // On component mount, get the user ID from localStorage
    const userId = localStorage.getItem("currentUserGoogleId");
    
    if (userId) {
      // Pass the user ID to the API call
      fetchStats(userId).then(setStats).catch(console.error);
    }
  }, []); // Empty dependency array ensures this runs once on mount
  
  const data = [
    { name: "Urgent", value: stats.urgent },
    { name: "Normal", value: stats.normal },
    { name: "Pending", value: stats.pending },
    { name: "Resolved", value: stats.resolved },
  ];
  
  const COLORS = ["#ef4444", "#3b82f6", "#facc15", "#22c55e"];

  return (
    <div className="bg-white dark:bg-gray-800 shadow rounded-2xl p-4">
      <h2 className="text-lg font-semibold mb-4">Emails by Priority</h2>
      <ResponsiveContainer width="100%" height={190}>
        {/* ... your existing PieChart JSX ... */}
        <PieChart>
           <Pie
             data={data}
             cx="50%"
             cy="50%"
             outerRadius={40}
             dataKey="value"
             label
           >
             {data.map((entry, index) => (
               <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
             ))}
           </Pie>
           <Tooltip />
           <Legend />
         </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default EmailsByPriorityChart;