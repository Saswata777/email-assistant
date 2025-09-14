// // EmailCard.js (a new component file)
// "use client";
// import React, { useState } from "react";
// import { sendReply } from "@/app/api";

// const EmailCard = ({ email }) => {
//   // State is now local to each card, which is correct!
//   const [isEditing, setIsEditing] = useState(false);
//   const [reply, setReply] = useState(email.ai_reply);
//   const [isApproved, setIsApproved] = useState(false);

//   const handleSave = () => {
//     // Here you would also likely make an API call to save the new reply
//     console.log("Saving reply for email:", email.id, "New reply:", reply);
//     setIsEditing(false);
//   };

//   const handleCancel = () => {
//     setReply(email.ai_reply); // Reset to the original AI reply
//     setIsEditing(false);
//   };

//   const handleApproveSend = async () => {
//   try {
//     const data = await sendReply(email.id, reply);
//     if (data.status === "success") {
//       setIsApproved(true);
//       if (email) {
//         email.status = "sent";
//       }
//     } else {
//       alert("Failed to send: " + data.message);
//     }
//   } catch (err) {
//     console.error("Error sending email:", err);
//     alert("Error: " + err.message);
//   }
// };

//   return (
//     <div
//       className="w-full p-4 bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-gray-800 dark:border-gray-700"
//     >
//       {/* Header */}
//       <div className="flex justify-between items-center mb-2">
//         <div className="flex justify-items-start items-center mb-2">
//           <span
//             className={`text-xs font-semibold px-2 py-1 rounded ${
//               email.priority === "high" || email.priority === "URGENT"
//                 ? "bg-red-100 text-red-600"
//                 : "bg-green-100 text-green-600"
//             }`}
//           >
//             {email.priority === "high" || email.priority === "URGENT"? "URGENT" : "Normal"}
//           </span>

//           <span
//             className={`text-xs font-semibold px-2 py-1 rounded ms-3 ${
//               email.sentiment === "negative"
//                 ? "bg-red-100 text-red-600": email.sentiment === "neutral"
//                 ? "bg-yellow-100 text-yellow-600"
//                 : "bg-green-100 text-green-600"
//             }`}
//           >
//             {email.sentiment === "negative"? "Negative" : email.sentiment === "neutral"? "Neutral" : "Positive"}
//           </span>
//         </div>
//           <span className="text-xs text-gray-500 ms-5">{email.received_at}</span>
//       </div>


//       {/* Subject */}
//       <h5 className="text-lg font-bold text-gray-900 dark:text-white">
//         {email.subject}
//       </h5>

//       {/* Metadata */}
//       <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">
//         <span className="font-semibold">From:</span> {email.sender}
//       </p>

//       {/* Snippet */}
//       <p className="text-gray-600 dark:text-gray-300 mb-3">
//         {email.body}
//       </p>

//       {/* AI Suggested Reply */}
//       <div className="bg-gray-50 dark:bg-gray-700 p-3 rounded-md mb-3">
//         {isEditing ? (
//           <textarea
//             className="w-full p-2 border rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
//             value={reply}
//             onChange={(e) => setReply(e.target.value)}
//             rows={4}
//           />
//         ) : (
//           <p className="text-sm text-gray-700 dark:text-gray-200">
//             {reply}
//           </p>
//         )}
//       </div>

//       {/* Action Buttons */}
//       <div className="flex flex-wrap gap-2">
//         {isEditing ? (
//           <>
//             <button
//               onClick={handleSave}
//               className="px-3 py-1 bg-blue-500 hover:bg-blue-600 text-white rounded"
//             >
//               Save
//             </button>
//             <button
//               onClick={handleCancel}
//               className="px-3 py-1 bg-gray-300 hover:bg-gray-400 text-gray-800 rounded"
//             >
//               Cancel
//             </button>
//           </>
//         ) : (
//           <button
//             onClick={() => setIsEditing(true)}
//             className="px-3 py-1 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded"
//           >
//             Edit Reply
//           </button>
//         )}

//         <button
//           onClick={handleApproveSend}
//           disabled={isApproved}
//           className={`px-3 py-1 rounded ${
//             email.status === "sent" || isApproved
//               ? "bg-green-500 text-white"
//               : "bg-blue-600 hover:bg-blue-700 text-white"
//           }`}
//         >
//           {isApproved ? "Approved" : "Approve & Send"}
//         </button>
        
//       </div>
//     </div>
//   );
// };

// export default EmailCard;



// EmailCard.jsx
"use client";
import React, { useState } from "react";
import { sendReply } from "@/app/api";

