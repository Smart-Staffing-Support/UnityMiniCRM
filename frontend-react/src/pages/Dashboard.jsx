import { useState, useEffect, useCallback } from "react";
import {
  HiOutlineUsers,
  HiOutlineBuildingOffice2,
  HiOutlineClipboardDocumentList,
  HiOutlineChartBar,
  HiOutlineBolt,
  HiOutlineUserPlus,
  HiOutlineBuildingOffice,
  HiOutlinePlus,
} from "react-icons/hi2";
import { AiOutlineLoading3Quarters } from "react-icons/ai";
import { crmService } from "../services/api";
import AddContactModal from "../components/AddContactModal";
import AddCompanyModal from "../components/AddCompanyModal";
import AddDealModal from "../components/AddDealModal";

const formatCurrency = (value) =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value || 0);

const stage_colors = {
  lead: { chip: "bg-slate-200 text-slate-700", bar: "bg-slate-500" },
  qualified: { chip: "bg-blue-100 text-blue-700", bar: "bg-blue-500" },
  proposal: { chip: "bg-purple-100 text-purple-700", bar: "bg-purple-500" },
  negotiation: { chip: "bg-orange-100 text-orange-700", bar: "bg-orange-500" },
  won: { chip: "bg-green-100 text-green-700", bar: "bg-green-500" },
  lost: { chip: "bg-red-100 text-red-700", bar: "bg-red-500" },
};

function StatCard({
  label,
  value,
  sub,
  subColor,
  iconBg,
  iconColor,
  Icon,
  onClick,
}) {
  return (
    <button
      onClick={onClick}
      className="w-full text-left bg-white rounded-xl shadow-md p-5 flex items-center justify-between border-l-4 border-l-transparent hover:border-l-blue-600 hover:-translate-y-1 transition-all duration-300 cursor-pointer"
    >
      <div className="flex-1 min-w-0">
        <p className="text-xs font-semibold uppercase tracking-widest text-gray-500 mb-1">
          {label}
        </p>
        <h2 className="text-3xl font-bold text-[#1a237e] mb-1 leading-none">
          {value}
        </h2>
        <p className={`text-xs font-medium ${subColor || "text-gray-400"}`}>
          {sub}
        </p>
      </div>
      <div
        className={`w-16 h-16 rounded-full flex items-center justify-center shrink-0 ml-4 ${iconBg}`}
      >
        <Icon className={`w-8 h-8 ${iconColor}`} />
      </div>
    </button>
  );
}

