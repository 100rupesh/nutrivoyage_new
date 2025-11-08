from django.shortcuts import render,redirect,get_object_or_404
from .models import ClientDetails
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.contrib import messages
from django.http import JsonResponse
from .models import DailyHealthRecord
from .utils import calculate_client_summary
import json

# Create your views here.
from utils.decorators import role_required

# @login_required(login_url='login')
@role_required('NORMAL')
def client(request):
    return render(request,'clients/client.html')


@role_required('NORMAL')
def client_activity(request):
    return render(request,'clients/client_activity.html')

@role_required('NORMAL')
def client_plan(request):
    return render(request,'clients/client_plan.html')


@role_required('NORMAL')
def client_progress(request):
    return render(request,'clients/client_progress.html')

@role_required('NORMAL')
def client_appointment(request):
    return render(request,'clients/client_appointment.html')


@role_required('NORMAL')
def client_message(request):
    return render(request,'clients/client_message.html')

@role_required('NORMAL')
def client_meal(request):
    return render(request,'clients/client_mealtracking.html')

# @role_required('NORMAL')
# def client(request):
#     return render(request,'clients/client_form.html')


@role_required('DIETICIAN')
def create_client(request):
    if request.method == 'POST':
        # Fetch the logged-in user
        user = request.user
        f=request.POST.get('first_name')
        g=request.POST.get('gender')
        print("First Name:\t",f)
        print("Gender Name:\t",g)
        username=request.POST.get('username')
        password=str(123456)
        if User.objects.filter(username=username).exists():
            messages.error(request, 'User already exists')
            return redirect('create_client')  # Redirect back to the form page


        user_name = User.objects.create_user(username=username, password=password)


        # Create a new ClientDetails object
        client = ClientDetails.objects.create(
            user=user_name,
            created_by=user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            dob=request.POST.get('date_of_birth') or None,
            contact_no=request.POST.get('contact_no'),
            email_id=request.POST.get('email_id'),
            location=request.POST.get('location'),
            height=request.POST.get('height') or None,
            weight=request.POST.get('weight') or None,
            gender=request.POST.get('gender'),
            client_type=request.POST.get('client_type') or '',
            medical_condition=request.POST.get('medical_condition'),
            notes=request.POST.get('notes'),
            diet_preference=request.POST.get('diet_type'),
            medications=request.POST.get('medications'),
            chief_complaints=request.POST.get('chief_complaints'),
        )
        return redirect('client_list')  # Redirect to a success page or dashboard

    return render(request, 'clients/client_form.html')

@role_required('DIETICIAN')
def client_list(request):
    data=ClientDetails.objects.filter(created_by=request.user)#.order_by('-date_of_creation')
    print("-----",data)
    return render(request,'clients/client_list.html',context={'users':data})

@role_required('DIETICIAN')
def client_detail_view(request, client_id):
    # Retrieve the user object or return 404 if not found
    client = get_object_or_404(ClientDetails, id=client_id)
    context = {
        'user': client,
    }
    return render(request, 'clients/client_detail.html', context)



def update_client(request, client_id):
    client = get_object_or_404(ClientDetails, id=client_id)

    if request.method == 'POST':
        client.first_name = request.POST.get('first_name', '')
        client.last_name = request.POST.get('last_name', '')
        client.dob = request.POST.get('date_of_birth') or None
        client.contact_no = request.POST.get('contact_no', '')
        client.email_id = request.POST.get('email_id', '')
        client.location = request.POST.get('location', '')
        client.height = request.POST.get('height') or None
        client.weight = request.POST.get('weight') or None
        client.gender = request.POST.get('gender', '')
        client.client_type = request.POST.get('client_type') or ''
        client.medical_condition = request.POST.get('medical_condition', '')
        client.notes = request.POST.get('notes', '')
        client.medications = request.POST.get('medications', '')
        client.chief_complaints = request.POST.get('chief_complaints', '')

        client.save()
        return redirect('client_detail', client_id=client.id)  # Replace with your success view name

    return render(request, 'clients/client_edit.html', {'client': client})


@login_required
def health_graph(request):
    """Renders a page with dropdowns for username & parameter."""
    users = User.objects.all()
    parameters = [
        ('weight', 'Weight'),
        ('sleep_hours', 'Sleep Hours'),
        ('food_calories', 'Food Calories'),
        ('workout_calories', 'Workout Calories'),
        ('workout_duration', 'Workout Duration'),
    ]
    return render(request, 'clients/health_graph.html', {'users': users, 'parameters': parameters})


@login_required
def get_graph_data(request):
    """Returns JSON data for the selected user and parameter."""
    username = request.GET.get('username')
    parameter = request.GET.get('parameter')

    if not username or not parameter:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    records = DailyHealthRecord.objects.filter(user=user).order_by('date')
    data = {
        'labels': [r.date.strftime('%Y-%m-%d') for r in records],
        'values': [getattr(r, parameter) or 0 for r in records],
    }
    print("----->",data)
    return JsonResponse(data)

def client_view_graph(request, user_id):
    user = get_object_or_404(User, id=user_id)
    records = DailyHealthRecord.objects.filter(user=user).order_by('date')

    parameters = [
        ('workout_calories', 'Workout Calories'),
        ('sleep_hours', 'Sleep Hours'),
        ('weight', 'Weight'),
        ('food_calories', 'Food Calories'),
    ]

    # Pre-serialize data for JS (as a dict of lists)
    data_dict = {
        "dates": [str(r.date) for r in records],
        "workout_calories": [float(r.workout_calories or 0) for r in records],
        "sleep_hours": [float(r.sleep_hours or 0) for r in records],
        "weight": [float(r.weight or 0) for r in records],
        "food_calories": [float(r.food_calories or 0) for r in records],
    }

    context = {
        "user": user,
        "parameters": parameters,
        "data_json": json.dumps(data_dict),
    }

    return render(request, 'clients/client_view_graph.html', context)


