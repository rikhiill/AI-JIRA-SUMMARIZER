/**
 * Dashboard.js
 * -------------------------
 * 📌 This is the main dashboard of the AI-based Jira Summarizer project.
 * ✅ Features:
 *   - Smart summary of tasks
 *   - Editable AI-generated summaries
 *   - Search, filter, pagination
 *   - Raw Jira fields expandable view
 *   - Report download (PDF, CSV, etc.)
 *   - Theme toggle and login session handling
 * Author: Rikhil Pasula
 * Date: [2025-07-07]
 */
// src/Dashboard.js
// ===============================
// ✅ IMPORTS & GLOBAL SETUP
// ===============================
import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from './Navbar';
import Toast from './Toast';
import './App.css';

const backendURL = process.env.REACT_APP_BACKEND_URL;

function Dashboard() {
  // ===============================
  // ✅ STATE VARIABLES
  // ===============================
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'system');
  const [allSummaries, setAllSummaries] = useState([]);
  const [summaries, setSummaries] = useState([]);
  const [toast, setToast] = useState(null);
  const [smartSummary, setSmartSummary] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('All');
  const [assigneeFilter, setAssigneeFilter] = useState('All');
  const [assigneeOptions, setAssigneeOptions] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [expandedEditCard, setExpandedEditCard] = useState(null);
  const [expandedRawCard, setExpandedRawCard] = useState(null);
  const [editingText, setEditingText] = useState('');
  const [loading, setLoading] = useState(true);
  const rowsPerPage = 5;
  const inputRef = useRef(null);

  //===============================
  // ✅ THEME MANAGEMENT
  // ===============================
  useEffect(() => {
    const root = document.body;
    root.classList.remove('light-mode', 'dark-mode');
    if (theme === 'dark') root.classList.add('dark-mode');
    else if (theme === 'light') root.classList.add('light-mode');
    else {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      root.classList.toggle('dark-mode', prefersDark);
      root.classList.toggle('light-mode', !prefersDark);
    }
    localStorage.setItem('theme', theme);
  }, [theme]);

  // ===============================
  // ✅ FETCH SUMMARIES ON LOAD
  // ===============================


  useEffect(() => {
    const token = localStorage.getItem('jwt_token');
    const storedUser = localStorage.getItem('user');
    if (!token) return navigate('/login');
    setUsername(storedUser);

    fetch(`${backendURL}/api/summary`, {
      headers: { Authorization: 'Bearer ' + token }
    })
      .then(async (res) => {
        if (res.status === 401) throw new Error('Unauthorized');
        const data = await res.json();
        setAllSummaries(data);
        setSummaries(data);

        const assigneeNames = Array.from(new Set(data.map(item => item.assignee).filter(Boolean)));
        setAssigneeOptions(['All', ...assigneeNames]);

        const counts = data.reduce((acc, cur) => {
          const s = cur.status || 'unknown';
          acc[s] = (acc[s] || 0) + 1;
          return acc;
        }, {});
        setSmartSummary(
          `📊 Total: ${data.length} issues — ✅ Done: ${counts['Done'] || 0}, 🔄 In Progress: ${counts['In Progress'] || 0}, 📝 To Do: ${counts['To Do'] || 0}`
        );
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setToast({ type: 'error', message: '🔒 Session expired. Redirecting...' });
        setTimeout(() => {
          localStorage.clear();
          navigate('/login');
        }, 2000);
      });
  }, [navigate]);

  useEffect(() => {
    if (expandedEditCard && inputRef.current) inputRef.current.focus();
  }, [expandedEditCard]);

  useEffect(() => {
    let filtered = allSummaries;
    if (statusFilter !== 'All') filtered = filtered.filter(i => i.status === statusFilter);
    if (assigneeFilter !== 'All') filtered = filtered.filter(i => i.assignee === assigneeFilter);
    if (searchTerm.trim() !== '') {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(i =>
        i.summary_generated?.toLowerCase().includes(term) ||
        i.assignee?.toLowerCase().includes(term)
      );
    }
    setSummaries(filtered);
    setCurrentPage(1);
  }, [statusFilter, assigneeFilter, searchTerm, allSummaries]);

  const totalPages = Math.ceil(summaries.length / rowsPerPage);
  const currentSummaries = summaries.slice(
    (currentPage - 1) * rowsPerPage,
    currentPage * rowsPerPage
  );
  // ===============================
  // ✅ HANDLERS: Copy, Edit, Delete, Download
  // ===============================
  const handleDownload = async (type) => {
    try {
      const win = window.open(`${backendURL}/download/${type}`, '_blank');
      if (win) {
        setToast({ type: 'success', message: `📥 ${type.toUpperCase()} download logged!` });
      } else {
        throw new Error("Popup blocked");
      }
    } catch (err) {
      console.error(err);
      setToast({ type: 'error', message: '⚠️ Download failed or blocked' });
    }
  };

  const handleLogout = () => { localStorage.clear(); navigate('/login'); };
  const copyText = (text) => { navigator.clipboard.writeText(text); setToast({ type: 'success', message: '📋 Copied to clipboard!' }); };
  const searchText = (text) => window.open(`https://google.com/search?q=${encodeURIComponent(text)}`, '_blank');
  const toggleRawView = (key) => setExpandedRawCard(prev => prev === key ? null : key);

  const deleteIssue = (key) => {
    if (!window.confirm(`Delete ${key}?`)) return;
    const updated = summaries.filter(s => s.key !== key);
    setSummaries(updated);
    setAllSummaries(allSummaries.filter(s => s.key !== key));
    fetch(`${backendURL}/api/update-summary`, {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('jwt_token'),
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(updated)
    });
    setToast({ type: 'success', message: `🗑️ ${key} deleted` });
  };

  const handleSaveEdit = (key) => {
    const updated = allSummaries.map(s => s.key === key ? { ...s, summary_generated: editingText } : s);
    setAllSummaries(updated);
    setSummaries(updated);
    setExpandedEditCard(null);
    fetch(`${backendURL}/api/update-summary`, {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('jwt_token'),
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(updated)
    });
    setToast({ type: 'success', message: `💾 Summary updated` });
  };

  const toggleExpand = (key, original) => {
    if (expandedEditCard === key) {
      setExpandedEditCard(null);
      setEditingText('');
    } else {
      setExpandedEditCard(key);
      setEditingText(original);
      setExpandedRawCard(null);
    }
  };

  const highlightMatch = (text) => {
    if (!searchTerm.trim()) return text;
    const regex = new RegExp(`(${searchTerm})`, 'gi');
    return text.split(regex).map((chunk, i) =>
      regex.test(chunk) ? <mark key={i}>{chunk}</mark> : chunk
    );
  };

  const statusCounts = allSummaries.reduce((a, i) => {
    a[i.status] = (a[i.status] || 0) + 1;
    return a;
  }, {});

  return (
    <div className="dashboard-container">
      {toast && <Toast type={toast.type} message={toast.message} onClose={() => setToast(null)} />}
      <Navbar username={username} onLogout={handleLogout} theme={theme} setTheme={setTheme} />

      <div className="top-bar">
        <div className="smart-summary">{smartSummary}</div>
        <div className="download-buttons">
          {['pdf', 'csv', 'json', 'all'].map((t, i) => (
            <button key={i} className="download-btn" onClick={() => handleDownload(t)}>📥 {t.toUpperCase()}</button>
          ))}
        </div>
      </div>

      <div style={{ marginBottom: '25px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
        <input
          type="text"
          placeholder="🔍 Search by assignee or summary"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{ padding: '10px', borderRadius: '6px', border: '1px solid #ccc', width: '100%', maxWidth: '320px' }}
        />
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          style={{ padding: '10px', borderRadius: '6px', border: '1px solid #ccc', minWidth: '150px' }}
        >
          <option value="All">All Statuses</option>
          <option value="To Do">To Do</option>
          <option value="In Progress">In Progress</option>
          <option value="Done">Done</option>
        </select>
        <select
          value={assigneeFilter}
          onChange={(e) => setAssigneeFilter(e.target.value)}
          style={{ padding: '10px', borderRadius: '6px', border: '1px solid #ccc', minWidth: '150px' }}
        >
          {assigneeOptions.map(name => (
            <option key={name} value={name}>{name}</option>
          ))}
        </select>
      </div>

      <div className="status-cards">
        {['To Do', 'In Progress', 'Done'].map(status => (
          <div key={status} className="status-card">
            <div className="status-title">{status}</div>
            <div className="status-count">{statusCounts[status] || 0}</div>
          </div>
        ))}
      </div>

      {loading ? (
        <p style={{ textAlign: 'center', padding: '50px 0', fontSize: '16px', color: '#888' }}>⏳ Loading summaries...</p>
      ) : (
        <div className="summary-grid">
          {currentSummaries.map((s, idx) => (
            <div key={idx} className="summary-card fancy-card">
              <div className="summary-header">
                <strong>{s.key}</strong>
                <span className={`status-badge ${s.status?.toLowerCase().replace(/\s/g, '-')}`}>{s.status}</span>
              </div>
              <div className="summary-text">
                {expandedEditCard === s.key ? (
                  <textarea
                    ref={inputRef}
                    rows={3}
                    value={editingText}
                    onChange={(e) => setEditingText(e.target.value)}
                    style={{ width: '100%', padding: '8px', borderRadius: '6px', border: '1px solid #ccc', fontSize: '14px', marginBottom: '10px' }}
                  ></textarea>
                ) : (
                  highlightMatch(s.summary_generated)
                )}
              </div>
              <div className="summary-footer">
                <span className="user-badge">👤 {s.assignee || '—'}</span>
                <div className="action-buttons">
                  {expandedEditCard === s.key ? (
                    <>
                      <button
                        onClick={() => handleSaveEdit(s.key)}
                        disabled={editingText === s.summary_generated.trim()}
                        title="Save"
                      >💾</button>
                      <button onClick={() => setExpandedEditCard(null)} title="Cancel">❌</button>
                    </>
                  ) : (
                    <>
                      <button onClick={() => copyText(s.summary_generated)} title="Copy">📋</button>
                      <button onClick={() => searchText(s.summary_generated)} title="Search">🔎</button>
                      <button onClick={() => toggleExpand(s.key, s.summary_generated)} title="Edit">✏️</button>
                      <button onClick={() => toggleRawView(s.key)} title="View Raw">📝</button>
                      <button onClick={() => deleteIssue(s.key)} title="Delete">🗑️</button>
                    </>
                  )}
                </div>
              </div>
              <div className={`raw-info-wrapper ${expandedRawCard === s.key ? 'open' : ''}`}>
                <div className="raw-info">
                  <p><strong>📝 Clean Summary:</strong> {s.summary_clean || 'N/A'}</p>
                  <p><strong>📄 Clean Description:</strong> {s.description_clean || 'N/A'}</p>
                </div>
              </div>
            </div>
          ))}
          {summaries.length === 0 && (
            <p style={{ textAlign: 'center', color: '#999', fontStyle: 'italic' }}>
              🤔 No matching summaries found.
            </p>
          )}
        </div>
      )}

      {summaries.length > rowsPerPage && (
        <div style={{ textAlign: 'center', marginTop: '20px' }}>
          <button
            onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
            disabled={currentPage === 1}
            className="pagination-btn"
          >⬅ Prev</button>
          <span style={{ margin: '0 15px' }}>Page <strong>{currentPage}</strong> of <strong>{totalPages}</strong></span>
          <button
            onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
            disabled={currentPage === totalPages}
            className="pagination-btn"
          >Next ➡</button>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
