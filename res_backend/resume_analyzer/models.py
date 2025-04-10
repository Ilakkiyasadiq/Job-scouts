from django.db import models

class ResumeAnalysis(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    resume = models.FileField(upload_to='resumes/')
    job_description = models.TextField()
    candidate_email = models.EmailField()
    recruiter_email = models.EmailField(default="default@gmail.com")  # New field for recruiter's email
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Analysis Results
    match_score = models.FloatField(null=True, blank=True)
    matching_skills = models.JSONField(default=list, blank=True)
    missing_skills = models.JSONField(default=list, blank=True)
    experience_match = models.FloatField(null=True, blank=True)
    education_match = models.FloatField(null=True, blank=True)
    recommendations = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Resume Analysis for {self.candidate_email} ({self.status})"

    class Meta:
        verbose_name_plural = "Resume Analyses"
        ordering = ['-created_at']
