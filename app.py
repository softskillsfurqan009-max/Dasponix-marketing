from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from flask_cors import CORS
from functools import wraps
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'nova-secret-key-2025')
CORS(app)

# ============================================
# EMAIL CONFIGURATION - UPDATE THESE VALUES
# ============================================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# !!! IMPORTANT: Replace with your actual email and app password !!!
SENDER_EMAIL = "novamarketing79@gmail.com"
SENDER_PASSWORD = "YOUR_16_DIGIT_APP_PASSWORD_HERE"  # Get from Google App Passwords
RECEIVER_EMAIL = "novamarketing79@gmail.com"

def send_email_notification(name, email, company, message):
    """Send email notification"""
    try:
        subject = f"🔔 New Contact Form Message from {name}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"></head>
        <body style="font-family: Arial, sans-serif; background: #0A0A0A; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: #111; border: 2px solid #D4AF37; border-radius: 20px; padding: 20px;">
                <div style="text-align: center; border-bottom: 2px solid #D4AF37; padding-bottom: 15px;">
                    <h1 style="color: #D4AF37;">✨ NOVA MARKETING ✨</h1>
                    <p style="color: #D4AF37;">New Contact Form Submission</p>
                </div>
                <div style="padding: 20px;">
                    <p><strong style="color: #D4AF37;">👤 Name:</strong> <span style="color: #FFF;">{name}</span></p>
                    <p><strong style="color: #D4AF37;">📧 Email:</strong> <span style="color: #FFF;">{email}</span></p>
                    <p><strong style="color: #D4AF37;">🏢 Company:</strong> <span style="color: #FFF;">{company if company else 'Not provided'}</span></p>
                    <p><strong style="color: #D4AF37;">💬 Message:</strong></p>
                    <div style="background: #1A1A1A; padding: 15px; border-radius: 10px; color: #FFF;">{message}</div>
                </div>
                <div style="text-align: center; padding-top: 15px; border-top: 1px solid #333; color: #888; font-size: 12px;">
                    <p>© 2025 Nova Marketing - Black & Gold Agency</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"NEW MESSAGE\nName: {name}\nEmail: {email}\nCompany: {company}\nMessage: {message}"
        
        msg = MIMEMultipart('alternative')
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email sent to {RECEIVER_EMAIL}")
        return True
    except Exception as e:
        print(f"❌ Email error: {str(e)}")
        return False

# ============================================
# STATIC FILES
# ============================================
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# ============================================
# TEAM DATA
# ============================================
team_members = [
    {'id': 1, 'name': 'Adeel Lodhi', 'title': 'SEO Expert',
     'description': 'Leads search engine optimization strategies, focusing on site structure, traffic growth, and long-term visibility.',
     'skills': ['Keyword Research', 'Technical SEO', 'Link Building', 'Audits'],
     'experience': '2+ years in SEO industry | Worked with 30+ clients | 150% avg traffic increase',
     'image': '👨‍💻'},
    {'id': 2, 'name': 'Inham Sheikh', 'title': 'Google Ads & Performance Expert',
     'description': 'Specializes in ROI-driven campaigns within the Google ecosystem, including funnel optimization and scaling.',
     'skills': ['Google Ads', 'Conversion Tracking', 'ROI Optimization'],
     'experience': '3+ years in PPC | Managed $500K+ ad spend | 2.5x avg ROAS',
     'image': '📊'},
    {'id': 3, 'name': 'Sania Khalid', 'title': 'Meta Ads Expert',
     'description': 'Manages paid acquisition across Meta platforms, focusing on audience targeting, creative testing, and retargeting.',
     'skills': ['FB/Insta Ads', 'Audience Research', 'Lead Generation'],
     'experience': '3+ years in Social Media Ads | 500+ campaigns | 35% avg conversion rate',
     'image': '🎯'},
    {'id': 4, 'name': 'Fouzan Ahmed', 'title': 'Content & Video Specialist',
     'description': 'Transforms brand ideas into high-quality visual content, storytelling, and engaging short-form video.',
     'skills': ['Video Editing', 'Brand Storytelling', 'Short-form Video'],
     'experience': '10+ years in Video Production | 1000+ videos created | 100M+ views generated',
     'image': '🎬'},
    {'id': 5, 'name': 'Danish', 'title': 'Content Creator',
     'description': 'Crafts cohesive messaging across blog posts, ad copies, and scripts to inform, engage, and convert.',
     'skills': ['SEO Content', 'Copywriting', 'Content Strategy'],
     'experience': '2+ years in Content Writing | 500+ articles | Featured on 10+ publications',
     'image': '✍️'}
]

