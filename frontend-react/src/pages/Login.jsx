import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { HiOutlineUser, HiOutlineLockClosed, HiOutlineBuildingOffice2 } from "react-icons/hi2";
import { AiOutlineLoading3Quarters } from "react-icons/ai";
import { authService } from "../services/api";

export default function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!username || !password) {
      setError("Please enter both username and password");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const data = await authService.login(username, password);
      localStorage.setItem("token", data.token);
      localStorage.setItem("user", JSON.stringify(data.user));
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.error || "Login failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#001f3f] to-[#0074D9]">
      <div className="w-full max-w-md mx-4">
        <div className="bg-white rounded-xl shadow-2xl p-8">
          <div className="text-center mb-6">
            <div className="flex justify-center mb-3">
              <HiOutlineBuildingOffice2 className="w-16 h-16 text-blue-600" />
            </div>
            <h1 className="text-2xl font-bold text-[#001f3f] mb-1">Mini CRM</h1>
            <p className="text-gray-500 text-sm">Sign in to continue</p>
          </div>

          <form onSubmit={handleLogin}>
            <div className="mb-3">
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <HiOutlineUser className="w-5 h-5 text-gray-400" />
                </div>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Username"
                  disabled={loading}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
                />
              </div>
            </div>

            <div className="mb-4">
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <HiOutlineLockClosed className="w-5 h-5 text-gray-400" />
                </div>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Password"
                  disabled={loading}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
                />
              </div>
            </div>

            {error && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-start justify-between gap-2">
                <span className="text-red-700 text-sm">{error}</span>
                <button
                  type="button"
                  onClick={() => setError("")}
                  className="text-red-400 hover:text-red-600 text-lg leading-none shrink-0"
                >
                  &times;
                </button>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-60 disabled:cursor-not-allowed flex items-center justify-center mb-4"
            >
              {loading ? (
                <AiOutlineLoading3Quarters className="animate-spin h-5 w-5 text-white" />
              ) : (
                "Sign In"
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
