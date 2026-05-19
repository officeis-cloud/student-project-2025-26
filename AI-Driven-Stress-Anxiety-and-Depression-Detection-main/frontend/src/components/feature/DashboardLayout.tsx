import { ReactNode, useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { getUserProfile } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';

interface DashboardLayoutProps {
  children: ReactNode;
}

const navItems = [
  { path: '/dashboard', label: 'Dashboard', icon: 'ri-dashboard-line' },
  { path: '/analyze', label: 'Emotion Analysis', icon: 'ri-brain-line' },
  { path: '/journal', label: 'Mood Journal', icon: 'ri-book-line' },
  { path: '/trends', label: 'Trend Analysis', icon: 'ri-line-chart-line' },
  { path: '/wellness', label: 'Wellness Plan', icon: 'ri-heart-pulse-line' },
  { path: '/profile', label: 'Profile', icon: 'ri-user-line' },
];

const pageTitles: Record<string, string> = {
  '/dashboard': 'Dashboard',
  '/analyze': 'Emotion Analysis',
  '/journal': 'Mood Journal',
  '/trends': 'Trend Analysis',
  '/wellness': 'Wellness Plan',
  '/profile': 'Profile',
};

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const location = useLocation();
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [avatarOpen, setAvatarOpen] = useState(false);
  const [animKey, setAnimKey] = useState(location.pathname);
  const [userData, setUserData] = useState({ name: 'User', email: 'user@mindcare.ai' });

  const pageTitle = pageTitles[location.pathname] ?? 'MindCare AI';

  // Handle logout
  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // Fetch user profile data
  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await getUserProfile();
        setUserData({
          name: response.user.name || 'User',
          email: response.user.email || 'user@mindcare.ai'
        });
      } catch (error) {
        console.error('Failed to fetch user data:', error);
      }
    };
    fetchUserData();
  }, []);

  // Get user initials for avatar
  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map((n) => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  const userInitials = getInitials(userData.name);
  const displayName = userData.name.split(' ')[0]; // First name only

  // Trigger page transition on route change
  useEffect(() => {
    setAnimKey(location.pathname);
    setMobileOpen(false);
  }, [location.pathname]);

  // Close dropdowns on outside click
  useEffect(() => {
    const handler = () => {
      setAvatarOpen(false);
    };
    document.addEventListener('click', handler);
    return () => document.removeEventListener('click', handler);
  }, []);

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden">

      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="fixed inset-0 bg-black/40 z-20 lg:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* ── Sidebar ── */}
      <aside
        className={`
          fixed lg:relative z-30 flex flex-col h-full bg-white border-r border-gray-200
          transition-all duration-300 ease-in-out
          ${collapsed ? 'w-[72px]' : 'w-64'}
          ${mobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        `}
      >
        {/* Logo */}
        <div className={`flex items-center border-b border-gray-200 h-16 px-4 ${collapsed ? 'justify-center' : 'gap-3'}`}>
          <Link to="/" className="flex items-center gap-3 cursor-pointer min-w-0">
            <div className="w-9 h-9 flex-shrink-0 bg-gradient-to-br from-teal-500 to-emerald-600 rounded-lg flex items-center justify-center shadow-sm">
              <i className="ri-heart-pulse-line text-white text-lg w-5 h-5 flex items-center justify-center"></i>
            </div>
            {!collapsed && (
              <div className="min-w-0">
                <h1 className="text-base font-bold text-gray-800 leading-tight whitespace-nowrap">MindCare AI</h1>
                <p className="text-[11px] text-gray-400 whitespace-nowrap">Mental Wellness</p>
              </div>
            )}
          </Link>
        </div>

        {/* Nav */}
        <nav className="flex-1 py-4 px-2 overflow-y-auto">
          <ul className="space-y-1">
            {navItems.map((item) => {
              const active = location.pathname === item.path;
              return (
                <li key={item.path}>
                  <Link
                    to={item.path}
                    title={collapsed ? item.label : undefined}
                    className={`
                      flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-150 cursor-pointer group relative
                      ${active ? 'bg-teal-50 text-teal-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-800'}
                    `}
                  >
                    <span className={`w-5 h-5 flex items-center justify-center flex-shrink-0 ${active ? 'text-teal-600' : ''}`}>
                      <i className={`${item.icon} text-lg`}></i>
                    </span>
                    {!collapsed && (
                      <span className="text-sm font-medium whitespace-nowrap">{item.label}</span>
                    )}
                    {active && !collapsed && (
                      <span className="ml-auto w-1.5 h-1.5 rounded-full bg-teal-500"></span>
                    )}
                    {/* Tooltip when collapsed */}
                    {collapsed && (
                      <span className="absolute left-full ml-3 px-2 py-1 bg-gray-800 text-white text-xs rounded-md whitespace-nowrap opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-50">
                        {item.label}
                      </span>
                    )}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* Collapse toggle + Logout */}
        <div className="p-2 border-t border-gray-200 space-y-1">
          <button
            onClick={() => setCollapsed((c) => !c)}
            title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
            className="w-full flex items-center gap-3 px-3 py-2.5 text-gray-500 hover:bg-gray-50 hover:text-gray-700 rounded-lg transition-colors cursor-pointer"
          >
            <span className="w-5 h-5 flex items-center justify-center flex-shrink-0">
              <i className={`${collapsed ? 'ri-arrow-right-s-line' : 'ri-arrow-left-s-line'} text-lg`}></i>
            </span>
            {!collapsed && <span className="text-sm font-medium whitespace-nowrap">Collapse</span>}
          </button>
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-3 py-2.5 text-gray-500 hover:bg-red-50 hover:text-red-600 rounded-lg transition-colors cursor-pointer"
          >
            <span className="w-5 h-5 flex items-center justify-center flex-shrink-0">
              <i className="ri-logout-box-line text-lg"></i>
            </span>
            {!collapsed && <span className="text-sm font-medium whitespace-nowrap">Logout</span>}
          </button>
        </div>
      </aside>

      {/* ── Right panel ── */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">

        {/* ── Top Header ── */}
        <header className="h-16 bg-white border-b border-gray-200 flex items-center px-4 md:px-6 gap-4 flex-shrink-0 z-10">
          {/* Mobile hamburger */}
          <button
            className="lg:hidden w-9 h-9 flex items-center justify-center text-gray-500 hover:bg-gray-100 rounded-lg cursor-pointer"
            onClick={() => setMobileOpen((o) => !o)}
          >
            <i className="ri-menu-line text-xl"></i>
          </button>

          {/* Page title */}
          <div className="flex-1 min-w-0">
            <h2 className="text-base md:text-lg font-semibold text-gray-800 truncate">{pageTitle}</h2>
            <p className="text-xs text-gray-400 hidden sm:block">
              {new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
            </p>
          </div>

          {/* Right actions */}
          <div className="flex items-center gap-2">

            {/* Avatar */}
            <div className="relative">
              <button
                onClick={(e) => { e.stopPropagation(); setAvatarOpen((o) => !o); }}
                className="flex items-center gap-2 pl-1 pr-2 py-1 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors"
              >
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-teal-400 to-emerald-500 flex items-center justify-center text-white text-sm font-bold flex-shrink-0">
                  {userInitials}
                </div>
                <span className="text-sm font-medium text-gray-700 hidden sm:block whitespace-nowrap">{displayName}</span>
                <i className="ri-arrow-down-s-line text-gray-400 hidden sm:block"></i>
              </button>

              {avatarOpen && (
                <div
                  className="absolute right-0 top-12 w-52 bg-white rounded-xl shadow-xl border border-gray-100 z-50 overflow-hidden"
                  onClick={(e) => e.stopPropagation()}
                >
                  <div className="px-4 py-3 border-b border-gray-100">
                    <p className="text-sm font-semibold text-gray-800">{userData.name}</p>
                    <p className="text-xs text-gray-400">{userData.email}</p>
                  </div>
                  <ul className="py-1">
                    <li>
                      <Link to="/profile" className="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 cursor-pointer">
                        <i className="ri-user-line text-gray-400"></i> My Profile
                      </Link>
                    </li>
                    <li>
                      <Link to="/wellness" className="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 cursor-pointer">
                        <i className="ri-settings-3-line text-gray-400"></i> Wellness Settings
                      </Link>
                    </li>
                  </ul>
                  <div className="border-t border-gray-100 py-1">
                    <button
                      onClick={handleLogout}
                      className="w-full flex items-center gap-2 px-4 py-2 text-sm text-red-600 hover:bg-red-50 cursor-pointer"
                    >
                      <i className="ri-logout-box-line"></i> Logout
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </header>

        {/* ── Page content with transition ── */}
        <main className="flex-1 overflow-y-auto">
          <div
            key={animKey}
            className="p-4 md:p-6 animate-fadeSlideIn"
          >
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