// MODIFIED: Destructure userGoogleId and onReplySent from props
const EmailCard = ({ email, userGoogleId, onReplySent }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [reply, setReply] = useState(email.ai_reply);
  const [isSending, setIsSending] = useState(false);

  const handleApproveSend = async () => {
    // Check if user ID is available
    if (!userGoogleId) {
      alert("Could not send reply: User is not logged in.");
      return;
    }

    setIsSending(true);
    try {
      // MODIFIED: Pass userGoogleId as the first argument
      const data = await sendReply(userGoogleId, email.id, reply);
      
      if (data.status === "success") {
        // Instead of manually updating state, we tell the parent to refresh all data
        // This ensures stats (like 'resolved') are also updated
        if (onReplySent) {
          onReplySent();
        }
      } else {
        alert("Failed to send: " + data.message);
      }
    } catch (err) {
      console.error("Error sending email:", err);
      alert("Error: " + err.message);
    } finally {
      setIsSending(false);
    }
  };
  
  // ... other handlers like handleSave, handleCancel ...

   const handleSave = () => {
     // Here you would also likely make an API call to save the new reply
     console.log("Saving reply for email:", email.id, "New reply:", reply);
     setIsEditing(false);
   };

   const handleCancel = () => {
     setReply(email.ai_reply); // Reset to the original AI reply
     setIsEditing(false);
   };


  return (
    <div className="w-full p-4 bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-gray-800 dark:border-gray-700">
      {/* ... your existing JSX ... */}

      {/* Header */}
       <div className="flex justify-between items-center mb-2">
         <div className="flex justify-items-start items-center mb-2">
           <span
             className={`text-xs font-semibold px-2 py-1 rounded ${
               email.priority === "high" || email.priority === "URGENT"
                 ? "bg-red-100 text-red-600"
                 : "bg-green-100 text-green-600"
             }`}
           >
             {email.priority === "high" || email.priority === "URGENT"? "URGENT" : "Normal"}
           </span>

           <span
             className={`text-xs font-semibold px-2 py-1 rounded ms-3 ${
               email.sentiment === "negative"
                 ? "bg-red-100 text-red-600": email.sentiment === "neutral"
                 ? "bg-yellow-100 text-yellow-600"
                 : "bg-green-100 text-green-600"
             }`}
           >
             {email.sentiment === "negative"? "Negative" : email.sentiment === "neutral"? "Neutral" : "Positive"}
           </span>
         </div>
           <span className="text-xs text-gray-500 ms-5">{email.received_at}</span>
       </div>


       {/* Subject */}
       <h5 className="text-lg font-bold text-gray-900 dark:text-white">
         {email.subject}
       </h5>

       {/* Metadata */}
       <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">
         <span className="font-semibold">From:</span> {email.sender}
       </p>

       {/* Snippet */}
       <p className="text-gray-600 dark:text-gray-300 mb-3">
         {email.body}
       </p>

       {/* AI Suggested Reply */}
       <div className="bg-gray-50 dark:bg-gray-700 p-3 rounded-md mb-3">
         {isEditing ? (
           <textarea
             className="w-full p-2 border rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
             value={reply}
             onChange={(e) => setReply(e.target.value)}
             rows={4}
           />
         ) : (
           <p className="text-sm text-gray-700 dark:text-gray-200">
             {reply}
           </p>
         )}
       </div>
      
      {/* Action Buttons */}
      <div className="flex flex-wrap gap-2">
        {/* ... edit/save/cancel buttons ... */}
        {isEditing ? (
           <>
             <button
               onClick={handleSave}
               className="px-3 py-1 bg-blue-500 hover:bg-blue-600 text-white rounded"
             >
               Save
             </button>
             <button
               onClick={handleCancel}
               className="px-3 py-1 bg-gray-300 hover:bg-gray-400 text-gray-800 rounded"
             >
               Cancel
             </button>
           </>
         ) : (
           <button
             onClick={() => setIsEditing(true)}
             className="px-3 py-1 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded"
           >
             Edit Reply
           </button>
         )}
        
        <button
          onClick={handleApproveSend}
          disabled={isSending || email.status === "sent"}
          className={`px-3 py-1 rounded ${
            email.status === "sent"
              ? "bg-green-500 text-white cursor-not-allowed"
              : isSending
              ? "bg-blue-300 text-white cursor-wait"
              : "bg-blue-600 hover:bg-blue-700 text-white"
          }`}
        >
          {email.status === "sent" ? "Sent" : isSending ? "Sending..." : "Approve & Send"}
        </button>
      </div>
    </div>
  );
};

export default EmailCard;