import React from "react";
import { useNavigate, useParams } from "react-router-dom";
import { motion } from "framer-motion";
import {
  HomeIcon,
  LayersIcon,
  BookOpenIcon,
  MessageSquareIcon,
  SparklesIcon,
  SearchIcon,
  BellIcon,
} from "lucide-react";
const topics = [
  {
    id: "html-basics",
    title: "Introduction to HTML",
    summary:
      "Learn the building blocks of web pages with semantic HTML elements.",
    progress: 75,
    duration: "2 hours",
  },
  {
    id: "css-basics",
    title: "CSS Fundamentals",
    summary: "Style your web pages with modern CSS techniques and layouts.",
    progress: 45,
    duration: "3 hours",
  },
  {
    id: "js-core",
    title: "JavaScript Core",
    summary: "Master variables, functions, and control flow in JavaScript.",
    progress: 20,
    duration: "4 hours",
  },
  {
    id: "react-intro",
    title: "React Foundations",
    summary:
      "Build interactive UIs with components, props, and state management.",
    progress: 0,
    duration: "5 hours",
  },
];
export function Dashboard() {
  const navigate = useNavigate();
  const { courseId, level } = useParams();
  return (
    <div className="flex min-h-screen w-full bg-black">
      {/* Sidebar */}
      <motion.div
        initial={{
          x: -20,
          opacity: 0,
        }}
        animate={{
          x: 0,
          opacity: 1,
        }}
        className="w-80 bg-gray-900/50 backdrop-blur-sm border-r border-gray-800 p-6"
      >
        <div className="flex items-center gap-3 mb-8">
          <div className="w-12 h-12 bg-gradient-to-br from-green-600 to-emerald-600 rounded-xl flex items-center justify-center">
            <span className="text-white text-xl">🎓</span>
          </div>
          <div>
            <h2 className="text-white font-semibold">EduPlanner</h2>
            <p className="text-gray-500 text-sm">Home</p>
          </div>
        </div>
        <nav className="space-y-2 mb-8">
          <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl bg-gray-800 text-white">
            <LayersIcon className="w-5 h-5" />
            <span>Modules</span>
          </button>
          <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-gray-400 hover:bg-gray-800 hover:text-white transition-all">
            <BookOpenIcon className="w-5 h-5" />
            <span>Library</span>
          </button>
          <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-gray-400 hover:bg-gray-800 hover:text-white transition-all">
            <MessageSquareIcon className="w-5 h-5" />
            <span>Community</span>
          </button>
        </nav>
        <div className="bg-gradient-to-br from-green-900/50 to-emerald-900/50 rounded-2xl p-6 border border-green-500/20">
          <div className="flex items-center gap-2 mb-3">
            <SparklesIcon className="w-5 h-5 text-green-400" />
            <span className="text-green-400 font-medium text-sm">
              Your Progress
            </span>
          </div>
          <div className="mb-4">
            <div className="flex items-center justify-between text-sm mb-2">
              <span className="text-white">Overall</span>
              <span className="text-green-400 font-bold">35%</span>
            </div>
            <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
              <div className="h-full bg-gradient-to-r from-green-600 to-emerald-600 w-[35%]" />
            </div>
          </div>
          <p className="text-gray-400 text-sm">
            Keep going! You are making great progress.
          </p>
        </div>
      </motion.div>
      {/* Main Content */}
      <div className="flex-1 overflow-auto">
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
          className="flex items-center justify-between p-6 border-b border-gray-800"
        >
          <div className="flex items-center gap-3">
            <SparklesIcon className="w-6 h-6 text-green-500" />
            <div>
              <h1 className="text-2xl font-bold text-white">Web Development</h1>
              <p className="text-gray-400 text-sm">Beginner Path</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <button className="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white py-2 px-6 rounded-xl transition-all duration-300 font-medium">
              Generate Plan Again
            </button>
            <button className="w-10 h-10 bg-gray-900 hover:bg-gray-800 rounded-xl flex items-center justify-center text-gray-400 hover:text-white transition-all">
              <SearchIcon className="w-5 h-5" />
            </button>
            <button className="w-10 h-10 bg-gray-900 hover:bg-gray-800 rounded-xl flex items-center justify-center text-gray-400 hover:text-white transition-all relative">
              <BellIcon className="w-5 h-5" />
              <div className="absolute top-2 right-2 w-2 h-2 bg-green-500 rounded-full" />
            </button>
            <div className="w-10 h-10 bg-gradient-to-br from-green-600 to-emerald-600 rounded-full flex items-center justify-center text-white font-semibold">
              JD
            </div>
          </div>
        </motion.div>
        {/* Topics Grid */}
        <div className="p-6">
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
            className="mb-6"
          >
            <h2 className="text-xl font-semibold text-white mb-2">
              Your Learning Path
            </h2>
            <p className="text-gray-400">
              Click on any topic to start learning, or take a test to assess
              your knowledge.
            </p>
          </motion.div>
          <div className="grid grid-cols-1 gap-4">
            {topics.map((topic, index) => (
              <motion.div
                key={topic.id}
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
                  scale: 1.01,
                  boxShadow: "0 0 30px rgba(168, 85, 247, 0.3)",
                }}
                className="group bg-gray-900/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-800 hover:border-green-500/50 transition-all duration-300 cursor-pointer"
                onClick={() => navigate(`/lesson/${topic.id}`)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-white mb-2 group-hover:text-green-400 transition-colors">
                      {topic.title}
                    </h3>
                    <p className="text-gray-400 mb-4">{topic.summary}</p>
                    <div className="flex items-center gap-4 mb-4">
                      <span className="text-sm text-gray-500">
                        Duration: {topic.duration}
                      </span>
                      <span className="text-sm text-green-400 font-medium">
                        {topic.progress}% complete
                      </span>
                    </div>
                    <div className="h-2 bg-gray-800 rounded-full overflow-hidden mb-4">
                      <motion.div
                        initial={{
                          width: 0,
                        }}
                        animate={{
                          width: `${topic.progress}%`,
                        }}
                        transition={{
                          duration: 1,
                          delay: 0.5 + index * 0.1,
                        }}
                        className="h-full bg-gradient-to-r from-green-600 to-emerald-600"
                      />
                    </div>
                  </div>
                  <button className="ml-6 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white py-2 px-6 rounded-xl transition-all duration-300 font-medium whitespace-nowrap">
                    Take Test
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