projects = [
    {'id': 1, 'name': 'The Women Lounge By Escobar', 'category': 'Social Media Marketing',
     'description': 'Premium women\'s lifestyle lounge - complete Instagram presence, branding, and social media strategy.',
     'link': 'https://www.instagram.com/thewomenloungebyescobar?igsh=dGIxaGg3djZpZXRy',
     'image': '📸', 'client': 'The Women Lounge', 'results': 'Growing Instagram community'},
    {'id': 2, 'name': 'Marketing Campaign Assets Library', 'category': 'Digital Marketing',
     'description': 'Complete marketing campaign assets, resources, and templates.',
     'link': 'https://drive.google.com/drive/folders/1uocMWVq8GVLwcVfcbMge-XUlFvxieYWD',
     'image': '📁', 'client': 'Nova Marketing', 'results': 'Organized campaign materials'},
    {'id': 3, 'name': 'Nova Marketing Portfolio Presentation', 'category': 'Brand Presentation',
     'description': 'Complete agency portfolio showcasing successful projects and case studies.',
     'link': 'https://drive.google.com/file/d/1a7uzY9Kweii1MZl7BZT3Fy4aZtS9sw7f/view?usp=drive_link',
     'image': '📊', 'client': 'Nova Marketing', 'results': 'Professional portfolio'},
    {'id': 4, 'name': 'SEO Strategy Blueprint 2025', 'category': 'Search Engine Optimization',
     'description': 'Complete SEO strategy document with keyword research and technical SEO.',
     'link': 'https://drive.google.com/file/d/12V1CqvtbENMWXvZ_-eHHWCyVI5IT38P-/view?usp=drive_link',
     'image': '🎯', 'client': 'SEO Clients', 'results': '340% organic traffic growth'}
]

contact_messages = []

# ============================================
# ADMIN AUTH
# ============================================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'novadmin' and password == 'Nova@2025':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/login.html', error='Invalid credentials')
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

# ============================================
# API ROUTES
# ============================================
@app.route('/api/team', methods=['GET'])
def get_team():
    return jsonify(team_members)

@app.route('/api/projects', methods=['GET'])
def get_projects():
    return jsonify(projects)

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    company = data.get('company', '')
    message = data.get('message')
    
    # Save locally
    contact_messages.append({
        'id': len(contact_messages) + 1,
        'name': name, 'email': email, 'company': company,
        'message': message,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    print(f"📩 New message from {name}")
    
    # Send email
    email_sent = send_email_notification(name, email, company, message)
    
    if email_sent:
        return jsonify({'success': True, 'message': 'Message sent! Check your email.'})
    else:
        return jsonify({'success': True, 'message': 'Message saved. Email configuration pending.'})

@app.route('/api/contact/messages', methods=['GET'])
@login_required
def get_messages():
    return jsonify(contact_messages)

@app.route('/api/contact/messages/<int:id>', methods=['DELETE'])
@login_required
def delete_message(id):
    global contact_messages
    contact_messages = [m for m in contact_messages if m['id'] != id]
    return jsonify({'success': True})

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 NOVA MARKETING BACKEND STARTED")
    print("📍 http://localhost:5000")
    print("🔐 Admin: http://localhost:5000/admin/login")
    print("👤 novadmin / Nova@2025")
    print("=" * 60)
    app.run(debug=True, port=5000)
