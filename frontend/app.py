import gradio as gr
import requests

REPLY_API = "http://127.0.0.1:8000/generate_reply"
IMPROVE_API = "http://127.0.0.1:8000/improve_email"

# Response functions
def generate_reply(email, tone):
    if not email.strip():
        return "❗ Please enter an email."
    try:
        payload = {"email": email, "tone": tone}
        response = requests.post(REPLY_API, json=payload)
        return response.json().get("reply", "⚠️ Failed to generate reply.")
    except:
        return "🚫 Could not reach backend."

def improve_email(email):
    if not email.strip():
        return "❗ Please enter an email."
    try:
        payload = {"email": email}
        response = requests.post(IMPROVE_API, json=payload)
        return response.json().get("improved", "⚠️ Failed to improve email.")
    except:
        return "🚫 Could not reach backend."

# Highlight logic
def highlight_buttons(last_clicked):
    if last_clicked == "reply":
        return gr.update(variant="primary"), gr.update(variant="secondary")
    else:
        return gr.update(variant="secondary"), gr.update(variant="primary")

# Gradio layout
with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("# ✨ Smart Email Assistant")

    email_input = gr.Textbox(
        lines=12,
        label="📥 Paste Email (Received or Drafted)",
        placeholder="e.g. Hey, can you send the report soon?"
    )

    tone_input = gr.Dropdown(
        ["Formal", "Friendly", "Sarcastic", "Enthusiastic"],
        label="🎭 Choose Tone (Only for Replies)",
        value="Formal"
    )

    last_clicked = gr.State(value="")  # Track last button clicked

    with gr.Row():
        reply_btn = gr.Button("✉️ Generate Reply Mail", elem_id="reply-btn")
        improve_btn = gr.Button("🛠 Improve This Email", elem_id="improve-btn")

    output_box = gr.Textbox(
        lines=12,
        label="📝 AI Output",
        placeholder="The result will appear here..."
    )

    reply_btn.click(
        fn=generate_reply,
        inputs=[email_input, tone_input],
        outputs=output_box
    ).then(fn=highlight_buttons, inputs=gr.State("reply"), outputs=[reply_btn, improve_btn])

    improve_btn.click(
        fn=improve_email,
        inputs=email_input,
        outputs=output_box
    ).then(fn=highlight_buttons, inputs=gr.State("improve"), outputs=[reply_btn, improve_btn])

app.launch()
