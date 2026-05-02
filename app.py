from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from flask_cors import CORS
from functools import wraps
from datetime import datetime
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = 'nova-secret-key-2025'
CORS(app)

# ============================================
# TEAM MEMBERS DATA (UPDATED EXPERIENCE YEARS)
# ============================================
team_members = [
    {
        'id': 1, 'name': 'Adeel Lodhi', 'title': 'SEO Expert',
        'description': 'Leads search engine optimization strategies, focusing on site structure, traffic growth, and long-term visibility.',
        'skills': ['Keyword Research', 'Technical SEO', 'Link Building', 'Audits'],
        'experience': '2+ years in SEO industry | Worked with 30+ clients | 150% avg traffic increase',
        'image': '👨‍💻'
    },
    {
        'id': 2, 'name': 'Inham Sheikh', 'title': 'Google Ads & Performance Expert',
        'description': 'Specializes in ROI-driven campaigns within the Google ecosystem, including funnel optimization and scaling.',
        'skills': ['Google Ads', 'Conversion Tracking', 'ROI Optimization'],
        'experience': '3+ years in PPC | Managed $500K+ ad spend | 2.5x avg ROAS',
        'image': '📊'
    },
    {
        'id': 3, 'name': 'Sania Khalid', 'title': 'Meta Ads Expert',
        'description': 'Manages paid acquisition across Meta platforms, focusing on audience targeting, creative testing, and retargeting.',
        'skills': ['FB/Insta Ads', 'Audience Research', 'Lead Generation'],
        'experience': '3+ years in Social Media Ads | 500+ campaigns | 35% avg conversion rate',
        'image': '🎯'
    },
    {
        'id': 4, 'name': 'Fouzan Ahmed', 'title': 'Content & Video Specialist',
        'description': 'Transforms brand ideas into high-quality visual content, storytelling, and engaging short-form video.',
        'skills': ['Video Editing', 'Brand Storytelling', 'Short-form Video'],
        'experience': '10+ years in Video Production | 1000+ videos created | 100M+ views generated',
        'image': '🎬'
    },
    {
        'id': 5, 'name': 'Danish', 'title': 'Content Creator',
        'description': 'Crafts cohesive messaging across blog posts, ad copies, and scripts to inform, engage, and convert.',
        'skills': ['SEO Content', 'Copywriting', 'Content Strategy'],
        'experience': '2+ years in Content Writing | 500+ articles | Featured on 10+ publications',
        'image': '✍️'
    }
]

# ============================================
# PROJECTS DATA (WITH YOUR LINKS)
# ============================================
projects = [
    {
        'id': 1,
        'name': 'The Women Lounge By Escobar',
        'category': 'Social Media Marketing',
        'description': 'Premium women\'s lifestyle lounge - complete Instagram presence, branding, and social media strategy.',
        'link': 'https://www.instagram.com/thewomenloungebyescobar?igsh=dGIxaGg3djZpZXRy',
        'image': '📸',
        'client': 'The Women Lounge',
        'results': 'Growing Instagram community | Increased brand visibility'
    },
    {
        'id': 2,
        'name': 'Marketing Campaign Assets Library',
        'category': 'Digital Marketing',
        'description': 'Complete marketing campaign assets, resources, and templates for successful campaign execution.',
        'link': 'https://drive.google.com/drive/folders/1uocMWVq8GVLwcVfcbMge-XUlFvxieYWD',
        'image': '📁',
        'client': 'Nova Marketing',
        'results': 'Organized campaign materials | Streamlined workflow'
    },
    {
        'id': 3,
        'name': 'Nova Marketing Portfolio Presentation',
        'category': 'Brand Presentation',
        'description': 'Complete agency portfolio showcasing successful projects, case studies, and client success stories.',
        'link': 'https://drive.google.com/file/d/1a7uzY9Kweii1MZl7BZT3Fy4aZtS9sw7f/view?usp=drive_link',
        'image': '📊',
        'client': 'Nova Marketing',
        'results': 'Professional portfolio | Client winning presentations'
    },
    {
        'id': 4,
        'name': 'SEO Strategy Blueprint 2025',
        'category': 'Search Engine Optimization',
        'description': 'Complete SEO strategy document with keyword research, technical SEO, content planning, and link building strategies.',
        'link': 'https://drive.google.com/file/d/12V1CqvtbENMWXvZ_-eHHWCyVI5IT38P-/view?usp=drive_link',
        'image': '🎯',
        'client': 'SEO Clients',
        'results': '340% organic traffic growth | Top rankings'
    }
]

contact_messages = []

# ============================================
# ADMIN AUTHENTICATION
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

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

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

@app.route('/api/team', methods=['GET'])
def get_team():
    return jsonify(team_members)

@app.route('/api/team', methods=['POST'])
@login_required
def add_team():
    data = request.json
    new_id = max([m['id'] for m in team_members]) + 1 if team_members else 1
    new_member = {
        'id': new_id, 'name': data['name'], 'title': data['title'],
        'description': data['description'], 'skills': data['skills'],
        'experience': data.get('experience', ''), 'image': data.get('image', '👤')
    }
    team_members.append(new_member)
    return jsonify(new_member)

@app.route('/api/team/<int:id>', methods=['PUT'])
@login_required
def update_team(id):
    data = request.json
    for member in team_members:
        if member['id'] == id:
            member.update(data)
            return jsonify(member)
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/team/<int:id>', methods=['DELETE'])
@login_required
def delete_team(id):
    global team_members
    team_members = [m for m in team_members if m['id'] != id]
    return jsonify({'success': True})

@app.route('/api/projects', methods=['GET'])
def get_projects():
    return jsonify(projects)

@app.route('/api/projects', methods=['POST'])
@login_required
def add_project():
    data = request.json
    new_id = max([p['id'] for p in projects]) + 1 if projects else 1
    new_project = {
        'id': new_id, 'name': data['name'], 'category': data['category'],
        'description': data['description'], 'link': data['link'],
        'image': data.get('image', '📁'), 'client': data.get('client', ''),
        'results': data.get('results', '')
    }
    projects.append(new_project)
    return jsonify(new_project)

@app.route('/api/projects/<int:id>', methods=['PUT'])
@login_required
def update_project(id):
    data = request.json
    for project in projects:
        if project['id'] == id:
            project.update(data)
            return jsonify(project)
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/projects/<int:id>', methods=['DELETE'])
@login_required
def delete_project(id):
    global projects
    projects = [p for p in projects if p['id'] != id]
    return jsonify({'success': True})

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    data = request.json
    message = {
        'id': len(contact_messages) + 1,
        'name': data['name'],
        'email': data['email'],
        'company': data.get('company', ''),
        'message': data['message'],
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    contact_messages.append(message)
    print(f"📩 New message from {data['name']}")
    return jsonify({'success': True})

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

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 NOVA MARKETING BACKEND STARTED")
    print("📍 http://localhost:5000")
    print("🔐 Admin: http://localhost:5000/admin/login")
    print("👤 novadmin / Nova@2025")
    print("=" * 60)
    app.run(debug=True, port=5000)