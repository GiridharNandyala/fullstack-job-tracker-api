import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = "https://fullstack-job-tracker-api.onrender.com";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isRegister, setIsRegister] = useState(false);
  const [jobs, setJobs] = useState([]);
  const [filterStatus, setFilterStatus] = useState("All");

  const [title, setTitle] = useState("");
  const [company, setCompany] = useState("");
  const [status, setStatus] = useState("Applied");

  useEffect(() => {
    if (token) fetchJobs();
  }, [token, filterStatus]);

  const fetchJobs = async () => {
    try {
      let url = `${API_URL}/jobs`;
      if (filterStatus !== "All") url += `?status=${filterStatus}`;
      const res = await axios.get(url, { headers: { Authorization: `Bearer ${token}` } });
      setJobs(res.data);
    } catch (err) {
      if (err.response?.status === 401) handleLogout();
    }
  };

  const handleAuth = async (e) => {
    e.preventDefault();
    try {
      if (isRegister) {
        await axios.post(`${API_URL}/register`, { email, password });
        alert("Account created successfully! Please login.");
        setIsRegister(false);
      } else {
        const formData = new URLSearchParams();
        formData.append("username", email);
        formData.append("password", password);
        const res = await axios.post(`${API_URL}/login`, formData, {
          headers: { "Content-Type": "application/x-www-form-urlencoded" }
        });
        setToken(res.data.access_token);
        localStorage.setItem("token", res.data.access_token);
      }
    } catch (err) {
      alert("Authentication failed. Check credentials.");
    }
  };

  const handleAddJob = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/jobs`, { title, company, status }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTitle(""); setCompany("");
      fetchJobs();
    } catch (err) {
      alert("Failed to add job.");
    }
  };

  const handleDeleteJob = async (jobId) => {
    if (window.confirm("Are you sure you want to delete this job application?")) {
      try {
        await axios.delete(`${API_URL}/jobs/${jobId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        fetchJobs();
      } catch (err) {
        alert("Failed to delete job.");
      }
    }
  };

  const handleLogout = () => {
    setToken("");
    localStorage.removeItem("token");
  };

  if (!token) {
    return (
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh", background: "#0f172a" }}>
        <div style={{ background: "#1e293b", padding: "40px", borderRadius: "12px", width: "400px", boxShadow: "0 10px 25px rgba(0,0,0,0.3)", border: "1px solid #334155" }}>
          <h2 style={{ color: "#fff", textAlign: "center", marginBottom: "24px" }}>{isRegister ? "Create Account" : "Welcome Back 👋"}</h2>
          <form onSubmit={handleAuth} style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
            <input type="email" placeholder="Email address" value={email} onChange={(e) => setEmail(e.target.value)} required style={{ padding: "12px", background: "#0f172a", border: "1px solid #334155", color: "#fff", borderRadius: "8px", outline: "none" }} />
            <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required style={{ padding: "12px", background: "#0f172a", border: "1px solid #334155", color: "#fff", borderRadius: "8px", outline: "none" }} />
            <button type="submit" style={{ padding: "12px", background: "#6366f1", color: "#fff", border: "none", borderRadius: "8px", fontWeight: "bold", cursor: "pointer" }}>{isRegister ? "Register" : "Login"}</button>
          </form>
          <p onClick={() => setIsRegister(!isRegister)} style={{ textAlign: "center", marginTop: "20px", color: "#94a3b8", cursor: "pointer", fontSize: "14px" }}>
            {isRegister ? "Already have an account? Login" : "Don't have an account? Register"}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: "1000px", margin: "40px auto", padding: "20px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "#1e293b", padding: "24px", borderRadius: "12px", border: "1px solid #334155" }}>
        <div>
          <h1 style={{ margin: "0 0 6px 0", color: "#fff", fontSize: "24px" }}>💼 Job Application Tracker</h1>
          <p style={{ margin: 0, color: "#94a3b8", fontSize: "14px" }}>Manage your career pipeline efficiently</p>
        </div>
        <button onClick={handleLogout} style={{ padding: "10px 20px", background: "#ef4444", color: "#fff", border: "none", borderRadius: "8px", cursor: "pointer", fontWeight: "bold" }}>Logout</button>
      </div>

      <div style={{ background: "#1e293b", padding: "24px", borderRadius: "12px", border: "1px solid #334155", margin: "24px 0" }}>
        <h3 style={{ color: "#818cf8", margin: "0 0 16px 0" }}>Add New Application</h3>
        <form onSubmit={handleAddJob} style={{ display: "grid", gridTemplateColumns: "1fr 1fr 150px 120px", gap: "12px" }}>
          <input type="text" placeholder="Job Title" value={title} onChange={(e) => setTitle(e.target.value)} required style={{ padding: "10px", background: "#0f172a", border: "1px solid #334155", color: "#fff", borderRadius: "6px" }} />
          <input type="text" placeholder="Company" value={company} onChange={(e) => setCompany(e.target.value)} required style={{ padding: "10px", background: "#0f172a", border: "1px solid #334155", color: "#fff", borderRadius: "6px" }} />
          <select value={status} onChange={(e) => setStatus(e.target.value)} style={{ padding: "10px", background: "#0f172a", border: "1px solid #334155", color: "#fff", borderRadius: "6px" }}>
            <option value="Applied">Applied</option>
            <option value="Interviewing">Interviewing</option>
            <option value="Offered">Offered</option>
            <option value="Rejected">Rejected</option>
          </select>
          <button type="submit" style={{ padding: "10px", background: "#10b981", color: "#fff", border: "none", borderRadius: "6px", fontWeight: "bold", cursor: "pointer" }}>Save Job</button>
        </form>
      </div>

      <div style={{ background: "#1e293b", padding: "24px", borderRadius: "12px", border: "1px solid #334155" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
          <h3 style={{ color: "#fff", margin: 0 }}>Your Applications Pipeline</h3>
          <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)} style={{ padding: "8px 12px", background: "#0f172a", border: "1px solid #334155", color: "#fff", borderRadius: "6px" }}>
            <option value="All">All Statuses</option>
            <option value="Applied">Applied</option>
            <option value="Interviewing">Interviewing</option>
            <option value="Offered">Offered</option>
            <option value="Rejected">Rejected</option>
          </select>
        </div>

        <table style={{ width: "100%", borderCollapse: "collapse", textAlign: "left" }}>
          <thead>
            <tr style={{ borderBottom: "1px solid #334155", color: "#94a3b8", fontSize: "14px" }}>
              <th style={{ padding: "12px" }}>ID</th>
              <th style={{ padding: "12px" }}>Title</th>
              <th style={{ padding: "12px" }}>Company</th>
              <th style={{ padding: "12px" }}>Status</th>
              <th style={{ padding: "12px", textAlign: "center" }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {jobs.length > 0 ? (
              jobs.map((job) => (
                <tr key={job.id} style={{ borderBottom: "1px solid #33415550" }}>
                  <td style={{ padding: "14px 12px", color: "#94a3b8" }}>#{job.id}</td>
                  <td style={{ padding: "14px 12px", fontWeight: "500", color: "#fff" }}>{job.title}</td>
                  <td style={{ padding: "14px 12px", color: "#cbd5e1" }}>{job.company}</td>
                  <td style={{ padding: "14px 12px" }}>
                    <span style={{
                      padding: "4px 10px", borderRadius: "20px", fontSize: "12px", fontWeight: "bold",
                      background: job.status === 'Offered' ? 'rgba(16, 185, 129, 0.15)' : job.status === 'Interviewing' ? 'rgba(245, 158, 11, 0.15)' : job.status === 'Rejected' ? 'rgba(239, 68, 68, 0.15)' : 'rgba(99, 102, 241, 0.15)',
                      color: job.status === 'Offered' ? '#34d399' : job.status === 'Interviewing' ? '#fbbf24' : job.status === 'Rejected' ? '#f87171' : '#818cf8'
                    }}>
                      {job.status}
                    </span>
                  </td>
                  <td style={{ padding: "14px 12px", textAlign: "center" }}>
                    <button 
                      onClick={() => handleDeleteJob(job.id)} 
                      style={{ padding: "6px 12px", background: "rgba(239, 68, 68, 0.2)", color: "#f87171", border: "1px solid rgba(239, 68, 68, 0.4)", borderRadius: "6px", cursor: "pointer", fontSize: "12px", fontWeight: "bold" }}>
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5" style={{ textAlign: "center", padding: "30px", color: "#64748b" }}>No jobs found</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;