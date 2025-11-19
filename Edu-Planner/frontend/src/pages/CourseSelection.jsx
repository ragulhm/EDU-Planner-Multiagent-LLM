import React from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useAuth } from "../context/AuthContext";
import {
  CodeIcon,
  DatabaseIcon,
  BrainCircuitIcon,
  PaletteIcon,
  SearchIcon,
  SparklesIcon,
  LogOutIcon,
} from "lucide-react";
const courses = [
  {
    id: "web-dev",
    title: "Web Development",
    description:
      "Build modern experiences with HTML, CSS, JavaScript, and React.",
    icon: CodeIcon,
    gradient: "from-green-600 to-emerald-600",
  },
  {
    id: "data-science",
    title: "Data Science",
    description:
      "Master analytics, visualization, and machine learning fundamentals.",
    icon: DatabaseIcon,
    gradient: "from-green-600 to-emerald-600",
  },
  {
    id: "ai",
    title: "Artificial Intelligence",
    description: "Explore neural networks, deep learning, and AI applications.",
    icon: BrainCircuitIcon,
    gradient: "from-green-600 to-emerald-600",
  },
  {
    id: "ui-ux",
    title: "UI/UX Design",
    description: "Create beautiful, user-centered digital experiences.",
    icon: PaletteIcon,
    gradient: "from-emerald-600 to-green-600",
  },
];
export function CourseSelection() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  return (
    <div className="min-h-screen w-full bg-black">
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-20 w-96 h-96 bg-green-500/5 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-emerald-500/5 rounded-full blur-3xl animate-pulse delay-1000" />
      </div>
      {/* Top Bar */}
      <motion.div
        initial={{
          y: -20,
          opacity: 0,
        }}
        animate={{
          y: 0,
          opacity: 1,
        }}
        className="relative z-10 flex items-center justify-between p-6 border-b border-gray-800"
      >
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 bg-gradient-to-br from-green-600 to-emerald-600 rounded-xl flex items-center justify-center">
            <span className="text-white text-xl">🎓</span>
          </div>
          <div>
            <h2 className="text-white font-semibold">EduPlanner</h2>
            <p className="text-gray-500 text-sm">
              Welcome back, {user?.email || "Student"}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <div className="relative">
            <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500" />
            <input
              type="text"
              placeholder="Search..."
              className="bg-gray-900 text-white py-2 pl-10 pr-4 rounded-xl border border-gray-800 focus:border-green-500 focus:outline-none w-64"
            />
          </div>
          <button
            onClick={logout}
            className="flex items-center gap-2 bg-gray-900 hover:bg-gray-800 text-white py-2 px-4 rounded-xl border border-gray-800 hover:border-red-500/50 transition-all duration-300"
          >
            <LogOutIcon className="w-4 h-4" />
            Logout
          </button>
          <div className="w-10 h-10 bg-gradient-to-br from-green-600 to-emerald-600 rounded-full flex items-center justify-center text-white font-semibold">
            {user?.email?.charAt(0).toUpperCase() || "U"}
          </div>
        </div>
      </motion.div>
      {/* Main Content */}
      <div className="relative z-10 max-w-7xl mx-auto px-6 py-12">
        <motion.div
          initial={{
            y: 20,
            opacity: 0,
          }}
          animate={{
            y: 0,
            opacity: 1,
          }}
          transition={{
            delay: 0.2,
          }}
          className="mb-12"
        >
          <div className="flex items-center gap-3 mb-4">
            <SparklesIcon className="w-6 h-6 text-green-400" />
            <span className="text-green-400 font-medium">Welcome</span>
          </div>
          <h1 className="text-5xl font-bold text-white mb-4">
            Choose your path
          </h1>
          <p className="text-gray-400 text-lg">Pick a domain and dive in.</p>
        </motion.div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {courses.map((course, index) => (
            <motion.div
              key={course.id}
              initial={{
                y: 20,
                opacity: 0,
              }}
              animate={{
                y: 0,
                opacity: 1,
              }}
              transition={{
                delay: 0.3 + index * 0.1,
              }}
              whileHover={{
                scale: 1.02,
                y: -5,
              }}
              className="group relative bg-gray-900/50 backdrop-blur-sm rounded-3xl p-8 border border-gray-800 hover:border-green-500/50 transition-all duration-300 cursor-pointer overflow-hidden"
              onClick={() => navigate(`/path/${course.id}`)}
            >
              {/* Gradient Overlay */}
              <div
                className={`absolute inset-0 bg-gradient-to-br ${course.gradient} opacity-0 group-hover:opacity-10 transition-opacity duration-300`}
              />
              <div className="relative z-10">
                <div className="flex items-start justify-between mb-6">
                  <div
                    className={`w-14 h-14 bg-gradient-to-br ${course.gradient} rounded-2xl flex items-center justify-center shadow-lg`}
                  >
                    <course.icon className="w-7 h-7 text-white" />
                  </div>
                  <span className="text-xs text-gray-500 bg-gray-800 px-3 py-1 rounded-full">
                    Course
                  </span>
                </div>
                <h3 className="text-2xl font-bold text-white mb-3">
                  {course.title}
                </h3>
                <p className="text-gray-400 mb-6">{course.description}</p>
                <button className="text-green-400 font-medium flex items-center gap-2 group-hover:gap-3 transition-all">
                  Explore
                  <motion.span
                    animate={{
                      x: [0, 5, 0],
                    }}
                    transition={{
                      duration: 1.5,
                      repeat: Infinity,
                    }}
                  >
                    →
                  </motion.span>
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