def dietician_dashboard(request):
    clients = User.objects.filter(is_staff=False)
    summaries = [calculate_client_summary(u) for u in clients if calculate_client_summary(u)]

    return render(request, 'clients/dietician_dashboard.html', {
        'summaries': summaries
    })


import io
from datetime import timedelta
from django.http import FileResponse
from django.utils.timezone import now
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.graphics.shapes import Drawing, String, Rect
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from .models import DailyHealthRecord


def weekly_report(request, user_id):
    user = User.objects.get(id=user_id)
    today = now().date()
    week_ago = today - timedelta(days=7)
    records = DailyHealthRecord.objects.filter(
        user=user, date__range=[week_ago, today]
    ).order_by("date")

    buffer = io.BytesIO()
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), leftMargin=40, rightMargin=40, topMargin=40)
    elements = []

    if not records.exists():
        elements.append(Paragraph("No data available for this week.", styles["Normal"]))
        doc.build(elements)
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename="no_data.pdf")

    # Extract and normalize data
    def safe_float(v): return float(v or 0)
    dates = [r.date.strftime("%d %b") for r in records]
    workout = [safe_float(r.workout_calories) for r in records]
    sleep = [safe_float(r.sleep_hours) for r in records]
    weight = [safe_float(r.weight) for r in records]
    calories = [safe_float(r.food_calories) for r in records]

    # === HEADER ===
    title_style = ParagraphStyle('title', parent=styles['Title'], textColor=colors.HexColor("#1B4F72"))
    elements.append(Paragraph("🏋️‍♀️ Weekly Health Report Dashboard", title_style))
    elements.append(Paragraph(f"Client: <b>{user.username}</b>", styles['Normal']))
    elements.append(Paragraph(f"Period: {week_ago.strftime('%d %b')} – {today.strftime('%d %b %Y')}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # === CHART CREATOR ===
    def make_chart(values, title, color):
        d = Drawing(250, 150)
        bg = Rect(0, 0, 250, 150, fillColor=colors.whitesmoke)
        d.add(bg)

        lc = HorizontalLineChart()
        lc.x = 30
        lc.y = 25
        lc.height = 100
        lc.width = 200
        lc.data = [values]
        lc.joinedLines = True
        lc.lines[0].strokeColor = color
        lc.lines[0].strokeWidth = 2

        lc.categoryAxis.categoryNames = dates
        lc.categoryAxis.labels.boxAnchor = 'ne'
        lc.categoryAxis.labels.angle = 45
        lc.categoryAxis.labels.fontSize = 7
        lc.categoryAxis.strokeColor = colors.black

        lc.valueAxis.valueMin = 0
        lc.valueAxis.valueMax = max(values) * 1.2 if max(values) > 0 else 10
        lc.valueAxis.visibleGrid = True
        lc.valueAxis.gridStrokeColor = colors.lightgrey
        lc.valueAxis.labels.fontSize = 7
        lc.valueAxis.strokeColor = colors.black

        d.add(lc)
        d.add(String(70, 135, title, fontSize=10, fillColor=color))
        return d

    # === CREATE 4 CHARTS ===
    charts = [
        make_chart(workout, "💪 Workout Minutes", colors.HexColor("#1ABC9C")),
        make_chart(sleep, "😴 Sleep Hours", colors.HexColor("#9B59B6")),
        make_chart(weight, "⚖️ Weight (kg)", colors.HexColor("#E67E22")),
        make_chart(calories, "🍽️ Calories", colors.HexColor("#2E86C1")),
    ]

    # === LAYOUT IN 2×2 GRID ===
    grid = Drawing(520, 330)

    # translate each chart to its grid position
    charts[0].translate(0, 170)     # top-left
    charts[1].translate(260, 170)   # top-right
    charts[2].translate(0, 0)       # bottom-left
    charts[3].translate(260, 0)     # bottom-right

    # add them to the main drawing
    grid.add(charts[0])
    grid.add(charts[1])
    grid.add(charts[2])
    grid.add(charts[3])


    # === SUMMARY TABLE ===
    avg_calories = sum(calories) / len(calories)
    avg_sleep = sum(sleep) / len(sleep)
    avg_workout = sum(workout) / len(workout)
    weight_change = weight[-1] - weight[0]

    data = [
        ["Metric", "Avg / Change", "Remarks"],
        ["Workout (min)", f"{avg_workout:.1f}", "Good" if avg_workout > 30 else "Needs effort"],
        ["Sleep (hrs)", f"{avg_sleep:.1f}", "Sufficient" if avg_sleep >= 7 else "Low"],
        ["Calories (kcal)", f"{avg_calories:.1f}", "Normal" if avg_calories < 2200 else "High"],
        ["Weight Δ (kg)", f"{weight_change:+.1f}", "Stable" if abs(weight_change) < 1 else "Change"],
    ]
    table = Table(data, colWidths=[2.5*inch, 1.5*inch, 2.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2E86C1")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
    ]))
    elements.append(Paragraph("📋 Weekly Summary", styles['Heading3']))
    elements.append(table)
    elements.append(Spacer(1, 15))

    # === AI INSIGHT TEXT ===
    summary = (
        f"<b>AI Insights:</b> {user.username} averaged {avg_workout:.0f} mins workout/day, "
        f"{avg_sleep:.1f} hrs sleep, {avg_calories:.0f} kcal intake, "
        f"and weight change {weight_change:+.1f} kg. "
        f"{'Great consistency!' if avg_workout > 30 else 'Try increasing activity slightly for improved progress.'}"
    )
    elements.append(Paragraph(summary, styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"{user.username}_weekly_report.pdf")
