import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Paper,
  Typography,
  Box,
  Grid,
  CircularProgress,
  Chip,
  List,
  ListItem,
  ListItemText,
  Rating,
  Alert,
} from '@mui/material';

const Results = () => {
  const { id } = useParams();
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/analyses/${id}/`);
        if (!response.ok) {
          throw new Error('Failed to fetch results');
        }
        const data = await response.json();
        setAnalysis(data);
      } catch (err) {
        setError('Failed to load analysis results');
      } finally {
        setLoading(false);
      }
    };

    const pollResults = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/analyses/${id}/status/`);
        if (!response.ok) {
          throw new Error('Failed to fetch status');
        }
        const data = await response.json();
        
        if (data.status === 'completed') {
          fetchResults();
        } else if (data.status === 'failed') {
          setError('Analysis failed');
          setLoading(false);
        } else {
          setTimeout(pollResults, 2000);
        }
      } catch (err) {
        setError('Failed to check analysis status');
        setLoading(false);
      }
    };

    pollResults();
  }, [id]);

  if (loading) {
    return (
      <Box display="flex" flexDirection="column" alignItems="center" mt={4}>
        <CircularProgress size={60} />
        <Typography variant="h6" sx={{ mt: 2 }}>
          Analyzing Resume...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mt: 4 }}>
        {error}
      </Alert>
    );
  }

  if (!analysis) {
    return (
      <Alert severity="info" sx={{ mt: 4 }}>
        No analysis results found
      </Alert>
    );
  }

  return (
    <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
      <Typography variant="h5" gutterBottom>
        Resume Analysis Results
      </Typography>

      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <Box mb={4}>
            <Typography variant="h6" gutterBottom>
              Overall Match Score
            </Typography>
            <Box display="flex" alignItems="center">
              <Box position="relative" display="inline-flex">
                <CircularProgress
                  variant="determinate"
                  value={analysis.match_score}
                  size={100}
                  thickness={4}
                  sx={{ color: analysis.match_score >= 70 ? 'success.main' : 'warning.main' }}
                />
                <Box
                  position="absolute"
                  top={0}
                  left={0}
                  bottom={0}
                  right={0}
                  display="flex"
                  alignItems="center"
                  justifyContent="center"
                >
                  <Typography variant="h4" component="div">
                    {Math.round(analysis.match_score)}%
                  </Typography>
                </Box>
              </Box>
            </Box>
          </Box>

          <Box mb={4}>
            <Typography variant="h6" gutterBottom>
              Matching Skills
            </Typography>
            <Box>
              {analysis.matching_skills?.map((skill) => (
                <Chip
                  key={skill}
                  label={skill}
                  color="success"
                  sx={{ m: 0.5 }}
                />
              ))}
            </Box>
          </Box>

          <Box mb={4}>
            <Typography variant="h6" gutterBottom>
              Skills to Develop
            </Typography>
            <Box>
              {analysis.missing_skills?.map((skill) => (
                <Chip
                  key={skill}
                  label={skill}
                  color="warning"
                  variant="outlined"
                  sx={{ m: 0.5 }}
                />
              ))}
            </Box>
          </Box>
        </Grid>

        <Grid item xs={12} md={6}>
          <Box mb={4}>
            <Typography variant="h6" gutterBottom>
              Experience & Education
            </Typography>
            <List>
              <ListItem>
                <ListItemText
                  primary="Experience Match"
                  secondary={
                    <Rating
                      value={analysis.experience_match / 20}
                      readOnly
                      precision={0.5}
                    />
                  }
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Education Match"
                  secondary={
                    <Rating
                      value={analysis.education_match / 20}
                      readOnly
                      precision={0.5}
                    />
                  }
                />
              </ListItem>
            </List>
          </Box>

          <Box>
            <Typography variant="h6" gutterBottom>
              Recommendations
            </Typography>
            <List>
              {analysis.recommendations?.map((recommendation, index) => (
                <ListItem key={index}>
                  <ListItemText
                    primary={recommendation}
                    sx={{
                      '& .MuiListItemText-primary': {
                        color: 'text.secondary',
                      },
                    }}
                  />
                </ListItem>
              ))}
            </List>
          </Box>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default Results;