import React, { useState } from 'react';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import { 
  FaUsers, 
  FaPlus, 
  FaSearch, 
  FaComments, 
  FaLeaf,
  FaRecycle,
  FaBicycle,
  FaSolarPanel,
  FaTree,
  FaWater,
  FaCrown,
  FaUserShield,
  FaUser,
  FaCalendarAlt,
  FaTasks,
  FaMapMarkerAlt,
  FaGlobe
} from 'react-icons/fa';
import './Community.css';

// Mock community data
const mockCommunities = [
  {
    id: 1,
    name: 'Urban Gardeners',
    description: 'Growing green spaces in cities, one plant at a time',
    category: 'gardening',
    members: 1245,
    icon: <FaTree />,
    location: 'Global',
    activities: ['Community Gardens', 'Seed Swaps', 'Workshops'],
    joined: true,
  },
  {
    id: 2,
    name: 'Zero Waste Warriors',
    description: 'Committed to reducing waste and living sustainably',
    category: 'recycling',
    members: 2890,
    icon: <FaRecycle />,
    location: 'Worldwide',
    activities: ['Beach Cleanups', 'Recycling Drives', 'DIY Workshops'],
    joined: false,
  },
  {
    id: 3,
    name: 'Bike to Work Club',
    description: 'Promoting cycling as a sustainable commute option',
    category: 'transport',
    members: 567,
    icon: <FaBicycle />,
    location: 'City-wide',
    activities: ['Group Rides', 'Bike Maintenance', 'Advocacy'],
    joined: true,
  },
  {
    id: 4,
    name: 'Solar Enthusiasts',
    description: 'Advancing renewable energy adoption in homes',
    category: 'energy',
    members: 834,
    icon: <FaSolarPanel />,
    location: 'National',
    activities: ['Solar Installs', 'Energy Audits', 'Education'],
    joined: false,
  },
  {
    id: 5,
    name: 'Water Conservation League',
    description: 'Protecting our most precious resource',
    category: 'conservation',
    members: 1567,
    icon: <FaWater />,
    location: 'Regional',
    activities: ['River Cleanups', 'Rain Harvesting', 'Awareness'],
    joined: false,
  },
];

// Mock roles in communities
const communityRoles = [
  { id: 1, name: 'Community Leader', icon: <FaCrown />, responsibilities: ['Manage community', 'Organize events', 'Moderate discussions'] },
  { id: 2, name: 'Event Coordinator', icon: <FaCalendarAlt />, responsibilities: ['Plan activities', 'Schedule events', 'Send reminders'] },
  { id: 3, name: 'Moderator', icon: <FaUserShield />, responsibilities: ['Monitor chat', 'Enforce guidelines', 'Help members'] },
  { id: 4, name: 'Member', icon: <FaUser />, responsibilities: ['Participate', 'Contribute ideas', 'Support initiatives'] },
];

