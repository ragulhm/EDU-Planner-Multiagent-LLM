import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "./context/AuthContext";
import { Login } from "./pages/Login";
import { CourseSelection } from "./pages/CourseSelection";
import { LearningPath } from "./pages/LearningPath";
import { Assessment } from "./pages/Assessment";
import { Dashboard } from "./pages/Dashboard";
import { LessonPlan } from "./pages/LessonPlan";

function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-black text-white">
        Loading...
      </div>
    );
  }

  return isAuthenticated ? children : <Navigate to="/" replace />;
}

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route
          path="/courses"
          element={
            <ProtectedRoute>
              <CourseSelection />
            </ProtectedRoute>
          }
        />
        <Route
          path="/path/:courseId"
          element={
            <ProtectedRoute>
              <LearningPath />
            </ProtectedRoute>
          }
        />
        <Route
          path="/assessment/:courseId/:level"
          element={
            <ProtectedRoute>
              <Assessment />
            </ProtectedRoute>
          }
        />
        <Route
          path="/dashboard/:courseId/:level"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/lesson/:topicId"
          element={
            <ProtectedRoute>
              <LessonPlan />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
