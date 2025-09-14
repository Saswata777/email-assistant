// const API_URL = "http://127.0.0.1:8000"; // FastAPI backend

// export async function fetchEmails() {
//   const res = await fetch(`${API_URL}/emails`);
//   if (!res.ok) throw new Error("Failed to fetch emails");
//   return res.json();
// }

// export async function addEmail(emailData) {
//   const res = await fetch(`${API_URL}/emails`, {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify(emailData),
//   });
//   if (!res.ok) throw new Error("Failed to add email");
//   return res.json();
// }

// export async function fetchStats() {
//   try {
//     const res = await fetch(`${API_URL}/stats`);
//     if (!res.ok) throw new Error("Failed to fetch stats");
//     const data = await res.json();

//     // ✅ Ensure defaults if backend doesn't return something
//     return {
//       total: data.total ?? 0,
//       urgent: data.urgent ?? 0,
//       resolved: data.resolved ?? 0,
//       pending: data.pending ?? 0,
//       normal: data.normal ?? 0,
//     };
//   } catch (err) {
//     console.error("Error fetching stats:", err);
//     // ✅ Return fallback stats to avoid breaking UI
//     return { total: 0, urgent: 0, resolved: 0, pending: 0, normal: 0};
//   }
// }


// // ✅ NEW: Send reply to backend
// export async function sendReply(emailId, replyText) {
//   const res = await fetch(`${API_URL}/send-reply`, {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({
//       email_id: emailId,
//       reply: replyText,
//     }),
//   });

//   if (!res.ok) {
//     const err = await res.json().catch(() => ({}));
//     throw new Error(err.detail || "Failed to send reply");
//   }

//   return res.json();
// }


// The backend is now running on port 8000
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

/**
 * Fetches emails for a specific user.
 * @param {string} userGoogleId - The Google ID of the logged-in user.
 */
export async function fetchEmails(userGoogleId) {
  if (!userGoogleId) throw new Error("User ID is required to fetch emails.");
  
  // The endpoint now requires the user's ID
  const res = await fetch(`${API_URL}/emails/${userGoogleId}`);
  if (!res.ok) throw new Error("Failed to fetch emails");
  return res.json();
}

/**
 * Triggers a server-side sync to fetch the latest emails from Gmail for a specific user.
 * This replaces the old addEmail and the background scheduler.
 * @param {string} userGoogleId - The Google ID of the logged-in user.
 */
export async function syncEmails(userGoogleId) {
  if (!userGoogleId) throw new Error("User ID is required to sync emails.");

  const res = await fetch(`${API_URL}/sync-emails/${userGoogleId}`, {
    method: "POST", // This is a POST request as it initiates an action
  });
  if (!res.ok) throw new Error("Failed to sync emails");
  return res.json();
}

/**
 * Fetches statistics for a specific user.
 * @param {string} userGoogleId - The Google ID of the logged-in user.
 */
export async function fetchStats(userGoogleId) {
  if (!userGoogleId) throw new Error("User ID is required to fetch stats.");
  
  try {
    // The endpoint now requires the user's ID
    const res = await fetch(`${API_URL}/stats/${userGoogleId}`);
    if (!res.ok) throw new Error("Failed to fetch stats");
    const data = await res.json();

    return {
      total: data.total ?? 0,
      urgent: data.urgent ?? 0,
      resolved: data.resolved ?? 0,
      pending: data.pending ?? 0,
      normal: data.normal ?? 0,
    };
  } catch (err) {
    console.error("Error fetching stats:", err);
    return { total: 0, urgent: 0, resolved: 0, pending: 0, normal: 0 };
  }
}

/**
 * Sends a reply for a specific email.
 * @param {string} userGoogleId - The Google ID of the logged-in user.
 * @param {number} emailId - The database ID of the email being replied to.
 * @param {string} replyText - The content of the reply.
 */
export async function sendReply(userGoogleId, emailId, replyText) {
  if (!userGoogleId) throw new Error("User ID is required to send a reply.");

  const res = await fetch(`${API_URL}/send-reply`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_google_id: userGoogleId, // The backend now requires the user's ID in the body
      email_id: emailId,
      reply: replyText,
    }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to send reply");
  }

  return res.json();
}