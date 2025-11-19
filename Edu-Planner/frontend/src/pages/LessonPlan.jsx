import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeftIcon, PlayIcon, CheckCircleIcon, CircleIcon, SendIcon, BookOpenIcon, VideoIcon, FileTextIcon } from 'lucide-react';
const lessonSteps = [{
  id: 1,
  title: 'Intro',
  description: 'Get a quick overview and context.',
  completed: true
}, {
  id: 2,
  title: 'Concepts',
  description: 'Learn core ideas with small demos.',
  completed: true
}, {
  id: 3,
  title: 'Hands-on',
  description: 'Build a mini project to apply the concept.',
  completed: false
}, {
  id: 4,
  title: 'Review',
  description: 'Summarize, quiz yourself, and set next actions.',
  completed: false
}];
const resources = [{
  title: 'MDN Guide',
  url: '#'
}, {
  title: 'WebAIM Checklist',
  url: '#'
}, {
  title: 'Awesome Repo',
  url: '#'
}, {
  title: 'Practice Challenges',
  url: '#'
}];
export function LessonPlan() {
  const navigate = useNavigate();
  const {
    topicId
  } = useParams();
  const [currentStep, setCurrentStep] = useState(0);
  const [chatMessage, setChatMessage] = useState('');
  return <div className="min-h-screen w-full bg-black">
      {/* Header */}
      <motion.div initial={{
      y: -20,
      opacity: 0
    }} animate={{
      y: 0,
      opacity: 1
    }} className="border-b border-gray-800 p-6">
        <div className="flex items-center justify-between max-w-7xl mx-auto">
          <button onClick={() => navigate(-1)} className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors">
            <ArrowLeftIcon className="w-5 h-5" />
            Back
          </button>
          <div className="flex items-center gap-4">
            <button className="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white py-2 px-6 rounded-xl transition-all duration-300 font-medium">
              Quick Quiz
            </button>
          </div>
        </div>
      </motion.div>
      {/* Main Content */}
      <div className="max-w-7xl mx-auto p-6">
        <motion.div initial={{
        y: 20,
        opacity: 0
      }} animate={{
        y: 0,
        opacity: 1
      }} transition={{
        delay: 0.1
      }} className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            Web Development • HTML Basics
          </h1>
          <p className="text-gray-400">
            Structure the web with semantic building blocks.
          </p>
        </motion.div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content Area */}
          <div className="lg:col-span-2 space-y-6">
            {/* Overview Section */}
            <motion.div initial={{
            y: 20,
            opacity: 0
          }} animate={{
            y: 0,
            opacity: 1
          }} transition={{
            delay: 0.2
          }} className="bg-gray-900/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-800">
              <div className="flex items-center gap-3 mb-4">
                <VideoIcon className="w-5 h-5 text-green-500" />
                <h2 className="text-xl font-bold text-white">Overview</h2>
              </div>
              <p className="text-gray-400 mb-6">
                This lesson introduces key ideas with a short video, concise
                notes, and practice tasks. Use the progress timeline to jump
                between stages.
              </p>
              {/* Video Player */}
              <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl aspect-video flex items-center justify-center mb-6 relative overflow-hidden group cursor-pointer">
                <div className="absolute inset-0 bg-gradient-to-br from-green-900/20 to-emerald-900/20" />
                <motion.button whileHover={{
                scale: 1.1
              }} whileTap={{
                scale: 0.95
              }} className="relative z-10 w-20 h-20 bg-white/10 backdrop-blur-sm rounded-full flex items-center justify-center group-hover:bg-white/20 transition-all">
                  <PlayIcon className="w-10 h-10 text-white ml-1" />
                </motion.button>
                <div className="absolute bottom-4 left-4 text-white text-sm bg-black/50 backdrop-blur-sm px-3 py-1 rounded-lg">
                  Video Tutorial
                </div>
              </div>
            </motion.div>
            {/* Learning Objectives */}
            <motion.div initial={{
            y: 20,
            opacity: 0
          }} animate={{
            y: 0,
            opacity: 1
          }} transition={{
            delay: 0.3
          }} className="bg-gray-900/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-800">
              <div className="flex items-center gap-3 mb-4">
                <BookOpenIcon className="w-5 h-5 text-green-500" />
                <h2 className="text-xl font-bold text-white">
                  Learning Objectives
                </h2>
              </div>
              <ul className="space-y-3">
                <li className="flex items-start gap-3 text-gray-300">
                  <CheckCircleIcon className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>Understand the problem domain and vocabulary</span>
                </li>
                <li className="flex items-start gap-3 text-gray-300">
                  <CheckCircleIcon className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>Apply concepts with guided exercises</span>
                </li>
                <li className="flex items-start gap-3 text-gray-300">
                  <CheckCircleIcon className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>Evaluate solutions and reflect on improvements</span>
                </li>
              </ul>
            </motion.div>
            {/* Lesson Steps */}
            <motion.div initial={{
            y: 20,
            opacity: 0
          }} animate={{
            y: 0,
            opacity: 1
          }} transition={{
            delay: 0.4
          }} className="bg-gray-900/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-800">
              <div className="flex items-center gap-3 mb-4">
                <FileTextIcon className="w-5 h-5 text-green-500" />
                <h2 className="text-xl font-bold text-white">Lesson Steps</h2>
              </div>
              <div className="space-y-3">
                {lessonSteps.map((step, index) => <motion.div key={step.id} whileHover={{
                scale: 1.02
              }} className={`p-4 rounded-xl border-2 cursor-pointer transition-all ${currentStep === index ? 'border-green-500 bg-green-500/10' : 'border-gray-800 bg-gray-800/50 hover:border-gray-700'}`} onClick={() => setCurrentStep(index)}>
                    <div className="flex items-start gap-4">
                      <div className="flex-shrink-0 mt-1">
                        {step.completed ? <CheckCircleIcon className="w-6 h-6 text-green-500" /> : <CircleIcon className="w-6 h-6 text-gray-600" />}
                      </div>
                      <div className="flex-1">
                        <h3 className="text-white font-semibold mb-1">
                          {step.id}. {step.title}
                        </h3>
                        <p className="text-gray-400 text-sm">
                          {step.description}
                        </p>
                      </div>
                    </div>
                  </motion.div>)}
              </div>
              <div className="mt-6 pt-6 border-t border-gray-800">
                <p className="text-gray-500 text-sm mb-2">
                  Drag to navigate steps
                </p>
                <div className="flex items-center gap-2">
                  {lessonSteps.map((step, index) => <div key={step.id} className={`h-2 rounded-full flex-1 cursor-pointer transition-all ${index <= currentStep ? 'bg-gradient-to-r from-green-600 to-emerald-600' : 'bg-gray-800'}`} onClick={() => setCurrentStep(index)} />)}
                </div>
                <p className="text-gray-400 text-sm mt-2">
                  Current: {lessonSteps[currentStep].title}
                </p>
              </div>
            </motion.div>
            {/* Resources */}
            <motion.div initial={{
            y: 20,
            opacity: 0
          }} animate={{
            y: 0,
            opacity: 1
          }} transition={{
            delay: 0.5
          }} className="bg-gray-900/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-800">
              <h2 className="text-xl font-bold text-white mb-4">Resources</h2>
              <div className="grid grid-cols-2 gap-3">
                {resources.map((resource, index) => <a key={index} href={resource.url} className="bg-gray-800/50 hover:bg-gray-800 p-4 rounded-xl border border-gray-700 hover:border-green-500/50 transition-all text-white text-sm font-medium">
                    {resource.title}
                  </a>)}
              </div>
            </motion.div>
          </div>
          {/* Sidebar - AI Chat Tutor */}
          <div className="lg:col-span-1">
            <motion.div initial={{
            y: 20,
            opacity: 0
          }} animate={{
            y: 0,
            opacity: 1
          }} transition={{
            delay: 0.3
          }} className="bg-gray-900/50 backdrop-blur-sm rounded-2xl border border-gray-800 overflow-hidden sticky top-6">
              <div className="p-6 border-b border-gray-800">
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                  AI Chat Tutor
                  <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                </h2>
                <p className="text-gray-400 text-sm mt-1">
                  Ask anything about this lesson and get instant guidance.
                </p>
              </div>
              <div className="h-96 p-6 overflow-y-auto space-y-4">
                <div className="bg-green-900/20 border border-green-500/30 rounded-2xl p-4">
                  <p className="text-green-300 text-sm">
                    Hi! I am here to help you understand HTML basics. What would
                    you like to know?
                  </p>
                </div>
              </div>
              <div className="p-4 border-t border-gray-800">
                <div className="flex gap-2">
                  <input type="text" placeholder="Type your question..." value={chatMessage} onChange={e => setChatMessage(e.target.value)} className="flex-1 bg-gray-800 text-white py-3 px-4 rounded-xl border border-gray-700 focus:border-green-500 focus:outline-none" />
                  <button className="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white p-3 rounded-xl transition-all">
                    <SendIcon className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </motion.div>
            {/* Quick Knowledge Check */}
            <motion.div initial={{
            y: 20,
            opacity: 0
          }} animate={{
            y: 0,
            opacity: 1
          }} transition={{
            delay: 0.4
          }} className="bg-gray-900/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-800 mt-6">
              <h3 className="text-lg font-bold text-white mb-4">
                Quick Knowledge Check
              </h3>
              <p className="text-gray-400 text-sm mb-4">
                Which tag creates a link?
              </p>
              <div className="space-y-2 mb-4">
                {['<url>', '<a>', '<link>'].map((option, index) => <button key={index} className="w-full text-left p-3 rounded-xl border border-gray-800 hover:border-green-500/50 bg-gray-800/50 hover:bg-gray-800 text-white text-sm transition-all">
                    {option}
                  </button>)}
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500">Score: 0</span>
                <button className="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white py-2 px-4 rounded-lg transition-all">
                  Next
                </button>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>;
}