from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_welcome_email(user_email, user_name):
    """
    Send welcome email to newly registered user
    """
    subject = '🎉 Welcome to FIREPY - Registration Successful!'
    
    # HTML Email Content
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                padding: 20px;
                margin: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                overflow: hidden;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            }}
            .header {{
                background: linear-gradient(135deg, #9d7cbf 0%, #7952a8 100%);
                padding: 40px 20px;
                text-align: center;
                color: white;
            }}
            .header h1 {{
                margin: 0;
                font-size: 2.5em;
                text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            }}
            .content {{
                padding: 40px 30px;
                color: #333;
            }}
            .content h2 {{
                color: #7952a8;
                margin-top: 0;
            }}
            .content p {{
                font-size: 1.1em;
                line-height: 1.6;
                color: #666;
            }}
            .button {{
                display: inline-block;
                background: linear-gradient(135deg, #9d7cbf 0%, #7952a8 100%);
                color: white;
                padding: 15px 40px;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                margin: 20px 0;
                box-shadow: 0 5px 15px rgba(157, 124, 191, 0.4);
            }}
            .features {{
                background: #f5f0fb;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
            }}
            .features ul {{
                list-style: none;
                padding: 0;
            }}
            .features li {{
                padding: 10px 0;
                color: #7952a8;
                font-weight: 500;
            }}
            .features li:before {{
                content: "🎵 ";
                margin-right: 10px;
            }}
            .footer {{
                background: #1a1a1a;
                color: #c8b3e6;
                text-align: center;
                padding: 20px;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>♫ F I R E P Y ♫</h1>
                <p style="margin: 10px 0 0 0; font-size: 1.2em;">Your Music Journey Starts Here!</p>
            </div>
            
            <div class="content">
                <h2>Welcome, {user_name}! 🎉</h2>
                <p>
                    Thank you for joining <strong>FIREPY</strong> - your ultimate music streaming platform!
                    We're thrilled to have you as part of our growing community of music lovers.
                </p>
                
                <p>
                    Your account has been successfully created and you're all set to explore
                    thousands of songs across multiple genres.
                </p>
                
                <div style="text-align: center;">
                    <a href="http://127.0.0.1:8000/login/" class="button">Start Listening Now 🎧</a>
                </div>
                
                <div class="features">
                    <h3 style="color: #7952a8; margin-top: 0;">What You Can Do:</h3>
                    <ul>
                        <li>Stream unlimited songs from our vast library</li>
                        <li>Create and manage your personal playlists</li>
                        <li>Like your favorite tracks</li>
                        <li>Track your listening history</li>
                        <li>Discover new artists and genres</li>
                        <li>Enjoy ad-free music experience</li>
                    </ul>
                </div>
                
                <p>
                    If you have any questions or need assistance, feel free to reach out to our
                    support team anytime.
                </p>
                
                <p style="margin-top: 30px;">
                    Happy Listening! 🎶<br>
                    <strong>The FIREPY Team</strong>
                </p>
            </div>
            
            <div class="footer">
                <p>© 2026 FIREPY. All Rights Reserved.</p>
                <p>You're receiving this email because you registered on FIREPY.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Plain text version (fallback)
    plain_message = f"""
    Welcome to FIREPY, {user_name}!
    
    Thank you for joining our music streaming platform!
    Your account has been successfully created.
    
    Start listening now: http://127.0.0.1:8000/login/
    
    Happy Listening!
    The FIREPY Team
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"✅ Welcome email sent to {user_email}")
        return True
    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")
        return False