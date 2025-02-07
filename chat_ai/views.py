from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from vocabulary.models import UserVocabulary
import openai
import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Lấy API Key từ biến môi trường
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Cấu hình API Key cho OpenAI
openai.api_key = OPENAI_API_KEY

def generate_conversation(vocab_list, user_input):
    """Tạo câu trả lời và ngữ cảnh từ ChatGPT dựa trên từ vựng đã học."""
    if not vocab_list:
        return "Bạn chưa có từ vựng nào để luyện tập. Hãy thêm từ vào danh sách học!"

    prompt = f"""
    Bạn là một trợ lý giúp người học luyện tập từ vựng tiếng Anh. Hãy tạo câu trả lời phù hợp dựa trên tin nhắn của người dùng.
    Danh sách từ vựng cần luyện tập: {', '.join(vocab_list)}

    Người dùng: {user_input}
    """

    try:
        # Sử dụng API mới với openai.chat.completions.create
        response = openai.chat.completions.create(  # Thay đổi quan trọng ở đây
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là một trợ lý dạy tiếng Anh."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()    # Thay đổi quan trọng ở đây
    except Exception as e:
        return f"Lỗi khi gọi API: {str(e)}"

def home_chat(request):
    request.session['current_page'] = 'chat_ai'
    return render(request, 'home_chat.html')


@login_required
def chatbox_view(request):
    """Lấy danh sách từ vựng và gửi câu hỏi cho ChatGPT"""
    user_vocab_list = UserVocabulary.objects.filter(
        user=request.user, is_learned__in=['Not Learned', 'Learning']
    ).values_list('vocabulary__word', flat=True)

    vocabulary_words = list(user_vocab_list)

    if request.method == "POST":
        user_input = request.POST.get("user_input", "")
        bot_response = generate_conversation(vocabulary_words, user_input)
        return JsonResponse({"bot_response": bot_response})

    return render(request, 'chatbox.html', {'vocabulary_list': vocabulary_words})

def sentence_correction_review(request):
    return render(request, 'sentence_correction.html')