const Community = () => {
  const [activeTab, setActiveTab] = useState('discover');
  const [searchQuery, setSearchQuery] = useState('');
  const [filterCategory, setFilterCategory] = useState('all');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [selectedCommunity, setSelectedCommunity] = useState(null);
  
  const [newCommunity, setNewCommunity] = useState({
    name: '',
    description: '',
    category: 'general',
    location: '',
  });

  const filteredCommunities = mockCommunities.filter(community => {
    const matchesSearch = community.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         community.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = filterCategory === 'all' || community.category === filterCategory;
    const matchesTab = activeTab === 'discover' ? true : (activeTab === 'my-communities' ? community.joined : true);
    
    return matchesSearch && matchesCategory && matchesTab;
  });

  const handleCreateCommunity = () => {
    // TODO: API call to create community
    console.log('Creating community:', newCommunity);
    setShowCreateModal(false);
    setNewCommunity({ name: '', description: '', category: 'general', location: '' });
    alert('Community created successfully! You\'ve earned the "Community Founder" badge!');
  };

  const handleJoinCommunity = (communityId) => {
    // TODO: API call to join community
    console.log('Joining community:', communityId);
    alert('Successfully joined the community!');
  };

  const handleLeaveCommunity = (communityId) => {
    // TODO: API call to leave community
    console.log('Leaving community:', communityId);
    alert('You have left the community.');
  };

  const openCommunityDetails = (community) => {
    setSelectedCommunity(community);
  };

  return (
    <div className="community-page">
      <Navbar />
      <main className="community-content">
        <header className="community-header">
          <div className="header-content">
            <h1><FaUsers /> Communities</h1>
            <p>Connect with like-minded people and take action together</p>
          </div>
          <button className="btn-create-community" onClick={() => setShowCreateModal(true)}>
            <FaPlus /> Create Community
          </button>
        </header>

        {/* Tabs */}
        <div className="community-tabs">
          <button
            className={`tab ${activeTab === 'discover' ? 'active' : ''}`}
            onClick={() => setActiveTab('discover')}
          >
            <FaGlobe /> Discover
          </button>
          <button
            className={`tab ${activeTab === 'my-communities' ? 'active' : ''}`}
            onClick={() => setActiveTab('my-communities')}
          >
            <FaUsers /> My Communities
          </button>
        </div>

        {/* Search and Filter */}
        <div className="search-filter-section">
          <div className="search-bar">
            <FaSearch />
            <input
              type="text"
              placeholder="Search communities..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <select
            className="category-filter"
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
          >
            <option value="all">All Categories</option>
            <option value="gardening">Gardening</option>
            <option value="recycling">Recycling</option>
            <option value="transport">Transport</option>
            <option value="energy">Energy</option>
            <option value="conservation">Conservation</option>
          </select>
        </div>

        {/* Communities Grid */}
        <div className="communities-grid">
          {filteredCommunities.map((community) => (
            <div key={community.id} className="community-card">
              <div className="community-icon">{community.icon}</div>
              <div className="community-info">
                <h3>{community.name}</h3>
                <p className="community-description">{community.description}</p>
                <div className="community-meta">
                  <span className="members">
                    <FaUsers /> {community.members.toLocaleString()} members
                  </span>
                  <span className="location">
                    <FaMapMarkerAlt /> {community.location}
                  </span>
                </div>
                <div className="community-activities">
                  {community.activities.slice(0, 3).map((activity, index) => (
                    <span key={index} className="activity-tag">{activity}</span>
                  ))}
                </div>
              </div>
              <div className="community-actions">
                {community.joined ? (
                  <>
                    <button
                      className="btn btn-primary btn-open"
                      onClick={() => openCommunityDetails(community)}
                    >
                      <FaComments /> Open
                    </button>
                    <button
                      className="btn btn-secondary btn-leave"
                      onClick={() => handleLeaveCommunity(community.id)}
                    >
                      Leave
                    </button>
                  </>
                ) : (
                  <button
                    className="btn btn-primary btn-join"
                    onClick={() => handleJoinCommunity(community.id)}
                  >
                    <FaPlus /> Join Community
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>

        {filteredCommunities.length === 0 && (
          <div className="empty-state">
            <FaUsers className="empty-icon" />
            <h3>No communities found</h3>
            <p>Try adjusting your search or create a new community!</p>
          </div>
        )}

        {/* Create Community Modal */}
        {showCreateModal && (
          <div className="modal-overlay" onClick={() => setShowCreateModal(false)}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <h2><FaPlus /> Create New Community</h2>
                <button className="close-btn" onClick={() => setShowCreateModal(false)}>×</button>
              </div>
              <form onSubmit={(e) => { e.preventDefault(); handleCreateCommunity(); }}>
                <div className="form-group">
                  <label htmlFor="communityName">Community Name *</label>
                  <input
                    type="text"
                    id="communityName"
                    value={newCommunity.name}
                    onChange={(e) => setNewCommunity({ ...newCommunity, name: e.target.value })}
                    placeholder="e.g., Eco Warriors"
                    required
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="communityDescription">Description *</label>
                  <textarea
                    id="communityDescription"
                    value={newCommunity.description}
                    onChange={(e) => setNewCommunity({ ...newCommunity, description: e.target.value })}
                    placeholder="Tell people what your community is about..."
                    rows="4"
                    required
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="communityCategory">Category *</label>
                  <select
                    id="communityCategory"
                    value={newCommunity.category}
                    onChange={(e) => setNewCommunity({ ...newCommunity, category: e.target.value })}
                    required
                  >
                    <option value="general">General</option>
                    <option value="gardening">Gardening</option>
                    <option value="recycling">Recycling</option>
                    <option value="transport">Transport</option>
                    <option value="energy">Energy</option>
                    <option value="conservation">Conservation</option>
                  </select>
                </div>
                <div className="form-group">
                  <label htmlFor="communityLocation">Location *</label>
                  <input
                    type="text"
                    id="communityLocation"
                    value={newCommunity.location}
                    onChange={(e) => setNewCommunity({ ...newCommunity, location: e.target.value })}
                    placeholder="e.g., Global, New York, Online"
                    required
                  />
                </div>
                <div className="modal-actions">
                  <button type="button" className="btn btn-secondary" onClick={() => setShowCreateModal(false)}>
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary">
                    Create Community
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Community Details Modal */}
        {selectedCommunity && (
          <div className="modal-overlay" onClick={() => setSelectedCommunity(null)}>
            <div className="modal-content community-details-modal" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <div className="header-with-icon">
                  <div className="large-icon">{selectedCommunity.icon}</div>
                  <div>
                    <h2>{selectedCommunity.name}</h2>
                    <p className="members-count">{selectedCommunity.members.toLocaleString()} members</p>
                  </div>
                </div>
                <button className="close-btn" onClick={() => setSelectedCommunity(null)}>×</button>
              </div>

              <div className="community-details-content">
                <section className="details-section">
                  <h3>About</h3>
                  <p>{selectedCommunity.description}</p>
                  <div className="meta-info">
                    <span><FaMapMarkerAlt /> {selectedCommunity.location}</span>
                  </div>
                </section>

                <section className="details-section">
                  <h3><FaTasks /> Activities</h3>
                  <div className="activities-list">
                    {selectedCommunity.activities.map((activity, index) => (
                      <div key={index} className="activity-item">
                        <FaLeaf />
                        <span>{activity}</span>
                      </div>
                    ))}
                  </div>
                </section>

                <section className="details-section">
                  <h3><FaUserShield /> Roles & Responsibilities</h3>
                  <div className="roles-grid">
                    {communityRoles.map((role) => (
                      <div key={role.id} className="role-card">
                        <div className="role-header">
                          <span className="role-icon">{role.icon}</span>
                          <h4>{role.name}</h4>
                        </div>
                        <ul className="responsibilities">
                          {role.responsibilities.map((resp, index) => (
                            <li key={index}>{resp}</li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </section>

                <section className="details-section chat-section">
                  <h3><FaComments /> Community Chat</h3>
                  <div className="chat-preview">
                    <p className="chat-notice">
                      💬 Join the conversation! Connect with members, share ideas, and coordinate activities.
                    </p>
                    <button className="btn btn-primary btn-full">
                      <FaComments /> Open Group Chat
                    </button>
                  </div>
                </section>
              </div>
            </div>
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
};

export default Community;
