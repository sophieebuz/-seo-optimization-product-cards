## Checkpoint 6
## Запуск через kubernetes (minikube):
  1. `minikube start` запустить куребнетес-кластер (запускала с параметрами --driver=docker --memory=4096 --cpus=8)
  2. `minikube addons enable ingress` установить ingress-nginx провайдер
  3.  `.\k8s\k8s_apply.ps1` создать абстакции, дождаться пока status не станет running (запуск ps-скрипта - если windows, запустить вручную команды, прописанные в данном файле - если другая os)
  4. `kubectl port-forward pods/<ingress-nginx-controller-yourhash> -n ingress-nginx 62123:80` дать доступ к ingress извне
  5. `kubectl port-forward service/flower -n seo 55555:5555` дать доступ к сервису flower извне

Дальнейшие команды можно делать в любом поряке:
  - перейти в браузер по следующему url:
    -  `http://localhost:62123/seo-classification/training` для запуска обучения модели (можно понажимать несколько раз, пообновлять страницу, дождать конца обучения и тому подобного рода разные взаимодействия со страницей)
    -  `http://localhost:62123/seo-classification/` для инференса
    -  `http://localhost:55555` для сервиса flower

_Примечание:_ сервисы могут подняться и начать отвечать не сразу, иногда необходимо какое то время подождать

_Примечание1:_ проект может дорабатываться/изменяться в течении выполнения дз  
_Примечание2:_ на данный момент исп-ся упрощенная классификация (бинарная) с классами "bluzki-i-rubashki" и "antistress" (для примера на fastapi сервис можно подать [следующую картинку](https://diamondelectric.ru/images/2243/2242766/igryshkaantistress_expetro_1.jpg))
____
Общие сведения о проекте
# SEO-оптимизация карточек товара на маркетплейсах

# Студенты, выполняющие работы:
Бузаева Софья Михайловна, telegram: @ethee_real 

Куликов Дмитрий Алексевич, telegram: @dmitry_kulikov17

# Научный руководитель
Хажгериев Мурат Анзорович, telegram: @greedisneutral

# Постановка задачи
Идея: Помочь продавцам на маркетплейсах в заполнении seo карточки товара. Продавец делает фотографию товара и загружает его в сервис (телеграмм бот/web-приложение). Пользователю будет сгенерировано описание товара (можно, заранее задать ключевые слова) и подобрана наиболее подходящая категория. Правильно подобранная категория сильно повышает продажи на маркетплейсах. 

В будущем проект может быть использован для полноценного создания карточки товара на маркетплейсах с использованием их api методов. Делая только фотографию товара, пользователь может в несколько кликов выложить его на продажу сразу в нескольких торговых площадок, при этом не тратя время на изучение и особенностей их политик.

Допущения по ВКР: 
1. Рассматриваем два наиболее популярных маркетплейса в РФ: Ozon и Wildberries.
2. В рамках выполнения ВКР выберем только несколько видов категорий товаров, так как на площадках их присутсвует более 1000 штук (при этом список категорий динамический, со временем они могут добавляться/изменяться/удаляться). Это допущение делаем из за ограниченности во времени и вычислительных ресурсах.

# Этап работы:
1. Провести анализ данных. Написать парсеры маркетплейсов, чтобы собрать данные по товарам, категориям, описанию, фотографии и т.д. (20.03)
2. Подготовить проект по инфраструктурной части (настройка окружения, менеджемент зависимостей). (31.03)
3. Получаем из картинок эмбеддинги и обучаем на них классификатор с таргетом в виде категории товара. (31.04)
4. Также по этому эмбеддингу мы хотим получить описание товара (здесь можно воспользоваться готовыми АПИ или поднять свой инстанс LLM, которая будет генерить описание). (31.05)
5. Написание сервиса в виде телеграмм бота или web/приложения. (31.05)

# Анализ данных

Согласно [исследованию](https://www.retail.ru/news/tinkoff-ecommerce-v-2023-godu-kolichestvo-pokupok-na-marketpleysakh-vyroslo-na-6-29-yanvarya-2024-237087/) команды Tinkoff Ecommerce: самой привлекательной платформой для старта бизнеса является Wildberries: 63% продавцов в конце 2023 года выбирали ее в качестве первой площадки.

<img width="862" alt="image" src="https://github.com/Kulikov17/seo-optimization-product-cards/assets/61663158/66286c42-b768-4d40-a4ec-ae67740334e8">


Анализ парсинга Ozon:
1. Сильная защита, частая блокировка пользователей, смена userAgent не всегда помогает.
2. На странице много динамического контента и ленивой подгрузки, что создает трудности при парсинге динамически подгружаемых категорий.
3. Огромное количество подкатегорий товара.
4. Сложный парсинг товара:
   - Динамическая подгрузка отзывов, чтобы брать картинки из них.
   - Большая вариативность описания товара, нет единного шаблонна для парсинга. Так например, когда-то вместо текстов могут быть просто картинки или описание товара сопряженно с картинкой.


Анализ парсинга Wildberries:
1. Слабая защита, не требуется смена userAgent.
2. Статический контент для парсинга категорий и подкатегорий.
3. При парсинге товаров существует их ленивая подгрузка: для одной подкатегорий подгружается 15 товаров, чтобы подгрузить следующую пачку нужно проскроллить вниз.
4. Единное оформление карточки товара, упрощает парсинг товара: его описание, характеристики, фотографии из сео и из отзывов.


Итог: 
Принято решения писать ВКР для селлеров, использующий Wildberries, так как им чаще всего пользуются и он легче подается парсингу. В качестве направления дальнейшего развития можно рассмотреть другие маркетплейсы.


# Требования к запуску продукта:
  - Python 3.10
  - Poetry >= 1.0.0

## Стек технологий
Бэкенд будет написан на Python с использованием FastAPI. Модели будут написаны на pytorch. Для хранения фото и обработки фото может понадобится БД.

Если UI будет реализован в виде телеграмма бота, то предлагается использование библиотеки [aiogram](https://docs.aiogram.dev/en/latest/api/types/chat.html). В отличие от chatbot она предлагает использование ассинхронности, которая будет необходима при обработке и передачи фотографий и изображений.

Если UI будет реализован в виде web, то предлагается использование фреймворка Angular, так как есть опыт работы на нем, плюс позволяет создавать гибкие и масштабируемые решения.

<img width="627" alt="image" src="https://github.com/Kulikov17/seo-optimization-product-cards/assets/61663158/6bed9a33-21db-4950-8929-0916d7e52144">
