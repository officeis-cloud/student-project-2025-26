import { lazy } from 'react';
import { RouteObject } from 'react-router-dom';

const HomePage = lazy(() => import('../pages/home/page'));
const LoginPage = lazy(() => import('../pages/login/page'));
const SignupPage = lazy(() => import('../pages/signup/page'));
const DashboardPage = lazy(() => import('../pages/dashboard/page'));
const AnalyzePage = lazy(() => import('../pages/analyze/page'));
const JournalPage = lazy(() => import('../pages/journal/page'));
const TrendsPage = lazy(() => import('../pages/trends/page'));
const WellnessPage = lazy(() => import('../pages/wellness/page'));
const ProfilePage = lazy(() => import('../pages/profile/page'));
const NotFound = lazy(() => import('../pages/NotFound'));

const routes: RouteObject[] = [
  {
    path: '/',
    element: <HomePage />,
  },
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/signup',
    element: <SignupPage />,
  },
  {
    path: '/dashboard',
    element: <DashboardPage />,
  },
  {
    path: '/analyze',
    element: <AnalyzePage />,
  },
  {
    path: '/journal',
    element: <JournalPage />,
  },
  {
    path: '/trends',
    element: <TrendsPage />,
  },
  {
    path: '/wellness',
    element: <WellnessPage />,
  },
  {
    path: '/profile',
    element: <ProfilePage />,
  },
  {
    path: '*',
    element: <NotFound />,
  },
];

export default routes;