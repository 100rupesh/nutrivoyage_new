# views.py
from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import F,ExpressionWrapper, DateTimeField
from .models import Appointment,DietPlan
from clients.models import ClientDetails
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from accounts.models import User
from utils.decorators import role_required
from django.utils import timezone
from datetime import timedelta

@require_http_methods(["GET", "POST"])
@role_required('DIETICIAN')
def create_appointment(request):
    clients = ClientDetails.objects.filter(created_by=request.user)

    if request.method == 'POST':
        client_id = request.POST.get('patient')
        print("ID ->",client_id)
        appointment_type = request.POST.get('appointment_type')
        notes = request.POST.get('notes')
        try:
            client = User.objects.get(id=client_id)
            Appointment.objects.create(
                patient=client,
                appointment_type=appointment_type,
                notes=notes,
                created_by=request.user,
               
            )
            messages.success(request, 'Appointment created successfully.')
            return redirect('homepage')  # Update this to your actual appointment list view
        except ClientDetails.DoesNotExist:
            messages.error(request, 'Invalid client selected.')

    return render(request, 'appointments/create_appointment.html', {'clients': clients})




@role_required('DIETICIAN')
def appointment_list(request):
    thirty_days_ago = timezone.now() - timedelta(days=30)
    print("30",thirty_days_ago)
    data=Appointment.objects.filter(created_by=request.user,datetime__gte=thirty_days_ago)
    print("Data",data)
    return render(request,'appointments/appointment_list.html',context={'appointments':data})



@role_required('DIETICIAN')
def appointment_detail_view(request, appointment_id):
    # Retrieve the user object or return 404 if not found
    appointment = get_object_or_404(Appointment, id=appointment_id)
    diet_1=DietPlan.objects.filter(appointment=appointment,diet_no=1).first()
    diet_2=DietPlan.objects.filter(appointment=appointment,diet_no=2).first()
    context = {
        'appointment': appointment,
        'diet_1':diet_1,
        'diet_2':diet_2,
    }
    return render(request, 'appointments/appointment_detail.html', context)


def create_diet_plan(request, appointment_id,diet_no):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    print("P  ID",appointment.patient.client_profile.first_name)

    # if appointment.diet_plans.count() >= 2:
    #     messages.error(request, "Maximum of 2 diet plans already exist for this appointment.")
    #     return redirect('appointment_detail', pk=appointment.id)

    if request.method == 'POST':
        breakfast = request.POST.get('breakfast', '').strip()
        lunch = request.POST.get('lunch', '').strip()
        snacks = request.POST.get('snacks', '').strip()
        dinner = request.POST.get('dinner', '').strip()

        errors = {}
        if not breakfast:
            errors['breakfast'] = "Breakfast is required."
        if not lunch:
            errors['lunch'] = "Lunch is required."
        if not snacks:
            errors['snacks'] = "Snacks are required."
        if not dinner:
            errors['dinner'] = "Dinner is required."

        if errors:
            return render(request, 'create_diet_plan.html', {
                'appointment': appointment,
                'errors': errors,
                'data': request.POST,
            })

        # Save new DietPlan
        DietPlan.objects.create(
            appointment=appointment,
            breakfast=breakfast,
            lunch=lunch,
            snacks=snacks,
            dinner=dinner,
            diet_no=diet_no
        )
        messages.success(request, "Diet plan created successfully.")
        return redirect('appointment_detail', appointment_id=appointment.id)

    return render(request, 'appointments/create_dietplan.html', {
        'appointment': appointment,
    })


from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch
from django.shortcuts import get_object_or_404
from .models import Appointment, DietPlan

@role_required('DIETICIAN')
def download_diet_pdf(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    diet_1 = DietPlan.objects.filter(appointment=appointment, diet_no=1).first()
    diet_2 = DietPlan.objects.filter(appointment=appointment, diet_no=2).first()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Diet_Plan_{appointment.patient}.pdf"'

    # Create PDF
    doc = SimpleDocTemplate(response, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=40)
    story = []

    # Register Unicode font for multilingual support
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CustomTitle', fontSize=18, leading=22, textColor=colors.HexColor("#1e7e34"), spaceAfter=12, alignment=1))
    styles.add(ParagraphStyle(name='CustomHeader', fontSize=14, leading=18, textColor=colors.HexColor("#145624"), spaceBefore=10, spaceAfter=6))
    styles.add(ParagraphStyle(name='CustomText', fontSize=11, leading=16, textColor=colors.black))

    # Title
    story.append(Paragraph("🍃 Diet Plan Summary", styles['CustomTitle']))
    story.append(Paragraph(f"<b>Patient:</b> {appointment.patient}", styles['CustomText']))
    story.append(Paragraph(f"<b>Date:</b> {appointment.datetime.strftime('%B %d, %Y')}", styles['CustomText']))
    story.append(Spacer(1, 12))

    def add_diet_plan(plan, number):
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"Diet Plan {number}", styles['CustomHeader']))

        if not plan:
            story.append(Paragraph("No diet plan created yet.", styles['CustomText']))
            return

        data = [
            ["Meal", "Details"],
            ["Breakfast", plan.breakfast or ""],
            ["Lunch", plan.lunch or ""],
            ["Snacks", plan.snacks or ""],
            ["Dinner", plan.dinner or ""],
        ]

        table = Table(data, colWidths=[1.5 * inch, 4.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e7e34")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'HeiseiKakuGo-W5'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ]))
        story.append(table)

        story.append(Spacer(1, 8))
        story.append(Paragraph(f"<i>Created on: {plan.created_at.strftime('%B %d, %Y %I:%M %p')}</i>", styles['CustomText']))

    add_diet_plan(diet_1, 1)
    add_diet_plan(diet_2, 2)

    doc.build(story)
    return response
