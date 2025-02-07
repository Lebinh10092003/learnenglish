from django.shortcuts import render
import os
import pyttsx3
from .models import Vocabulary
from django.http import HttpResponse
from django.contrib.postgres.search import TrigramSimilarity
from dotenv import load_dotenv
import logging
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Vocabulary, UserVocabulary
import json
import random
from datetime import datetime

# Đảm bảo cấu hình logging
logging.basicConfig(level=logging.INFO)

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
# Load API key từ tệp .env
load_dotenv()

# Lấy API Key từ môi trường
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def search_word(request):
    request.session['current_page'] = 'search_word'
    return render(request, 'search_word.html')

def search_suggestions(request):
    query = request.GET.get('query', '')
    suggestions = []

    if query:
        try:
            # Sử dụng TrigramSimilarity để tìm các từ có độ tương đồng cao nhất với từ tìm kiếm
            suggestions = Vocabulary.objects.annotate(
                similarity=TrigramSimilarity('word', query)
            ).filter(similarity__gt=0.2).order_by('-similarity')[:7]  # Tăng ngưỡng tìm kiếm

            # Chỉ lấy các trường cần thiết và xử lý phần mô tả
            suggestions = [{
                'word': s.word,
                'meaning': process_text_field(s.meaning, 'meaning'),
                'phonetic': process_text_field(s.phonetic, 'phonetic'),
                'description': process_text_field(s.description, 'description'),
                'detail_description': process_text_field(s.detail_description, 'detail_description'),
                'example': process_text_field(s.example, 'example')
            } for s in suggestions]

        except Exception as e:
            logging.error(f"Lỗi khi tìm kiếm: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'suggestions': suggestions})


def process_text_field(field, field_name):
    """
    Hàm xử lý các trường có kiểu dữ liệu chuỗi dài hoặc danh sách.
    Nếu trường là danh sách, nối các phần tử lại thành chuỗi.
    """
    if field:
        # Log kiểu dữ liệu của trường
        #logging.info(f"Kiểu dữ liệu của trường '{field_name}': {type(field)}")

        # Kiểm tra nếu trường là danh sách
        if isinstance(field, list):
            # Nếu là danh sách, chuyển đổi thành chuỗi (tách các phần tử bằng dấu phẩy)
            return [str(item).strip() for item in field][:5]  # Lấy tối đa 5 phần tử đầu tiên

        # Kiểm tra nếu trường là chuỗi
        elif isinstance(field, str):
            return [field.strip()]  # Trường hợp là chuỗi, chuyển thành danh sách với 1 phần tử

        # Nếu là kiểu dữ liệu khác, trả về giá trị của trường dưới dạng chuỗi
        else:
            return [str(field)]  # Chuyển đổi bất kỳ kiểu dữ liệu nào khác thành chuỗi
    return []  # Nếu trường không có dữ liệu, trả về danh sách rỗng

# Ham de doc van ban
def read_text(request):
    # Lấy từ văn bản từ tham số GET
    text = request.GET.get('text', '')

    if text:
        # Thiết lập pyttsx3 để đọc văn bản
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            return JsonResponse({'status': 'success', 'message': 'Text is being read out.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error in reading text: {str(e)}'})
    else:
        return JsonResponse({'status': 'error', 'message': 'No text provided.'})

# Thêm từ vào danh sách học
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils import timezone
from .models import Vocabulary, UserVocabulary

# Thêm từ vào danh sách học
@csrf_exempt
def add_to_learning(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            word = data.get("word")

            # Kiểm tra người dùng đã đăng nhập chưa
            if not request.user.is_authenticated:
                return JsonResponse({'status': 'not_authenticated', 'message': 'Bạn cần đăng nhập để thực hiện chức năng này!'})

            # Kiểm tra từ có tồn tại trong database không, nếu chưa có thì tạo mới
            vocabulary, _ = Vocabulary.objects.get_or_create(word=word)

            # Kiểm tra user đã học từ này chưa
            existing_entry = UserVocabulary.objects.filter(user=request.user, vocabulary=vocabulary).first()

            if existing_entry:
                return JsonResponse({'status': 'exists', 'message': 'Bạn đã học từ này rồi!'})

            # Nếu chưa có, tạo mới
            UserVocabulary.objects.create(user=request.user, vocabulary=vocabulary, is_learned='Learning', learned_at=datetime.now())
            return JsonResponse({'status': 'success', 'message': 'Đã thêm từ vào danh sách học!'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Phương thức không hợp lệ!'})

# Learn new words
@login_required
def learn_new_word(request):
    request.session['current_page'] = 'learn_new_word'
    user = request.user
    user_vocabulary = UserVocabulary.objects.filter(user=user, is_learned='Learning')
    learned_words = UserVocabulary.objects.filter(user=user, is_learned='Learned')
    return render(request, 'learn_new_word.html', {'user_vocabulary': user_vocabulary , 'learned_words': learned_words})


# API random word
@login_required
def random_word(request):
    user = request.user
    words = list(UserVocabulary.objects.filter(user=user, is_learned="Learning"))
    if not words:  # Nếu không có từ nào
        return JsonResponse({
            'error': True,
            'message': 'Bạn đã học hết từ hoặc chưa có từ nào để học.'
        }, status=200)
    
    word_entry = random.choice(words)  # Chọn ngẫu nhiên một từ
    vocabulary = word_entry.vocabulary  # Lấy đối tượng Vocabulary

    # Trường 'meaning' là một danh sách từ, vì vậy trả về toàn bộ danh sách
    meaning_list = vocabulary.meaning if isinstance(vocabulary.meaning, list) else []

    return JsonResponse({
        'word': vocabulary.word,  
        'meaning': meaning_list  
    })

# Cập nhật trạng thái học từ
def update_learning_status_view(request, id):
    try:
        user_vocabulary = UserVocabulary.objects.get(id=id)
        if user_vocabulary.is_learned == 'Learning':
            user_vocabulary.is_learned = 'Learned'
        else:
            user_vocabulary.is_learned = 'Learning'
        user_vocabulary.save()
        return JsonResponse({'status': 'success', 'new_status': user_vocabulary.is_learned})
    except UserVocabulary.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Từ không tồn tại'}, status=404)

def delete_learning_word_view(request, id):
    try:
        user_vocabulary = UserVocabulary.objects.get(id=id)
        user_vocabulary.delete()
        return JsonResponse({'status': 'success', 'message': 'Đã xóa từ'})
    except UserVocabulary.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Từ không tồn tại'}, status=404)