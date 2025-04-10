from django.contrib import admin
from .models import ResumeAnalysis

@admin.register(ResumeAnalysis)
class ResumeAnalysisAdmin(admin.ModelAdmin):
    list_display = ('candidate_email', 'status', 'match_score', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('candidate_email',)
    readonly_fields = ('created_at', 'match_score', 'matching_skills', 'missing_skills',
                      'experience_match', 'education_match', 'recommendations')