function ProgressBar({ value, colorClass }) {
  return (
    <div className="w-full bg-gray-200 rounded-full h-1.5">
      <div
        className={`h-1.5 rounded-full transition-all duration-500 ${colorClass}`}
        style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
      />
    </div>
  );
}

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [contactOpen, setContactOpen] = useState(false);
  const [companyOpen, setCompanyOpen] = useState(false);
  const [dealOpen, setDealOpen] = useState(false);

  const loadStats = useCallback(async () => {
    try {
      const data = await crmService.getDashboardStats();
      setStats(data);
    } catch (error) {
      console.error("Failed to load dashboard data:", error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadStats();
  }, [loadStats]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-blue-50">
        <AiOutlineLoading3Quarters className="animate-spin h-16 w-16 text-blue-600" />
      </div>
    );
  }

  if (!stats) return null;

  const quickActions = [
    {
      Icon: HiOutlineUserPlus,
      title: "Add New Contact",
      sub: "Create a new contact",
      action: () => setContactOpen(true),
    },
    {
      Icon: HiOutlineBuildingOffice,
      title: "Add New Company",
      sub: "Create a new company",
      action: () => setCompanyOpen(true),
    },
    {
      Icon: HiOutlineClipboardDocumentList,
      title: "Create New Deal",
      sub: "Start a new deal",
      action: () => setDealOpen(true),
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-6">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-[#1a237e] mb-1">Dashboard</h1>
        <p className="text-lg text-gray-500">
          Welcome back! Here's what's happening today.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <StatCard
          label="Total Contacts"
          value={stats.total_contacts}
          sub="↑ View all contacts"
          subColor="text-green-600"
          iconBg="bg-blue-50"
          iconColor="text-blue-600"
          Icon={HiOutlineUsers}
          onClick={() => setContactOpen(true)}
        />
        <StatCard
          label="Total Companies"
          value={stats.total_companies}
          sub="↑ View all companies"
          subColor="text-green-600"
          iconBg="bg-purple-50"
          iconColor="text-purple-600"
          Icon={HiOutlineBuildingOffice2}
          onClick={() => setCompanyOpen(true)}
        />
        <StatCard
          label="Active Deals"
          value={stats.total_deals}
          sub="↑ View pipeline"
          subColor="text-green-600"
          iconBg="bg-orange-50"
          iconColor="text-orange-500"
          Icon={HiOutlineClipboardDocumentList}
          onClick={() => setDealOpen(true)}
        />
        <StatCard
          label="Total Pipeline Value"
          value={formatCurrency(stats.total_deal_value)}
          sub={`Won: ${formatCurrency(stats.won_deals_value)}`}
          subColor="text-green-600 font-semibold"
          iconBg="bg-green-50"
          iconColor="text-green-600"
          Icon={HiOutlineChartBar}
          onClick={() => setDealOpen(true)}
        />
      </div>

      <div className="flex flex-col lg:flex-row gap-6">
        <div className="flex-1 min-w-0">
          <div className="bg-white rounded-xl shadow-md overflow-hidden">
            <div className="flex items-center justify-between px-5 py-4 bg-gray-50 border-b border-gray-100">
              <div className="flex items-center gap-2">
                <HiOutlineChartBar className="w-5 h-5 text-blue-600" />
                <span className="text-base font-bold text-gray-800">
                  Sales Pipeline
                </span>
              </div>
              <button
                onClick={() => setDealOpen(true)}
                className="text-sm text-blue-600 hover:text-blue-800 font-medium flex items-center gap-1 transition-colors"
              >
                Add Deal
                <HiOutlinePlus className="w-4 h-4" />
              </button>
            </div>
            <div className="p-5 grid grid-cols-2 md:grid-cols-3 gap-3">
              {stats.deals_by_stage?.map((stage) => {
                const colors = stage_colors[stage.stage] || stage_colors.lead;
                const pct =
                  stats.total_deals > 0
                    ? (stage.count / stats.total_deals) * 100
                    : 0;
                return (
                  <div
                    key={stage.stage}
                    className="p-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-transform hover:scale-[1.02]"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span
                        className={`text-xs font-bold px-2 py-0.5 rounded-full capitalize ${colors.chip}`}
                      >
                        {stage.stage}
                      </span>
                      <span className="text-xl font-bold text-gray-800">
                        {stage.count}
                      </span>
                    </div>
                    <ProgressBar value={pct} colorClass={colors.bar} />
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        <div className="lg:w-72 shrink-0">
          <div className="bg-white rounded-xl shadow-md overflow-hidden">
            <div className="flex items-center gap-2 px-5 py-4 bg-gray-50 border-b border-gray-100">
              <HiOutlineBolt className="w-5 h-5 text-blue-600" />
              <span className="text-base font-bold text-gray-800">
                Quick Actions
              </span>
            </div>
            <ul className="p-3 space-y-1">
              {quickActions.map((item) => (
                <li key={item.title}>
                  <button
                    onClick={item.action}
                    className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-blue-50 transition-colors text-left group"
                  >
                    <div className="w-9 h-9 rounded-lg bg-gray-100 group-hover:bg-blue-100 flex items-center justify-center shrink-0 transition-colors">
                      <item.Icon className="w-5 h-5 text-gray-500 group-hover:text-blue-600 transition-colors" />
                    </div>
                    <div className="min-w-0">
                      <p className="text-sm font-semibold text-gray-800">
                        {item.title}
                      </p>
                      <p className="text-xs text-gray-400">{item.sub}</p>
                    </div>
                  </button>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      <AddContactModal
        isOpen={contactOpen}
        onClose={() => setContactOpen(false)}
        onSaved={loadStats}
      />
      <AddCompanyModal
        isOpen={companyOpen}
        onClose={() => setCompanyOpen(false)}
        onSaved={loadStats}
      />
      <AddDealModal
        isOpen={dealOpen}
        onClose={() => setDealOpen(false)}
        onSaved={loadStats}
      />
    </div>
  );
}
