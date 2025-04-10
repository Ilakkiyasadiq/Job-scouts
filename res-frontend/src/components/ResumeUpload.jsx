import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Alert,
  CircularProgress
} from '@mui/material';
import { CloudUpload } from '@mui/icons-material';

const ResumeUpload = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [candidateEmail, setCandidateEmail] = useState('');
  const [recruiterEmail, setRecruiterEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && (selectedFile.type === 'application/pdf' || 
        selectedFile.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')) {
      setFile(selectedFile);
      setError('');
    } else {
      setError('Please upload a PDF or DOCX file');
      setFile(null);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file || !jobDescription || !candidateEmail || !recruiterEmail) {
      setError('Please fill in all fields');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_description', jobDescription);
    formData.append('candidate_email', candidateEmail);
    formData.append('recruiter_email', recruiterEmail);

    try {
      const response = await fetch('http://localhost:8000/api/analyses/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const data = await response.json();
      navigate(`/results/${data.id}`);
    } catch (err) {
      setError('Failed to upload resume. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
      <Typography variant="h5" gutterBottom>
        Upload Resume for Analysis
      </Typography>

      <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
        <Box sx={{ mb: 3 }}>
          <input
            accept=".pdf,.docx"
            style={{ display: 'none' }}
            id="resume-file"
            type="file"
            onChange={handleFileChange}
          />
          <label htmlFor="resume-file">
            <Button
              variant="outlined"
              component="span"
              startIcon={<CloudUpload />}
              sx={{ mb: 1 }}
            >
              Choose Resume
            </Button>
          </label>
          {file && (
            <Typography variant="body2" sx={{ ml: 1 }}>
              Selected file: {file.name}
            </Typography>
          )}
        </Box>

        <TextField
          fullWidth
          label="Job Description"
          multiline
          rows={4}
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          sx={{ mb: 3 }}
        />

        <TextField
          fullWidth
          label="Candidate Email"
          type="email"
          value={candidateEmail}
          onChange={(e) => setCandidateEmail(e.target.value)}
          sx={{ mb: 3 }}
        />

        <TextField
          fullWidth
          label="Recruiter Email"
          type="email"
          value={recruiterEmail}
          onChange={(e) => setRecruiterEmail(e.target.value)}
          sx={{ mb: 3 }}
        />

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        <Button
          type="submit"
          variant="contained"
          disabled={loading}
          sx={{ minWidth: 200 }}
        >
          {loading ? (
            <CircularProgress size={24} color="inherit" />
          ) : (
            'Analyze Resume'
          )}
        </Button>
      </Box>
    </Paper>
  );
};

export default ResumeUpload;