Для запуска приложения необходимо использовать docker-compose build в директории task_tracker. используется Python 3.6.3, поэтому следить за совместимостью нет необходимости.
Зависимости в requirements.txt описаны так же для Python 3.6.

Приложение предоставляет API для управдения простым Task Tracker'ом.
При первом запуске неоюходимо создать superuser через manage.py для того, чтобы войти в админку http://0.0.0.0/admin/ и создать неодходимых юзеров, проекты и статусы.
Это возможно как через команду manage в docker-entrypoint.sh так и через docker-compose exec server bash и дальнейшей команде через терминал.

После этого можно воспользоваться командой test из docker-entrypoint.sh для запуска тестов.
База для использования: sqlite.

Для запуска советуется использовать стандартные настройки в docker-compose.yml, команда dev, при желании можно указать настройку volume для изменений директории с кодом.
Так же можно воспользоваться help для понимания команд, доступных при запуске.

Описание API:
  - api/task/$ - отображение текущих тасков и добавление новых через POST
  - api/task/(?P<pk>[0-9]+)/$ - информация про конкртный таск
  - api/comment/$ - отображение текущих комментов и добавление новых через POST
  - api/comment/(?P<pk>[0-9]+)/$ - отображение информации по комментам
  
Везде сипользуется DRF для действий (создание, измение, удаление)
Особенности:
  - При удалении тасков - удаляются все комментарии к ним и описания
  - При изменении доступны поля status и assignee, осальные игнорируются, но можно получить 400 на некорректный запрос
  - Права доступа не предусмотрены в этой версии, требует доработки при необходимости (все видят все и могут изменять, главное быть залогиненным в системе)
  - При изменении тасков, меняется поле updated для них, чтобы следить за изменением
  - логирование не включено, требует настройки
  - обращение к таскам идет по id в праметрах урла по базису DRF
  - вид тасков приспособлен для лучшего отобрадения, имена статусов и проектов - уникальные
  - есть unit тесты на модели и func на API
  - есть search для поиска по основным полям (текстовая информация) и дильтр по каждому основному полю

Образ Docker для запуска: 3.6.3.
