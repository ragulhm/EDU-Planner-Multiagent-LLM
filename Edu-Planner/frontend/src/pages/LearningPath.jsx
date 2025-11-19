import React from "react";
import { useNavigate, useParams } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowLeftIcon, StarIcon, TrendingUpIcon, ZapIcon } from "lucide-react";
const paths = [
  {
    level: "beginner",
    title: "Beginner",
    description:
      "Start from scratch with foundational concepts and guided exercises.",
    duration: "8-12 weeks",
    topics: 24,
    icon: StarIcon,
    gradient: "from-green-600 to-emerald-600",
  },
  {
    level: "intermediate",
    title: "Intermediate",
    description:
      "Build on basics with real-world projects and advanced techniques.",
    duration: "12-16 weeks",
    topics: 36,
    icon: TrendingUpIcon,
    gradient: "from-green-600 to-emerald-600",
  },
  {
    level: "advanced",
    title: "Advanced",
    description:
      "Master complex patterns, optimization, and industry best practices.",
    duration: "16-20 weeks",
    topics: 48,
    icon: ZapIcon,
    gradient: "from-emerald-600 to-green-600",
  },
];
export function LearningPath() {
  const navigate = useNavigate();
  const { courseId } = useParams();
  return (
    <div className="min-h-screen w-full bg-black">
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 right-20 w-96 h-96 bg-green-500/5 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-20 left-20 w-96 h-96 bg-emerald-500/5 rounded-full blur-3xl animate-pulse delay-1000" />
      </div>
      {/* Header */}
      <motion.div
        initial={{
          y: -20,
          opacity: 0,
        }}
        animate={{
          y: 0,
          opacity: 1,
        }}
        className="relative z-10 p-6 border-b border-gray-800"
      >
        <button
          onClick={() => navigate("/courses")}
          className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
        >
          <ArrowLeftIcon className="w-5 h-5" />
          Back to Courses
        </button>
      </motion.div>
      {/* Main Content */}
      <div className="relative z-10 max-w-6xl mx-auto px-6 py-16">
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
          className="text-center mb-16"
        >
          <h1 className="text-5xl font-bold text-white mb-4">
            Web Development
          </h1>
          <p className="text-gray-400 text-lg">
            Build modern experiences with HTML, CSS, JavaScript, and React.
          </p>
        </motion.div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {paths.map((path, index) => (
            <motion.div
              key={path.level}
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
                scale: 1.05,
                y: -10,
              }}
              className="group relative bg-gray-900/50 backdrop-blur-sm rounded-3xl p-8 border border-gray-800 hover:border-green-500/50 transition-all duration-300 cursor-pointer overflow-hidden"
              onClick={() => navigate(`/assessment/${courseId}/${path.level}`)}
            >
              {/* Gradient Overlay */}
              <div
                className={`absolute inset-0 bg-gradient-to-br ${path.gradient} opacity-0 group-hover:opacity-10 transition-opacity duration-300`}
              />
              <div className="relative z-10">
                <div
                  className={`w-16 h-16 bg-gradient-to-br ${path.gradient} rounded-2xl flex items-center justify-center shadow-lg mb-6`}
                >
                  <path.icon className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-3xl font-bold text-white mb-3">
                  {path.title}
                </h3>
                <p className="text-gray-400 mb-6 min-h-[60px]">
                  {path.description}
                </p>
                <div className="space-y-3 mb-6">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-500">Duration</span>
                    <span className="text-white font-medium">
                      {path.duration}
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-500">Topics</span>
                    <span className="text-white font-medium">
                      {path.topics} lessons
                    </span>
                  </div>
                </div>
                {/* Progress Bar */}
                <div className="mb-6">
                  <div className="flex items-center justify-between text-xs text-gray-500 mb-2">
                    <span>Progress</span>
                    <span>0%</span>
                  </div>
                  <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                    <div
                      className={`h-full bg-gradient-to-r ${path.gradient} w-0`}
                    />
                  </div>
                </div>
                <button className="w-full bg-gray-800 hover:bg-gray-700 text-white py-3 px-6 rounded-xl transition-all duration-300 font-medium">
                  Select Path
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
