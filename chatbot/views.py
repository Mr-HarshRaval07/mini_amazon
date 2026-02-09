from django.shortcuts import render
from django.http import JsonResponse
import json
from .bot_logic import get_bot_reply

def chatbot_home(request):
    return render(request, 'chatbot/chatbot.html')

def send_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            msg = data.get("message", "")
            reply = get_bot_reply(msg)
            return JsonResponse({"reply": reply})
        except Exception as e:
            return JsonResponse({"reply": f"Backend error: {str(e)}"})