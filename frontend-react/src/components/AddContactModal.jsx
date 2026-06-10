import { useState, useEffect } from "react";
import { HiOutlineUserPlus } from "react-icons/hi2";
import { AiOutlineLoading3Quarters } from "react-icons/ai";
import { crmService } from "../services/api";

const field = "w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent";
const label = "block text-sm font-medium text-gray-700 mb-1";

export default function AddContactModal({ isOpen, onClose, onSaved }) {
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    position: "",
    company: "",
  });
  const [companies, setCompanies] = useState([]);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!isOpen) return;
    setForm({ first_name: "", last_name: "", email: "", phone: "", position: "", company: "" });
    setError("");
    crmService.getCompanies().then(setCompanies).catch(() => setCompanies([]));
  }, [isOpen]);

  const set = (f) => (e) => setForm((prev) => ({ ...prev, [f]: e.target.value }));

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError("");
    try {
      await crmService.createContact({
        ...form,
        company: form.company ? Number(form.company) : null,
      });
      onSaved();
      onClose();
    } catch (err) {
      const data = err.response?.data;
      setError(typeof data === "string" ? data : JSON.stringify(data) || "Failed to save contact");
    } finally {
      setSaving(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-lg">
        <div className="flex items-center gap-2 px-6 py-4 bg-gray-50 rounded-t-xl border-b border-gray-200">
          <HiOutlineUserPlus className="w-5 h-5 text-blue-600" />
          <span className="text-lg font-bold text-gray-800">New Contact</span>
        </div>

        <form onSubmit={handleSave} className="p-6">
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className={label}>First Name *</label>
              <input required className={field} value={form.first_name} onChange={set("first_name")} placeholder="John" />
            </div>
            <div>
              <label className={label}>Last Name *</label>
              <input required className={field} value={form.last_name} onChange={set("last_name")} placeholder="Doe" />
            </div>
          </div>

          <div className="mb-4">
            <label className={label}>Email *</label>
            <input required type="email" className={field} value={form.email} onChange={set("email")} placeholder="john@example.com" />
          </div>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className={label}>Phone</label>
              <input className={field} value={form.phone} onChange={set("phone")} placeholder="+1 555 0100" />
            </div>
            <div>
              <label className={label}>Position</label>
              <input className={field} value={form.position} onChange={set("position")} placeholder="CEO" />
            </div>
          </div>

          <div className="mb-5">
            <label className={label}>
              Company <span className="text-gray-400 font-normal">(optional)</span>
            </label>
            <select className={field} value={form.company} onChange={set("company")}>
              <option value="">— Select a company —</option>
              {companies.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">{error}</div>
          )}

          <div className="flex justify-end gap-3 pt-3 border-t border-gray-100">
            <button type="button" onClick={onClose} className="px-4 py-2.5 text-sm font-medium text-gray-600 hover:text-gray-800 transition-colors">
              Cancel
            </button>
            <button
              type="submit"
              disabled={saving}
              className="px-5 py-2.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-60 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
            >
              {saving && <AiOutlineLoading3Quarters className="animate-spin h-4 w-4" />}
              Save Contact
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
