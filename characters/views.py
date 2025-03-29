from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegisterForm, CharacterCreateForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Character
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def index(request):
    form = AuthenticationForm()
    return render(request, 'index.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        char_form = CharacterCreateForm(request.POST)
        if form.is_valid() and char_form.is_valid():
            user = form.save()
            character = char_form.save(commit=False)
            character.user = user
            character.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('index')
        else:
            messages.error(request, 'Ошибка регистрации. Пожалуйста, проверьте введенные данные.')
    else:
        form = UserRegisterForm()
        char_form = CharacterCreateForm()
    return render(request, 'register.html', {'form': form, 'char_form': char_form})


def update_character_after_battle(request, character_id):
    if request.method == 'POST':
        try:
            character = get_object_or_404(Character, id=character_id)
            health_loss = int(request.POST.get('health_loss', 0))
            experience_gain = int(request.POST.get('experience_gain', 0))

            character.update_health()
            character.reduce_health(health_loss)  # Используем метод reduce_health
            character.experience += experience_gain
            old_level = character.level
            character.update_level()
            character.save(update_fields=['health', 'experience', 'level', 'skill_points', 'max_health'])

            if character.level > old_level:  # Если уровень повысился
                return JsonResponse({'status': 'success', 'level_up': True})
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=400)

@login_required
def home(request):
    return render(request, 'haupt_stadt.html', {'user': request.user})

def fight(request):
    enemies = [
        {
            'name': 'Волк',
            'health': 15,
            'image': 'static/images/wolf.png',
            'strength': 3,
            'dexterity': 1,
            'luck': 1
        },
        {
            'name': 'Паук',
            'health': 10,
            'image': '/static/images/spider.png',
            'strength': 2,
            'dexterity': 2,
            'luck': 2
        },
        # Добавьте больше врагов здесь
    ]
    context = {
        'enemies': enemies,
        'user': request.user
    }
    return render(request, 'fight.html', context)


def update_character_health(request, character_id):
    if request.method == 'GET':
        character = get_object_or_404(Character, id=character_id)
        character.update_health()
        return JsonResponse({'status': 'success', 'health': character.health})
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=400)


def distribute_skill_points(request, character_id):
    character = get_object_or_404(Character, id=character_id)
    if request.method == 'POST':
        strength_points = int(request.POST.get('strength_points', 0))
        dexterity_points = int(request.POST.get('dexterity_points', 0))
        endurance_points = int(request.POST.get('endurance_points', 0))
        luck_points = int(request.POST.get('luck_points', 0))

        total_points = strength_points + dexterity_points + endurance_points + luck_points
        if total_points <= character.skill_points:
            character.strength += strength_points
            character.dexterity += dexterity_points
            character.endurance += endurance_points
            character.luck += luck_points

            # Увеличение HP за каждое очко выносливости
            character.max_health += endurance_points * 10
            character.health = min(character.health, character.max_health)

            character.skill_points -= total_points
            character.save()
            return redirect('home')  # Перенаправление на главную страницу после распределения очков

    context = {
        'character': character
    }
    return render(request, 'distribute_skill_points.html', context)