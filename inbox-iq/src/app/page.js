// import Image from "next/image";
import Navbar from "./components/Navbar";
import InboxSection from "./components/MainLayout/InboxSection";
import AnalyticsSection from "./components/MainLayout/AnalyticsSection";

export default function Home() {
  return (
    <div>
      <Navbar />
      <div className="grid grid-cols-1 lg:grid-cols-10 gap-4 p-4">
        {/* Inbox takes 3 parts */}
        <div className="lg:col-span-7">
          <InboxSection />
        </div>

        {/* Analytics takes 2 parts */}
        <div className="lg:col-span-3">
          <AnalyticsSection />
        </div>
      </div>
    </div>
  );
}
