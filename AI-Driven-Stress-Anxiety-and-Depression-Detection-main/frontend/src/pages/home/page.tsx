
import { Link } from 'react-router-dom';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-teal-50 via-white to-blue-50">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 transition-all duration-300 bg-white/80 backdrop-blur-md shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img 
              src="https://public.readdy.ai/ai/img_res/85dcc970-73df-4a59-8d6d-8e5d7d2d3a0a.png" 
              alt="MindCare AI Logo" 
              className="w-10 h-10 object-contain"
            />
            <span className="text-xl font-semibold text-gray-800">MindCare AI</span>
          </div>
          <div className="flex items-center gap-4">
            <Link 
              to="/login" 
              className="px-5 py-2 text-sm font-medium text-teal-600 hover:text-teal-700 transition-colors whitespace-nowrap cursor-pointer"
            >
              Sign In
            </Link>
            <Link 
              to="/signup" 
              className="px-6 py-2 text-sm font-medium bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors whitespace-nowrap cursor-pointer"
            >
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6">
        <div className="max-w-6xl mx-auto text-center">
          <div className="inline-block px-4 py-2 bg-teal-100 text-teal-700 rounded-full text-sm font-medium mb-6">
            AI-Powered Mental Wellness Platform
          </div>
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            AI-Driven Stress, Anxiety, and Depression Detection and Lifestyle Support System
          </h1>
          <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto leading-relaxed">
            An intelligent mental health monitoring platform that analyzes your emotional state through text, 
            providing personalized insights and wellness recommendations to support your mental wellbeing.
          </p>
          <div className="flex items-center justify-center gap-4 mb-16">
            <Link 
              to="/dashboard" 
              className="px-8 py-4 bg-teal-600 text-white rounded-lg font-medium hover:bg-teal-700 transition-all shadow-lg hover:shadow-xl whitespace-nowrap cursor-pointer"
            >
              Start Analysis
            </Link>
            <Link 
              to="/signup" 
              className="px-8 py-4 bg-white text-teal-600 border-2 border-teal-600 rounded-lg font-medium hover:bg-teal-50 transition-all whitespace-nowrap cursor-pointer"
            >
              Create Account
            </Link>
          </div>

          {/* Workflow Visualization */}
          <div className="bg-white rounded-2xl shadow-xl p-8 max-w-5xl mx-auto">
            <h3 className="text-2xl font-bold text-gray-800 mb-8">How It Works</h3>
            <div className="flex flex-col md:flex-row items-center justify-center gap-4 md:gap-6">
              <div className="flex flex-col items-center max-w-[200px]">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                  <i className="ri-edit-line text-3xl text-blue-600"></i>
                </div>
                <h4 className="font-semibold text-gray-800 mb-2">User Text Input</h4>
                <p className="text-sm text-gray-600 text-center">Express your feelings and thoughts freely</p>
              </div>
              <div className="flex items-center justify-center">
                <i className="ri-arrow-right-line md:text-3xl text-2xl text-teal-400 rotate-90 md:rotate-0"></i>
              </div>
              <div className="flex flex-col items-center max-w-[200px]">
                <div className="w-16 h-16 bg-teal-100 rounded-full flex items-center justify-center mb-4">
                  <i className="ri-brain-line text-3xl text-teal-600"></i>
                </div>
                <h4 className="font-semibold text-gray-800 mb-2">AI Emotion Detection</h4>
                <p className="text-sm text-gray-600 text-center">Advanced AI analyzes emotional patterns</p>
              </div>
              <div className="flex items-center justify-center">
                <i className="ri-arrow-right-line md:text-3xl text-2xl text-teal-400 rotate-90 md:rotate-0"></i>
              </div>
              <div className="flex flex-col items-center max-w-[200px]">
                <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mb-4">
                  <i className="ri-heart-pulse-line text-3xl text-purple-600"></i>
                </div>
                <h4 className="font-semibold text-gray-800 mb-2">Mental Health Insights</h4>
                <p className="text-sm text-gray-600 text-center">Detailed emotional state analysis</p>
              </div>
              <div className="flex items-center justify-center">
                <i className="ri-arrow-right-line md:text-3xl text-2xl text-teal-400 rotate-90 md:rotate-0"></i>
              </div>
              <div className="flex flex-col items-center max-w-[200px]">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4">
                  <i className="ri-lightbulb-line text-3xl text-green-600"></i>
                </div>
                <h4 className="font-semibold text-gray-800 mb-2">Lifestyle Support</h4>
                <p className="text-sm text-gray-600 text-center">Personalized wellness recommendations</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-6 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Comprehensive Mental Wellness Features</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Our AI-powered platform provides everything you need to monitor and improve your mental health
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="bg-gradient-to-br from-blue-50 to-teal-50 rounded-2xl p-8 hover:shadow-xl transition-shadow">
              <div className="w-14 h-14 bg-blue-600 rounded-lg flex items-center justify-center mb-6">
                <i className="ri-emotion-line text-2xl text-white"></i>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-3">Emotion Detection</h3>
              <p className="text-gray-600 leading-relaxed">
                Advanced AI algorithms analyze your text to detect emotions like sadness, fear, anger, and joy with high accuracy. 
                Understand your emotional state in real-time with detailed probability scores.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-gradient-to-br from-teal-50 to-green-50 rounded-2xl p-8 hover:shadow-xl transition-shadow">
              <div className="w-14 h-14 bg-teal-600 rounded-lg flex items-center justify-center mb-6">
                <i className="ri-line-chart-line text-2xl text-white"></i>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-3">Mental Health Trend Tracking</h3>
              <p className="text-gray-600 leading-relaxed">
                Monitor your stress, anxiety, and depression levels over time with intuitive charts and graphs. 
                Identify patterns and triggers to better understand your mental health journey.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-8 hover:shadow-xl transition-shadow">
              <div className="w-14 h-14 bg-purple-600 rounded-lg flex items-center justify-center mb-6">
                <i className="ri-heart-add-line text-2xl text-white"></i>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-3">Personalized Wellness Recommendations</h3>
              <p className="text-gray-600 leading-relaxed">
                Receive tailored lifestyle suggestions including breathing exercises, mindfulness techniques, 
                and daily wellness plans based on your detected emotional state.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="bg-gradient-to-br from-green-50 to-teal-50 rounded-2xl p-8 hover:shadow-xl transition-shadow">
              <div className="w-14 h-14 bg-green-600 rounded-lg flex items-center justify-center mb-6">
                <i className="ri-book-open-line text-2xl text-white"></i>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-3">Mood Journal</h3>
              <p className="text-gray-600 leading-relaxed">
                Keep track of your daily emotions with our secure mood journal. Review past entries and 
                see how your emotional state evolves over time with automatic emotion tagging.
              </p>
            </div>

            {/* Feature 5 */}
            <div className="bg-gradient-to-br from-orange-50 to-red-50 rounded-2xl p-8 hover:shadow-xl transition-shadow">
              <div className="w-14 h-14 bg-orange-600 rounded-lg flex items-center justify-center mb-6">
                <i className="ri-lightbulb-flash-line text-2xl text-white"></i>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-3">AI-Powered Insights</h3>
              <p className="text-gray-600 leading-relaxed">
                Get intelligent behavioral pattern analysis and predictive insights about your mental wellbeing. 
                Our AI identifies trends and provides actionable recommendations to improve your emotional health.
              </p>
            </div>

            {/* Feature 6 */}
            <div className="bg-gradient-to-br from-indigo-50 to-blue-50 rounded-2xl p-8 hover:shadow-xl transition-shadow">
              <div className="w-14 h-14 bg-indigo-600 rounded-lg flex items-center justify-center mb-6">
                <i className="ri-shield-check-line text-2xl text-white"></i>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-3">Privacy & Security</h3>
              <p className="text-gray-600 leading-relaxed">
                Your emotional data is encrypted and completely private. We prioritize your confidentiality 
                with industry-standard security measures to protect your sensitive information.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Mental Health Awareness Section */}
      <section className="py-20 px-6 bg-gradient-to-br from-teal-600 to-blue-600 text-white">
        <div className="max-w-5xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-6">Mental Health Awareness</h2>
          <p className="text-xl mb-8 leading-relaxed opacity-90">
            Mental health is just as important as physical health. Our platform provides emotional insights 
            and support, but it is not a substitute for professional medical diagnosis or treatment.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6">
              <div className="text-4xl font-bold mb-2">1 in 5</div>
              <p className="text-sm opacity-90">Adults experience mental illness each year</p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6">
              <div className="text-4xl font-bold mb-2">50%</div>
              <p className="text-sm opacity-90">Of mental health conditions begin by age 14</p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6">
              <div className="text-4xl font-bold mb-2">24/7</div>
              <p className="text-sm opacity-90">Support available through helplines</p>
            </div>
          </div>
          <div className="mt-12 p-6 bg-white/10 backdrop-blur-sm rounded-xl">
            <p className="text-sm font-medium mb-2">Important Notice</p>
            <p className="text-sm opacity-90">
              If you're experiencing a mental health crisis, please contact emergency services or a mental health professional immediately. 
              This platform is designed to provide insights and support, not emergency intervention.
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6 bg-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-6">
            Start Your Mental Wellness Journey Today
          </h2>
          <p className="text-xl text-gray-600 mb-10">
            Join thousands of users who are taking control of their mental health with AI-powered insights
          </p>
          <div className="flex items-center justify-center gap-4">
            <Link 
              to="/signup" 
              className="px-10 py-4 bg-teal-600 text-white rounded-lg font-medium hover:bg-teal-700 transition-all shadow-lg hover:shadow-xl text-lg whitespace-nowrap cursor-pointer"
            >
              Create Free Account
            </Link>
            <Link 
              to="/dashboard" 
              className="px-10 py-4 bg-white text-teal-600 border-2 border-teal-600 rounded-lg font-medium hover:bg-teal-50 transition-all text-lg whitespace-nowrap cursor-pointer"
            >
              Try Demo
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center gap-3 mb-4">
                <img 
                  src="https://public.readdy.ai/ai/img_res/85dcc970-73df-4a59-8d6d-8e5d7d2d3a0a.png" 
                  alt="MindCare AI Logo" 
                  className="w-8 h-8 object-contain"
                />
                <span className="text-lg font-semibold">MindCare AI</span>
              </div>
              <p className="text-sm text-gray-400">
                AI-powered mental wellness monitoring and support platform
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Platform</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors cursor-pointer">Features</a></li>
                <li><a href="#" className="hover:text-white transition-colors cursor-pointer">How It Works</a></li>
                <li><a href="#" className="hover:text-white transition-colors cursor-pointer">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-white transition-colors cursor-pointer">Terms of Service</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Support Resources</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors cursor-pointer">Mental Health Helplines</a></li>
                <li><a href="#" className="hover:text-white transition-colors cursor-pointer">Crisis Support</a></li>
                <li><a href="#" className="hover:text-white transition-colors cursor-pointer">Find a Therapist</a></li>
                <li><a href="#" className="hover:text-white transition-colors cursor-pointer">Resources</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Contact</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li className="flex items-center gap-2">
                  <i className="ri-mail-line"></i>
                  <span>support@mindcareai.com</span>
                </li>
                <li className="flex items-center gap-2">
                  <i className="ri-phone-line"></i>
                  <span>1-800-MINDCARE</span>
                </li>
                <li className="flex items-center gap-2">
                  <i className="ri-time-line"></i>
                  <span>24/7 Support Available</span>
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-8 text-center">
            <p className="text-sm text-gray-400">
              © 2026 MindCare AI. All rights reserved. This platform provides emotional insights but is not a medical diagnosis tool.
            </p>
            <div className="flex items-center justify-center gap-6 mt-4">
              <a href="#" className="text-gray-400 hover:text-white transition-colors cursor-pointer">
                <i className="ri-facebook-fill text-xl"></i>
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors cursor-pointer">
                <i className="ri-twitter-fill text-xl"></i>
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors cursor-pointer">
                <i className="ri-instagram-fill text-xl"></i>
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors cursor-pointer">
                <i className="ri-linkedin-fill text-xl"></i>
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
