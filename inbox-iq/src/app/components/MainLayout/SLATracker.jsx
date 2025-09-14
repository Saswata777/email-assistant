import React from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

const data = [
  { day: "Mon", Resolved: 10, Pending: 5 },
  { day: "Tue", Resolved: 14, Pending: 4 },
  { day: "Wed", Resolved: 12, Pending: 6 },
  { day: "Thu", Resolved: 16, Pending: 3 },
  { day: "Fri", Resolved: 20, Pending: 2 },
];

const SLATracker = () => {
  return (
    <div className="bg-white dark:bg-gray-800 shadow rounded-2xl p-4">
      <h2 className="text-lg font-semibold mb-4">SLA Tracker</h2>
      <ResponsiveContainer width="100%" height={190}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="day" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="Resolved" stroke="#22c55e" strokeWidth={2} />
          <Line type="monotone" dataKey="Pending" stroke="#ef4444" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SLATracker;
