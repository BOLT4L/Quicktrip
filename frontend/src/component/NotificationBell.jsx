
import { useState, useEffect } from "react"
import NotificationItem from "./NotificationItem"
import MessageItem from "./MessageItem"
import api from "../api"
import { USER_ID } from "../constants"

const NotificationBell = () => {
  const [showDropdown, setShowDropdown] = useState(false)
  const [activeTab, setActiveTab] = useState("notifications")
  const [notifications, setNotifications] = useState([])
  const [staff, setStaff] = useState([])
  const [conversation , setConversation] = useState([])
  const id = localStorage.getItem(USER_ID);
  useEffect(()=>{
    getSubadmin()
    getNotification()
    getMessages()
  },[])
  const getNotification = () => {
    api
      .get(`api/ad_notif/${id}`)
      .then((res) => res.data)
      .then((data) => {
        setNotifications(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };
  const getSubadmin = () => {
    api
      .get(`api/staffs/`)
      .then((res) => res.data)
      .then((data) => {
        setStaff(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };
  const getMessages = () => {
    api
      .get(`api/messages/${id}`)
      .then((res) => res.data)
      .then((data) => {
        setConversation(data);
        const convos = {};
        data.forEach(msg => {
          const otherUserId = msg.sender.id === parseInt(id) ? msg.receiver.id : msg.sender.id;
          if (!convos[otherUserId]) {
            convos[otherUserId] = [];
          }
          convos[otherUserId].push(msg);
        });
        setConversations(convos);
      })
      .catch((err) => alert(err));
  };

  const [subAdmins, setSubAdmins] = useState([
    {
      id: 1,
      name: "eyob belayneh",
      avatar: null,
      lastMessage: "When will the new system update be released?",
      time: "5 min ago",
      unread: true,
    },
    {
      id: 2,
      name: "kidus asrat",
      avatar: null,
      lastMessage: "I've completed the vehicle inspections for today",
      time: "2 hours ago",
      unread: false,
    },
    {
      id: 3,
      name: "eden",
      avatar: null,
      lastMessage: "Thanks for the information",
      time: "Yesterday",
      unread: false,
    },
  ])

  const [selectedSubAdmin, setSelectedSubAdmin] = useState(null)
  const [messageText, setMessageText] = useState("")
  const [conversations, setConversations] = useState({
    1: [
      { id: 1, text: "Hello, I have a question about the system update", time: "5:30 PM", sender: 1 },
      { id: 2, text: "Sure, what would you like to know?", time: "5:32 PM", sender: "admin" },
      { id: 3, text: "When will the new system update be released?", time: "5:33 PM", sender: 1 },
    ],
    2: [
      { id: 1, text: "I've completed all vehicle inspections for today", time: "3:15 PM", sender: 2 },
      { id: 2, text: "Great job! Any issues to report?", time: "3:20 PM", sender: "admin" },
      { id: 3, text: "No issues, everything went smoothly", time: "3:22 PM", sender: 2 },
      { id: 4, text: "I've completed the vehicle inspections for today", time: "4:45 PM", sender: 2 },
    ],
    3: [
      { id: 1, text: "Welcome to the team, Emily!", time: "Yesterday, 10:00 AM", sender: "admin" },
      { id: 2, text: "Thank you! I'm excited to join", time: "Yesterday, 10:05 AM", sender: 3 },
      { id: 3, text: "Let me know if you need any help getting started", time: "Yesterday, 10:10 AM", sender: "admin" },
      { id: 4, text: "Thanks for the information", time: "Yesterday, 2:30 PM", sender: 3 },
    ],
  })

  const unreadNotificationsCount = notifications.filter((n) => !n.read).length
  const unreadMessagesCount = subAdmins.filter((sa) => sa.unread).length
  const totalUnreadCount = unreadNotificationsCount + unreadMessagesCount

  const toggleDropdown = () => {
    setShowDropdown(!showDropdown)
    if (selectedSubAdmin) {
      setSelectedSubAdmin(null)
    }
  }

  const handleMarkAsRead = (id) => {
    try {
      const res =  api.put(`api/ad_notifs/${id}`, {
        read : true
      });
      if (res.status === 201) {
        setNotifications(
          notifications.map((notification) => (notification.id === id ? { ...notification, read: true } : notification)),
        )
      }
    } catch (error) {
      alert(error);
    } finally {
    }
  
  }

  const handleMarkAllAsRead = () => {
    setNotifications(notifications.map((n) => ({ ...n, read: true })))
  }

  const selectSubAdmin = (id) => {
    setSelectedSubAdmin(id)
    // Mark messages as read when conversation is opened
    setSubAdmins(subAdmins.map((sa) => (sa.id === id ? { ...sa, unread: false } : sa)))
  }

  const sendMessage = () => {
    if (!messageText.trim() || !selectedSubAdmin) return

    const newMessage = {
      id: conversations[selectedSubAdmin].length + 1,
      text: messageText,
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      sender: "admin",
    }

    setConversations({
      ...conversations,
      [selectedSubAdmin]: [...conversations[selectedSubAdmin], newMessage],
    })

    setMessageText("")
  }

  return (
    <div className="notification-bell-container">
      <button
        className={`notification-bell ${totalUnreadCount > 0 ? "has-notifications" : ""}`}
        onClick={toggleDropdown}
        aria-label="Notifications"
      >
        <span className="bell-icon">🔔</span>
        {totalUnreadCount > 0 && <span className="notification-badge">{totalUnreadCount}</span>}
      </button>

      {showDropdown && (
        <div className="notification-dropdown">
          {!selectedSubAdmin ? (
            <>
              <div className="notification-header">
                <div className="tabs">
                  <button
                    className={`tab ${activeTab === "notifications" ? "active" : ""}`}
                    onClick={() => setActiveTab("notifications")}
                  >
                    Notifications
                    {unreadNotificationsCount > 0 && <span className="tab-badge">{unreadNotificationsCount}</span>}
                  </button>
                  <button
                    className={`tab ${activeTab === "messages" ? "active" : ""}`}
                    onClick={() => setActiveTab("messages")}
                  >
                    Messages
                    {unreadMessagesCount > 0 && <span className="tab-badge">{unreadMessagesCount}</span>}
                  </button>
                </div>

                {activeTab === "notifications" && unreadNotificationsCount > 0 && (
                  <button className="mark-all-read" onClick={handleMarkAllAsRead}>
                    Mark all as read
                  </button>
                )}
              </div>

              <div className="notification-body">
                {activeTab === "notifications" ? (
                  notifications.length > 0 ? (
                    <div className="notification-list">
                      {notifications.map((notification) => (
                        <NotificationItem
                          key={notification.id}
                          notification={notification}
                          onMarkAsRead={handleMarkAsRead}
                        />
                      ))}
                    </div>
                  ) : (
                    <div className="empty-state">No notifications</div>
                  )
                ) : subAdmins.length > 0 ? (
                  <div className="sub-admin-list">
                    {subAdmins.map((subAdmin) => (
                      <div
                        key={subAdmin.id}
                        className={`sub-admin-item ${subAdmin.unread ? "unread" : ""}`}
                        onClick={() => selectSubAdmin(subAdmin.id)}
                      >
                        <div className="sub-admin-avatar">
                          {subAdmin.avatar ? (
                            <img src={subAdmin.avatar || "/placeholder.svg"} alt={subAdmin.name} />
                          ) : (
                            <div className="avatar-placeholder">{subAdmin.name.charAt(0)}</div>
                          )}
                        </div>
                        <div className="sub-admin-info">
                          <div className="sub-admin-name">{subAdmin.name}</div>
                          <div className="sub-admin-message">{subAdmin.lastMessage}</div>
                        </div>
                        <div className="sub-admin-time">{subAdmin.time}</div>
                        {subAdmin.unread && <div className="unread-indicator"></div>}
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="empty-state">No messages</div>
                )}
              </div>

              <div className="notification-footer">
                <a href="#" className="view-all">
                  {activeTab === "notifications" ? "View all notifications" : "View all messages"}
                </a>
              </div>
            </>
          ) : (
            <div className="message-view">
              <div className="message-header">
                <button className="back-button" onClick={() => setSelectedSubAdmin(null)}>
                  ←
                </button>
                <div className="message-recipient">{subAdmins.find((sa) => sa.id === selectedSubAdmin)?.name}</div>
              </div>

              <div className="message-body">
                {conversations[selectedSubAdmin].map((message) => (
                  <MessageItem key={message.id} message={message} isCurrentUser={message.sender === "admin"} />
                ))}
              </div>

              <div className="message-footer">
                <input
                  type="text"
                  className="message-input"
                  placeholder="Type a message..."
                  value={messageText}
                  onChange={(e) => setMessageText(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && sendMessage()}
                />
                <button className="send-button" onClick={sendMessage}>
                  Send
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      <style jsx>{`
        .notification-bell-container {
          position: relative;
        }
        
        .notification-bell {
          background: none;
          border: none;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          width: 36px;
          height: 36px;
          border-radius: 50%;
          position: relative;
          transition: background-color 0.2s;
        }
        
        .notification-bell:hover {
          background-color: var(--hover-bg);
        }
        
        .bell-icon {
          font-size: 1.2rem;
        }
        
        .has-notifications .bell-icon {
          animation: bell-shake 0.5s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
          animation-iteration-count: 1;
        }
        
        @keyframes bell-shake {
          0% { transform: rotate(0); }
          15% { transform: rotate(5deg); }
          30% { transform: rotate(-5deg); }
          45% { transform: rotate(4deg); }
          60% { transform: rotate(-4deg); }
          75% { transform: rotate(2deg); }
          85% { transform: rotate(-2deg); }
          92% { transform: rotate(1deg); }
          100% { transform: rotate(0); }
        }
        
        .notification-badge {
          position: absolute;
          top: 0;
          right: 0;
          background-color: var(--danger-color);
          color: white;
          border-radius: 50%;
          width: 18px;
          height: 18px;
          font-size: 0.7rem;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: bold;
        }
        
        .notification-dropdown {
          position: absolute;
          top: 100%;
          right: 0;
          width: 320px;
          background-color: var(--bg-primary);
          border-radius: 8px;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
          margin-top: 10px;
          z-index: 1000;
          overflow: hidden;
          display: flex;
          flex-direction: column;
          max-height: 500px;
        }
        
        .notification-header {
          padding: 15px;
          border-bottom: 1px solid var(--border-color);
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        
        .tabs {
          display: flex;
          gap: 10px;
        }
        
        .tab {
          background: none;
          border: none;
          padding: 5px 10px;
          cursor: pointer;
          font-weight: 500;
          color: var(--text-secondary);
          position: relative;
          transition: color 0.2s;
        }
        
        .tab.active {
          color: var(--primary-color);
        }
        
        .tab-badge {
          position: absolute;
          top: -5px;
          right: -5px;
          background-color: var(--danger-color);
          color: white;
          border-radius: 50%;
          width: 16px;
          height: 16px;
          font-size: 0.7rem;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        
        .mark-all-read {
          background: none;
          border: none;
          color: var(--primary-color);
          font-size: 0.8rem;
          cursor: pointer;
        }
        
        .notification-body {
          flex: 1;
          overflow-y: auto;
        }
        
        .empty-state {
          padding: 30px;
          text-align: center;
          color: var(--text-light);
        }
        
        .notification-footer {
          padding: 10px 15px;
          border-top: 1px solid var(--border-color);
          text-align: center;
        }
        
        .view-all {
          color: var(--primary-color);
          text-decoration: none;
          font-size: 0.9rem;
        }
        
        .sub-admin-list {
          display: flex;
          flex-direction: column;
        }
        
        .sub-admin-item {
          display: flex;
          align-items: center;
          padding: 12px 15px;
          border-bottom: 1px solid var(--border-color);
          cursor: pointer;
          position: relative;
          transition: background-color 0.2s;
        }
        
        .sub-admin-item:hover {
          background-color: var(--hover-bg);
        }
        
        .sub-admin-item.unread {
          background-color: var(--unread-bg);
        }
        
        .sub-admin-avatar {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          overflow: hidden;
          margin-right: 10px;
          flex-shrink: 0;
        }
        
        .sub-admin-avatar img {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }
        
        .avatar-placeholder {
          width: 100%;
          height: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          background-color: var(--primary-color);
          color: white;
          font-weight: bold;
        }
        
        .sub-admin-info {
          flex: 1;
          min-width: 0;
        }
        
        .sub-admin-name {
          font-weight: 600;
          margin-bottom: 3px;
        }
        
        .sub-admin-message {
          font-size: 0.85rem;
          color: var(--text-secondary);
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        
        .sub-admin-time {
          font-size: 0.75rem;
          color: var(--text-light);
          margin-left: 10px;
        }
        
        .unread-indicator {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background-color: var(--primary-color);
          position: absolute;
          top: 50%;
          right: 15px;
          transform: translateY(-50%);
        }
        
        .message-view {
          display: flex;
          flex-direction: column;
          height: 100%;
          max-height: 500px;
        }
        
        .message-header {
          padding: 15px;
          border-bottom: 1px solid var(--border-color);
          display: flex;
          align-items: center;
        }
        
        .back-button {
          background: none;
          border: none;
          font-size: 1.2rem;
          cursor: pointer;
          margin-right: 10px;
          color: var(--text-primary);
        }
        
        .message-recipient {
          font-weight: 600;
        }
        
        .message-body {
          flex: 1;
          overflow-y: auto;
          padding: 15px;
          display: flex;
          flex-direction: column;
        }
        
        .message-footer {
          padding: 10px 15px;
          border-top: 1px solid var(--border-color);
          display: flex;
          gap: 10px;
        }
        
        .message-input {
          flex: 1;
          padding: 8px 12px;
          border: 1px solid var(--border-color);
          border-radius: 20px;
          outline: none;
          background-color: var(--input-bg);
          color: var(--text-primary);
        }
        
        .message-input:focus {
          border-color: var(--primary-color);
        }
        
        .send-button {
          background-color: var(--primary-color);
          color: white;
          border: none;
          border-radius: 20px;
          padding: 8px 15px;
          cursor: pointer;
          font-weight: 500;
        }
        
        .send-button:hover {
          background-color: var(--primary-hover);
        }
        
        @media (max-width: 576px) {
          .notification-dropdown {
            width: 300px;
            right: -100%;
          }
        }
        
        @media (max-width: 480px) {
          .notification-dropdown {
            width: 280px;
            right: -120%;
          }
          
          .notification-header {
            padding: 10px;
          }
          
          .mark-all-read {
            font-size: 0.7rem;
          }
        }
      `}</style>
    </div>
  )
}

export default NotificationBell

