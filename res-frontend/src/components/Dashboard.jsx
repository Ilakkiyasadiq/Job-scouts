import { useState, useEffect } from 'react';
import { 
  Paper, 
  Typography, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow,
  Button,
  Chip 
} from '@mui/material';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const [analyses, setAnalyses] = useState([]);

  useEffect(() => {
    const fetchAnalyses = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/analyses/');
        const data = await response.json();
        setAnalyses(data);
      } catch (error) {
        console.error('Error fetching analyses:', error);
      }
    };

    fetchAnalyses();
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'processing':
        return 'info';
      case 'failed':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <>
      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Typography variant="h5" gutterBottom>
          Recent Resume Analyses
        </Typography>
        <Button
          variant="contained"
          component={Link}
          to="/upload"
          sx={{ mb: 3 }}
        >
          New Analysis
        </Button>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Date</TableCell>
                <TableCell>Candidate Email</TableCell>
                <TableCell>Recruiter Email</TableCell>
                <TableCell>Match Score</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {analyses.map((analysis) => (
                <TableRow key={analysis.id}>
                  <TableCell>{new Date(analysis.created_at).toLocaleDateString()}</TableCell>
                  <TableCell>{analysis.candidate_email}</TableCell>
                  <TableCell>{analysis.recruiter_email}</TableCell>
                  <TableCell>
                    {analysis.match_score ? `${Math.round(analysis.match_score)}%` : 'N/A'}
                  </TableCell>
                  <TableCell>
                    <Chip 
                      label={analysis.status}
                      color={getStatusColor(analysis.status)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Button
                      variant="outlined"
                      size="small"
                      component={Link}
                      to={`/results/${analysis.id}`}
                    >
                      View Details
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </>
  );
};

export default Dashboard;