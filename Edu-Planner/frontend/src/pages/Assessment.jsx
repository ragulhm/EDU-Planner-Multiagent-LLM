import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { ClockIcon, ArrowRightIcon } from "lucide-react";
const questions = [
  {
    id: 1,
    question: "What does HTML stand for?",
    options: [
      "Hyper Text Markup Language",
      "High Tech Modern Language",
      "Home Tool Markup Language",
      "Hyperlinks and Text Markup Language",
    ],
    correct: 0,
  },
  {
    id: 2,
    question: "Which CSS property controls text size?",
    options: ["text-size", "font-size", "text-style", "font-style"],
    correct: 1,
  },
  {
    id: 3,
    question: "What is the correct syntax for a JavaScript function?",
    options: [
      "function myFunction()",
      "def myFunction()",
      "func myFunction()",
      "function:myFunction()",
    ],
    correct: 0,
  },
];
export function Assessment() {
  const navigate = useNavigate();
  const { courseId, level } = useParams();
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [timeLeft, setTimeLeft] = useState(60);
  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(timer);
  }, [currentQuestion]);
  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswer(null);
      setTimeLeft(60);
    } else {
      navigate(`/dashboard/${courseId}/${level}`);
    }
  };
  const progress = ((currentQuestion + 1) / questions.length) * 100;
  return (
    <div className="min-h-screen w-full bg-black flex items-center justify-center p-6">
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-green-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl animate-pulse delay-1000" />
      </div>
      <motion.div
        initial={{
          opacity: 0,
          y: 20,
        }}
        animate={{
          opacity: 1,
          y: 0,
        }}
        className="relative z-10 w-full max-w-3xl"
      >
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between text-sm text-gray-400 mb-2">
            <span>
              Question {currentQuestion + 1} of {questions.length}
            </span>
            <div className="flex items-center gap-2">
              <ClockIcon className="w-4 h-4" />
              <span className={timeLeft < 20 ? "text-red-500" : ""}>
                {timeLeft}s
              </span>
            </div>
          </div>
          <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
            <motion.div
              initial={{
                width: 0,
              }}
              animate={{
                width: `${progress}%`,
              }}
              className="h-full bg-gradient-to-r from-green-600 to-emerald-600"
            />
          </div>
        </div>
        {/* Question Card */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentQuestion}
            initial={{
              opacity: 0,
              x: 50,
            }}
            animate={{
              opacity: 1,
              x: 0,
            }}
            exit={{
              opacity: 0,
              x: -50,
            }}
            className="bg-gray-900/50 backdrop-blur-sm rounded-3xl p-10 border border-gray-800"
          >
            <h2 className="text-3xl font-bold text-white mb-8">
              {questions[currentQuestion].question}
            </h2>
            <div className="space-y-4 mb-8">
              {questions[currentQuestion].options.map((option, index) => (
                <motion.button
                  key={index}
                  whileHover={{
                    scale: 1.02,
                  }}
                  whileTap={{
                    scale: 0.98,
                  }}
                  onClick={() => setSelectedAnswer(index)}
                  className={`w-full text-left p-6 rounded-2xl border-2 transition-all duration-300 ${
                    selectedAnswer === index
                      ? "border-green-500 bg-green-500/10"
                      : "border-gray-800 bg-gray-800/50 hover:border-gray-700"
                  }`}
                >
                  <div className="flex items-center gap-4">
                    <div
                      className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                        selectedAnswer === index
                          ? "border-green-500 bg-green-500"
                          : "border-gray-600"
                      }`}
                    >
                      {selectedAnswer === index && (
                        <motion.div
                          initial={{
                            scale: 0,
                          }}
                          animate={{
                            scale: 1,
                          }}
                          className="w-3 h-3 bg-white rounded-full"
                        />
                      )}
                    </div>
                    <span className="text-white font-medium">{option}</span>
                  </div>
                </motion.button>
              ))}
            </div>
            <button
              onClick={handleNext}
              disabled={selectedAnswer === null}
              className="w-full bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 disabled:from-gray-700 disabled:to-gray-700 text-white py-4 px-6 rounded-2xl flex items-center justify-center gap-3 transition-all duration-300 shadow-lg disabled:shadow-none disabled:cursor-not-allowed"
            >
              {currentQuestion < questions.length - 1
                ? "Next Question"
                : "Complete Assessment"}
              <ArrowRightIcon className="w-5 h-5" />
            </button>
          </motion.div>
        </AnimatePresence>
      </motion.div>
    </div>
  );
}
