from rest_framework import serializers
from .models import ResumeAnalysis

class ResumeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeAnalysis
        fields = '__all__'
        read_only_fields = ('status', 'match_score', 'matching_skills', 'missing_skills', 
                          'experience_match', 'education_match', 'recommendations')