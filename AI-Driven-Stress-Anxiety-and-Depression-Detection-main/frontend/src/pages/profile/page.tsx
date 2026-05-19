import { useState, useEffect } from 'react';
import DashboardLayout from '../../components/feature/DashboardLayout';
import { getJournalHistory, getUserProfile, updateUserProfile, changePassword, deleteAccount } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function ProfilePage() {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);
  const [showPasswordSuccess, setShowPasswordSuccess] = useState(false);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalEntries: 0,
    memberSince: 'Loading...',
  });

  // User data state - fetched from MongoDB
  const [userData, setUserData] = useState({
    name: '',
    email: '',
  });

  // Password state
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });

  // Fetch real user profile and stats from backend
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch user profile
        const profileResponse = await getUserProfile();
        setUserData({
          name: profileResponse.user.name,
          email: profileResponse.user.email,
        });
        
        // Fetch journal stats
        const journalResponse = await getJournalHistory(1, 1000);
        const entries = journalResponse.entries;
        
        // Get member since date from user profile or oldest entry
        let memberSince = 'Loading...';
        if (profileResponse.user.created_at) {
          const dateObj = new Date(profileResponse.user.created_at);
          memberSince = dateObj.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long' 
          });
        } else if (entries.length > 0) {
          const oldestEntry = entries[entries.length - 1];
          const dateObj = new Date(oldestEntry.created_at);
          memberSince = dateObj.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long' 
          });
        }
        
        setStats({
          totalEntries: journalResponse.total,
          memberSince,
        });
      } catch (error) {
        console.error('Failed to fetch profile data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await updateUserProfile({
        name: userData.name,
        email: userData.email,
      });
      setShowSuccessMessage(true);
      setTimeout(() => setShowSuccessMessage(false), 3000);
    } catch (error) {
      console.error('Failed to update profile:', error);
      alert('Failed to update profile. Please try again.');
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate new password and confirm password match
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      alert('New passwords do not match');
      return;
    }
    
    // Validate password length
    if (passwordData.newPassword.length < 6) {
      alert('New password must be at least 6 characters long');
      return;
    }
    
    try {
      // Call backend to change password
      await changePassword(passwordData.currentPassword, passwordData.newPassword);
      
      // Success - clear form and show message
      setShowPasswordSuccess(true);
      setPasswordData({
        currentPassword: '',
        newPassword: '',
        confirmPassword: '',
      });
      setTimeout(() => setShowPasswordSuccess(false), 3000);
    } catch (error: any) {
      // Handle errors
      const errorMessage = error?.response?.data?.error || error?.message || 'Failed to change password';
      alert(errorMessage);
    }
  };

  const handleDeleteAccount = async () => {
    try {
      await deleteAccount();
      
      // Close modal
      setShowDeleteModal(false);
      
      // Logout and redirect to home
      logout();
      navigate('/');
    } catch (error: any) {
      setShowDeleteModal(false);
      const errorMessage = error?.response?.data?.error || error?.message || 'Failed to delete account';
      alert(errorMessage);
    }
  };

  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map((n) => n[0])
      .join('')
      .toUpperCase();
  };

  return (
    <DashboardLayout>
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto p-6">
          {/* Header */}
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Profile Settings</h1>
            <p className="text-gray-600">Manage your account information and preferences</p>
          </div>

          {loading ? (
            <div className="flex justify-center items-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-500"></div>
            </div>
          ) : (
            <>
              {/* Profile Header Card */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-5">
                <div className="flex items-center gap-6">
                  <div className="w-20 h-20 bg-gradient-to-br from-teal-500 to-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-2xl font-bold text-white">{getInitials(userData.name)}</span>
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold text-gray-800">{userData.name}</h2>
                    <p className="text-gray-600 mt-1">{userData.email}</p>
                    <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                      <span>Member since {stats.memberSince}</span>
                      <span>•</span>
                      <span>{stats.totalEntries} journal entries</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Success Message */}
              {showSuccessMessage && (
                <div className="bg-teal-50 border border-teal-200 rounded-lg p-4 mb-5 flex items-center gap-3">
                  <i className="ri-checkbox-circle-line text-teal-600 text-xl w-6 h-6 flex items-center justify-center"></i>
                  <span className="text-teal-800 font-medium">Profile updated successfully!</span>
                </div>
              )}

              {/* Personal Information */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-5">
                <h3 className="text-xl font-bold text-gray-800 mb-5">Personal Information</h3>
                <form onSubmit={handleSaveProfile}>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Full Name
                      </label>
                      <input
                        type="text"
                        value={userData.name}
                        onChange={(e) => setUserData({ ...userData, name: e.target.value })}
                        className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent outline-none transition-all"
                        placeholder="Enter your full name"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Email Address
                      </label>
                      <input
                        type="email"
                        value={userData.email}
                        onChange={(e) => setUserData({ ...userData, email: e.target.value })}
                        className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent outline-none transition-all"
                        placeholder="Enter your email"
                      />
                    </div>
                  </div>
                  <button
                    type="submit"
                    className="mt-5 px-6 py-2.5 bg-teal-600 text-white font-medium rounded-lg hover:bg-teal-700 transition-colors whitespace-nowrap cursor-pointer"
                  >
                    Save Changes
                  </button>
                </form>
              </div>

              {/* Change Password */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-5">
                <h3 className="text-xl font-bold text-gray-800 mb-5">Change Password</h3>
                {showPasswordSuccess && (
                  <div className="bg-teal-50 border border-teal-200 rounded-lg p-4 mb-5 flex items-center gap-3">
                    <i className="ri-checkbox-circle-line text-teal-600 text-xl w-6 h-6 flex items-center justify-center"></i>
                    <span className="text-teal-800 font-medium">Password changed successfully!</span>
                  </div>
                )}
                <form onSubmit={handleChangePassword}>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Current Password
                      </label>
                      <input
                        type="password"
                        value={passwordData.currentPassword}
                        onChange={(e) =>
                          setPasswordData({ ...passwordData, currentPassword: e.target.value })
                        }
                        className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent outline-none transition-all"
                        placeholder="Enter current password"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        New Password
                      </label>
                      <input
                        type="password"
                        value={passwordData.newPassword}
                        onChange={(e) =>
                          setPasswordData({ ...passwordData, newPassword: e.target.value })
                        }
                        className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent outline-none transition-all"
                        placeholder="Enter new password"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Confirm New Password
                      </label>
                      <input
                        type="password"
                        value={passwordData.confirmPassword}
                        onChange={(e) =>
                          setPasswordData({ ...passwordData, confirmPassword: e.target.value })
                        }
                        className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent outline-none transition-all"
                        placeholder="Confirm new password"
                        required
                      />
                    </div>
                  </div>
                  <button
                    type="submit"
                    className="mt-5 px-6 py-2.5 bg-teal-600 text-white font-medium rounded-lg hover:bg-teal-700 transition-colors whitespace-nowrap cursor-pointer"
                  >
                    Update Password
                  </button>
                </form>
              </div>

              {/* Danger Zone */}
              <div className="bg-white rounded-xl shadow-sm border border-red-200 p-6">
                <h3 className="text-xl font-bold text-red-600 mb-2">Danger Zone</h3>
                <p className="text-gray-600 mb-5">
                  Once you delete your account, there is no going back. Please be certain.
                </p>
                <button
                  onClick={() => setShowDeleteModal(true)}
                  className="px-6 py-2.5 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 transition-colors whitespace-nowrap cursor-pointer"
                >
                  Delete Account
                </button>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-2xl max-w-md w-full p-6">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <i className="ri-alert-line text-red-600 text-3xl w-8 h-8 flex items-center justify-center"></i>
            </div>
            <h3 className="text-2xl font-bold text-gray-800 text-center mb-3">
              Delete Account?
            </h3>
            <p className="text-gray-600 text-center mb-6">
              This action cannot be undone. All your data, including journal entries and emotional
              insights, will be permanently deleted.
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => setShowDeleteModal(false)}
                className="flex-1 px-6 py-2.5 bg-gray-100 text-gray-700 font-medium rounded-lg hover:bg-gray-200 transition-colors whitespace-nowrap cursor-pointer"
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteAccount}
                className="flex-1 px-6 py-2.5 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 transition-colors whitespace-nowrap cursor-pointer"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </DashboardLayout>
  );
}