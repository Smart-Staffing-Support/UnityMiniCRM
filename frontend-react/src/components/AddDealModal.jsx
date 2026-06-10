import { useState, useEffect } from "react";
import { HiOutlineClipboardDocumentList } from "react-icons/hi2";
import { AiOutlineLoading3Quarters } from "react-icons/ai";
import { crmService } from "../services/api";

const field =
  "w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent";
const label = "block text-sm font-medium text-gray-700 mb-1";

const stages = [
  { value: "lead", label: "Lead" },
  { value: "qualified", label: "Qualified" },
  { value: "proposal", label: "Proposal" },
  { value: "negotiation", label: "Negotiation" },
  { value: "won", label: "Won" },
  { value: "lost", label: "Lost" },
];

export default function AddDealModal({ isOpen, onClose, onSaved }) {
  const [form, setForm] = useState({
    title: "",
    amount: "",
    stage: "lead",
    company: "",
    contact: "",
    expected_close_date: "",
  });
  const [companies, setCompanies] = useState([]);
  const [contacts, setContacts] = useState([]);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!isOpen) return;
    setForm({
      title: "",
      amount: "",
      stage: "lead",
      company: "",
      contact: "",
      expected_close_date: "",
    });
    setError("");
    Promise.all([crmService.getCompanies(), crmService.getContacts()])
      .then(([co, ct]) => {
        setCompanies(co);
        setContacts(ct);
      })
      .catch(() => {});
  }, [isOpen]);

  const set = (f) => (e) =>
    setForm((prev) => ({ ...prev, [f]: e.target.value }));

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError("");
    try {
      await crmService.createDeal({
        ...form,
        amount: Number(form.amount) || 0,
        company: form.company ? Number(form.company) : null,
        contact: form.contact ? Number(form.contact) : null,
        expected_close_date: form.expected_close_date || null,
      });
      onSaved();
      onClose();
    } catch (err) {
      const data = err.response?.data;
      setError(
        typeof data === "string"
          ? data
          : JSON.stringify(data) || "Failed to save deal",
      );
    } finally {
      setSaving(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
        <div className="flex items-center gap-2 px-6 py-4 bg-gray-50 rounded-t-xl border-b border-gray-200 sticky top-0">
          <HiOutlineClipboardDocumentList className="w-5 h-5 text-blue-600" />
          <span className="text-lg font-bold text-gray-800">New Deal</span>
        </div>

        <form onSubmit={handleSave} className="p-6">
          <div className="mb-4">
            <label className={label}>Deal Title *</label>
            <input
              required
              className={field}
              value={form.title}
              onChange={set("title")}
              placeholder="Enterprise License Deal"
            />
          </div>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className={label}>Amount *</label>
              <div className="relative">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 text-sm">
                  $
                </span>
                <input
                  required
                  type="number"
                  min="0"
                  step="0.01"
                  className={`${field} pl-7`}
                  value={form.amount}
                  onChange={set("amount")}
                  placeholder="10000"
                />
              </div>
            </div>
            <div>
              <label className={label}>Stage *</label>
              <select
                required
                className={field}
                value={form.stage}
                onChange={set("stage")}
              >
                {stages.map((s) => (
                  <option key={s.value} value={s.value}>
                    {s.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className={label}>
                Company{" "}
                <span className="text-gray-400 font-normal">(optional)</span>
              </label>
              <select
                className={field}
                value={form.company}
                onChange={set("company")}
              >
                <option value="">— Select company —</option>
                {companies.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className={label}>
                Contact{" "}
                <span className="text-gray-400 font-normal">(optional)</span>
              </label>
              <select
                className={field}
                value={form.contact}
                onChange={set("contact")}
              >
                <option value="">— Select contact —</option>
                {contacts.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.first_name} {c.last_name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="mb-5">
            <label className={label}>Expected Close Date</label>
            <input
              type="date"
              className={field}
              value={form.expected_close_date}
              onChange={set("expected_close_date")}
            />
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
              {error}
            </div>
          )}

          <div className="flex justify-end gap-3 pt-3 border-t border-gray-100">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2.5 text-sm font-medium text-gray-600 hover:text-gray-800 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={saving}
              className="px-5 py-2.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-60 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
            >
              {saving && (
                <AiOutlineLoading3Quarters className="animate-spin h-4 w-4" />
              )}
              Save Deal
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
