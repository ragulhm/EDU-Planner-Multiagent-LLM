import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  MailIcon,
  LockIcon,
  LogInIcon,
  ArrowRightIcon,
  AlertCircle,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";

export function Login() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const endpoint = isLogin ? "/api/auth/login" : "/api/auth/signup";
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        login(data.user, data.token);
        navigate("/courses");
      } else {
        setError(data.message || "An error occurred");
      }
    } catch (error) {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="flex min-h-screen w-full bg-black">
      
      <motion.div
        initial={{
          opacity: 0,
          x: -50,
        }}
        animate={{
          opacity: 1,
          x: 0,
        }}
        transition={{
          duration: 0.8,
        }}
        className="hidden lg:flex lg:w-1/2 relative overflow-hidden"
      >
        <div className="absolute inset-0 bg-gradient-to-br from-gray-900 via-green-950 to-emerald-950">
          <div className="absolute inset-0 opacity-20">
            <div className="absolute top-20 left-20 w-64 h-64 bg-green-500 rounded-full blur-3xl animate-pulse" />
            <div className="absolute bottom-20 right-20 w-96 h-96 bg-emerald-500 rounded-full blur-3xl animate-pulse delay-1000" />
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-gray-500 rounded-full blur-3xl animate-pulse delay-500" />
          </div>
        </div>
        <div className="relative z-10 flex items-center justify-center w-full">
          <motion.div
            animate={{
              rotate: 360,
            }}
            transition={{
              duration: 20,
              repeat: Infinity,
              ease: "linear",
            }}
            className="w-64 h-64 border-4 border-white/10 rounded-full flex items-center justify-center"
          >
            <div className="w-48 h-48 border-4 border-white/20 rounded-full flex items-center justify-center">
              <div className="w-32 h-32 bg-white/5 backdrop-blur-sm rounded-full flex items-center justify-center">
                <span className="text-white text-6xl">🎓</span>
              </div>
            </div>
          </motion.div>
        </div>
        <div className="absolute bottom-8 left-8 text-white/40 text-sm flex items-center gap-2">
          <div className="w-2 h-2 bg-white/40 rounded-full animate-pulse" />
          Interactive 3D • Move your mouse
        </div>
      </motion.div>
      {/* Right Side - Login Form */}
      <motion.div
        initial={{
          opacity: 0,
          x: 50,
        }}
        animate={{
          opacity: 1,
          x: 0,
        }}
        transition={{
          duration: 0.8,
        }}
        className="w-full lg:w-1/2 flex items-center justify-center p-8"
      >
        <div className="w-full max-w-md space-y-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-white mb-2">EduPlanner</h1>
            <p className="text-gray-400">
              Welcome back — continue your journey.
            </p>
          </div>
          <div className="space-y-4">
            <button className="w-full bg-gray-900 hover:bg-gray-800 text-white py-4 px-6 rounded-2xl flex items-center justify-center gap-3 transition-all duration-300 border border-gray-800 hover:border-gray-700">
              <svg className="w-5 h-5 fill-gray-400" viewBox="0 0 24 24">
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
              </svg>
              Continue with Google
            </button>
            <button
              onClick={() => navigate("/courses")}
              className="w-full bg-gray-900 hover:bg-gray-800 text-white py-4 px-6 rounded-2xl flex items-center justify-center gap-3 transition-all duration-300 border border-gray-800 hover:border-gray-700"
            >
              Explore Courses
              <ArrowRightIcon className="w-5 h-5" />
            </button>
          </div>
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-800" />
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-4 bg-black text-gray-500">
                OR CONTINUE WITH EMAIL
              </span>
            </div>
          </div>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="relative">
              <MailIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-500" />
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-gray-900 text-white py-4 pl-12 pr-6 rounded-2xl border border-gray-800 focus:border-green-500 focus:outline-none transition-all duration-300"
              />
            </div>
            <div className="relative">
              <LockIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-500" />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-gray-900 text-white py-4 pl-12 pr-6 rounded-2xl border border-gray-800 focus:border-green-500 focus:outline-none transition-all duration-300"
              />
            </div>
            {error && (
              <div className="flex items-center gap-2 text-red-400 text-sm bg-red-900/20 border border-red-800 rounded-lg p-3">
                <AlertCircle className="w-4 h-4" />
                {error}
              </div>
            )}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 disabled:from-gray-600 disabled:to-gray-600 text-white py-4 px-6 rounded-2xl flex items-center justify-center gap-3 transition-all duration-300 shadow-lg shadow-green-500/20 disabled:opacity-50"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <LogInIcon className="w-5 h-5" />
              )}
              {loading ? "Processing..." : isLogin ? "Sign In" : "Sign Up"}
              {!loading && <ArrowRightIcon className="w-5 h-5" />}
            </button>
          </form>
          <div className="text-center text-gray-400">
            Don't have an account?{" "}
            <button
              onClick={() => setIsLogin(!isLogin)}
              className="text-green-400 hover:text-green-300 transition-colors"
            >
              Sign up
            </button>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
