from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import ResumeAnalysis
from .serializers import ResumeAnalysisSerializer
from .ml_utils import extract_text_from_file, analyze_resume
import os

class ResumeAnalysisViewSet(viewsets.ModelViewSet):
    queryset = ResumeAnalysis.objects.all()
    serializer_class = ResumeAnalysisSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(status='processing')

        try:
            resume_path = instance.resume.path
            resume_text = extract_text_from_file(resume_path)
            analysis_results = analyze_resume(resume_text, instance.job_description)
            
            instance.status = 'completed'
            instance.match_score = analysis_results['match_score']
            instance.matching_skills = analysis_results['matching_skills']
            instance.missing_skills = analysis_results['missing_skills']
            instance.experience_match = analysis_results['experience_match']
            instance.education_match = analysis_results['education_match']
            instance.recommendations = analysis_results['recommendations']
            instance.save()

            self._send_analysis_emails(instance)
            return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            instance.status = 'failed'
            instance.save()
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _send_analysis_emails(self, analysis):
        """Send HTML formatted analysis results to both candidate and recruiter"""
        
        def create_html_content(is_recruiter=False):
            context = {
                'is_recruiter': is_recruiter,
                'candidate_email': analysis.candidate_email,
                'match_score': round(analysis.match_score, 1),
                'matching_skills': analysis.matching_skills,
                'missing_skills': analysis.missing_skills,
                'experience_match': round(analysis.experience_match, 1),
                'education_match': round(analysis.education_match, 1),
                'recommendations': analysis.recommendations,
                'score_color': '#28a745' if analysis.match_score >= 70 else '#ffc107'
            }
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Resume Analysis Results</title>
            </head>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
                        <h2 style="margin-top: 0;">{'Resume Analysis Results' if not is_recruiter else f'Resume Analysis Results - {context["candidate_email"]}'}</h2>
                        {'<p>Dear Candidate,</p>' if not is_recruiter else f'<p>Dear Recruiter,</p>'}
                    </div>

                    <div style="margin-bottom: 20px; text-align: center;">
                        <h3>Overall Match Score</h3>
                        <table cellpadding="0" cellspacing="0" border="0" style="margin: 0 auto;">
                            <tr>
                                <td>
                                    <div style="background-color: {context['score_color']}; width: 120px; height: 120px; border-radius: 60px; margin: 20px auto; position: relative;">
                                        <table cellpadding="0" cellspacing="0" border="0" width="100%" height="100%">
                                            <tr>
                                                <td align="center" valign="middle" style="color: white; font-size: 32px; font-weight: bold;">
                                                    {context['match_score']}%
                                                </td>
                                            </tr>
                                        </table>
                                    </div>
                                </td>
                            </tr>
                        </table>
                    </div>

                    <div style="margin-bottom: 20px;">
                        <h3>Matching Skills</h3>
                        {'<p>No matching skills found</p>' if not context['matching_skills'] else ''}
                        <div>
                            {''.join(f'<span style="display: inline-block; background-color: #e9ecef; padding: 5px 10px; border-radius: 15px; margin: 2px;">{skill}</span>' for skill in context['matching_skills'])}
                        </div>
                    </div>

                    <div style="margin-bottom: 20px;">
                        <h3>Skills to Develop</h3>
                        {'<p>No skill gaps identified</p>' if not context['missing_skills'] else ''}
                        <div>
                            {''.join(f'<span style="display: inline-block; background-color: #fff3cd; padding: 5px 10px; border-radius: 15px; margin: 2px;">{skill}</span>' for skill in context['missing_skills'])}
                        </div>
                    </div>

                    <div style="margin-bottom: 20px;">
                        <h3>Experience & Education Match</h3>
                        <p><strong>Experience Match:</strong> <span style="color: {context['score_color']}">{context['experience_match']}%</span></p>
                        <p><strong>Education Match:</strong> <span style="color: {context['score_color']}">{context['education_match']}%</span></p>
                    </div>

                    <div style="margin-bottom: 20px;">
                        <h3>Recommendations</h3>
                        {''.join(f'<div style="padding: 10px; background-color: #f8f9fa; border-left: 4px solid #007bff; margin-bottom: 10px;">{rec}</div>' for rec in context['recommendations'])}
                    </div>

                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                        <p>Best regards,<br>Resume Analyzer Team</p>
                    </div>
                </div>
            </body>
            </html>
            """
            return html_content

        try:
            # Create and send candidate email
            candidate_subject = 'Your Resume Analysis Results'
            candidate_html = create_html_content(is_recruiter=False)
            candidate_text = strip_tags(candidate_html)
            
            msg_candidate = EmailMultiAlternatives(
                candidate_subject,
                candidate_text,
                settings.DEFAULT_FROM_EMAIL,
                [analysis.candidate_email]
            )
            msg_candidate.attach_alternative(candidate_html, "text/html")
            
            # Create and send recruiter email
            recruiter_subject = f'Resume Analysis Results - {analysis.candidate_email}'
            recruiter_html = create_html_content(is_recruiter=True)
            recruiter_text = strip_tags(recruiter_html)
            
            msg_recruiter = EmailMultiAlternatives(
                recruiter_subject,
                recruiter_text,
                settings.DEFAULT_FROM_EMAIL,
                [analysis.recruiter_email]
            )
            msg_recruiter.attach_alternative(recruiter_html, "text/html")
            
            # Send both emails
            msg_candidate.send()
            msg_recruiter.send()
            
        except Exception as e:
            print(f"Failed to send emails: {str(e)}")

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """Get the current status of an analysis"""
        instance = self.get_object()
        return Response({
            'status': instance.status,
            'match_score': instance.match_score
        })
