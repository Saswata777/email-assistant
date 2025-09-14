// AnalyticsSection.jsx

'use client';

import React from "react";
import EmailsByPriorityChart from "./EmailsByPriorityChart";
import SLATracker from "./SLATracker";

const AnalyticsSection = () => {
  return (
    <div className="flex flex-col gap-4 p-4 h-[calc(100vh-80px)]">
      <EmailsByPriorityChart />
      <SLATracker />
    </div>
  );
};

export default AnalyticsSection;
