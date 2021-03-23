# webmonit
Prosta aplikacja do automatycznego monitorowania stron internetowych

## Aplikacja
* ma możliwość zdefiniowania, edycji, usunięcia monitorowanej strony internetowej,
* ma możliwość ustawienia interwału czasowego dla każdej monitorowanej strony który będzie odpowiadał za częstotliwość zapytań sprawdzających działanie,
* wykrywa błędy w działaniu strony poprzez zapisywanie jej kodu odpowiedzi,
* zapisuje zmiany w kodzie odpowiedzi dzięki czemu można stwierdzić kiedy problem miał miejsce i kiedy się zakończył,
* wyświetla historię/log strony zawierający zmiany w kodzie odpowiedzi oraz zmiany w częstotliwości obserwacji strony,
* posiada specjalny widok wyświetlający strony z którymi jest aktualnie problem.

## Wykorzystywane biblioteki
* django,
* celery, 
* requests, 
* django_celery_beat, 
* redis,
___________

## Instalacja:
1. Wklej folder webmonit do Twojego projektu.
2. Dodaj kilka aplikacji do INSTALLED_APPS w pliku settings.py
 
	INSTALLED_APPS = [
	    'webmonit.apps.WebmonitConfig',
	    'widget_tweaks',
	    'requests',
	    'django_celery_beat',
	...
	]

3. Na końcu settings.py dodaj:
	CELERY_BROKER_URL = 'redis://localhost:6379'
	CELERY_RESULT_BACKEND = 'redis://localhost:6379'
	CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

4. W webmonit.celery.py dostosuj poniższą linię do swojego projektu.
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

5. Dodaj webmonit do URLconf w urls.py Twojego projektu w następujący sposób:
	path('webmonit/', include('webmonit.urls')),

6. Uruchom python manage.py migrate aby stworzyć modele.

7. Uruchom server i wejdź na http://127.0.0.1:8000/webmonit/ aby skorzystać z aplikacji

8. Panel administratora jest dostępny pod http://127.0.0.1:8000/admin/

9. Uruchom cellery:
	celery -A webmonit worker -l info
	celery -A webmonit beat -l INFO


## TODO:
* testy,
* przygotowanie pakietu z aplikacją.
* uruchamianie celery wraz z odpaleniem serwera
* wykorzystanie django-rest-frameworka w formie jakiegoś 1 może 2 endpointów 

