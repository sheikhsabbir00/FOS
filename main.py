from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI


app = FastAPI(title="Farsin OS Marketing Backend V2.1")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIGURATION ---
OFFICIAL_EMAIL = "farsinos.official@gmail.com"
APP_PASSWORD = "xnruvkralilrmkqy" 

# Lead Model
class LeadRequest(BaseModel):
    company: str
    role: str
    email: str
    workflow: str
    manual_process: str
    chat_platform: str
    chat_id: str

# --- CORE EMAIL ENGINE ---

def send_email(to_email: str, subject: str, html_content: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Farsin OS <{OFFICIAL_EMAIL}>"
    msg["To"] = to_email
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(OFFICIAL_EMAIL, APP_PASSWORD)
            server.sendmail(OFFICIAL_EMAIL, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"❌ Mail Engine Error: {e}")
        return False

def notify_admin_of_new_lead(lead: LeadRequest):
    """অ্যাডমিন নোটিফিকেশন - ক্লিনার টেমপ্লেট ফর CEO ফারসিন"""
    subject = f"🚨 NEW LEAD: {lead.company} | Workflow: {lead.workflow}"
    
    html_content = f"""
    <div style="font-family: Arial, sans-serif; background-color: #0a0f1c; padding: 40px; color: #cbd5e1;">
        <div style="max-width: 600px; margin: auto; background-color: #111827; border: 1px solid #1e293b; border-radius: 12px; overflow: hidden;">
            <div style="background-color: #06b6d4; padding: 20px; color: white; font-weight: bold; text-align: center; font-size: 20px;">
                NEW INBOUND LEAD DETECTED
            </div>
            <div style="padding: 30px;">
                <p style="margin-bottom: 20px;"><strong style="color: #06b6d4;">Company:</strong> {lead.company}</p>
                <p style="margin-bottom: 20px;"><strong style="color: #06b6d4;">Lead Name/Role:</strong> {lead.role}</p>
                <p style="margin-bottom: 20px;"><strong style="color: #06b6d4;">Email:</strong> {lead.email}</p>
                <p style="margin-bottom: 20px;"><strong style="color: #06b6d4;">Workflow Target:</strong> {lead.workflow}</p>
                
                <div style="background-color: #0f172a; padding: 15px; border-radius: 8px; border: 1px solid #1e293b;">
                    <p style="margin: 0; font-weight: bold; color: #06b6d4; margin-bottom: 10px;">Pain Points Analysis:</p>
                    <p style="margin: 0; font-size: 14px; line-height: 1.5;">{lead.manual_process}</p>
                </div>

                <div style="margin-top: 25px; padding-top: 15px; border-top: 1px solid #1e293b;">
                    <p style="margin: 5px 0;"><strong style="color: #06b6d4;">Preferred Platform:</strong> {lead.chat_platform}</p>
                    <p style="margin: 5px 0;"><strong style="color: #06b6d4;">Connection ID/Link:</strong> {lead.chat_id}</p>
                </div>
            </div>
            <div style="background-color: #0f172a; padding: 15px; text-align: center; font-size: 11px; color: #64748b;">
                System generated report for Farsin OS Operations.
            </div>
        </div>
    </div>
    """
    send_email(OFFICIAL_EMAIL, subject, html_content)

def send_client_auto_reply(lead: LeadRequest):
    """ক্লায়েন্টকে কাস্টমাইজড অটো-মেইল (DO NOT ALTER TEXT AS PER CEO)"""
    subject = f"Welcome to Farsin OS, {lead.role.split(',')[0]}! Let's automate {lead.company}."   
    
    html_content = f"""
    <div style="font-family: sans-serif; background-color: #0a0f1c; padding: 40px; color: #e2e8f0;">
        <div style="max-width: 600px; margin: auto; background: #111827; border: 1px solid #1e293b; border-radius: 12px; overflow: hidden;">
            <div style="background: #06b6d4; padding: 20px; text-align: center; color: white; font-weight: bold; font-size: 24px;">FARSIN OS</div>
            <div style="padding: 30px;">
                <h2 style="color: white;">Hi {lead.role.split(',')[0]},</h2>
                <p>Thank you for reaching out to <strong>Farsin OS</strong>. We've received your request to automate the <strong>{lead.workflow}</strong> workflow for <strong>{lead.company}</strong>.</p>
                
                <p style="color: #06b6d4; font-weight: bold; font-size: 15px; margin: 20px 0;">We received your request. CEO Farsin will drop you a message on {lead.chat_platform} shortly.</p>
                
                <div style="background: #0f172a; padding: 20px; border-radius: 8px; border-left: 4px solid #06b6d4; margin: 20px 0;">
                    <p><strong>What happens next?</strong></p>
                    <p>1. Our team will personally reach out to schedule a quick discovery conversation.</p>
                    <p>2. We will analyze the bottleneck in your current process.</p>
                </div>
                <p>Keep an eye on your inbox. Talk to you soon!</p>
                <p>Best Regards,<br><strong>Farsin & The AI Team</strong><br><small>Lead AI Developer & Agency Partner</small></p>
            </div>
            <div style="text-align: center; padding: 20px; font-size: 12px; color: #64748b; border-top: 1px solid #1e293b;">
                © 2026 Farsin OS. Centralized Agency Intelligence.
            </div>
        </div>
    </div>
    """
    send_email(lead.email, subject, html_content)

# --- API ENDPOINTS ---
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    with open("index.html", "r", encoding="utf-8") as file:
        return file.read()

@app.post("/api/submit-lead")
async def submit_lead(lead: LeadRequest, background_tasks: BackgroundTasks):
    # Admin Alert
    background_tasks.add_task(notify_admin_of_new_lead, lead)
    # Client Auto-Reply
    background_tasks.add_task(send_client_auto_reply, lead)
    return {"status": "success", "message": "Lead pipeline triggered successfully."}
