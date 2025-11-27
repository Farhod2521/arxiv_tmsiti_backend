📁 arxiv_tmsiti_backend

Django REST Framework asosida yaratilgan raqamli arxiv boshqaruv tizimi

arxiv_tmsiti_backend — bu tashkilot va muassasalarda hujjatlarni raqamlashtirish, tartibga solish, boshqarish va izlash jarayonini avtomatlashtirish uchun yaratilgan backend tizimi. Loyiha foydalanuvchi rollari, kategoriyalar, yig‘ma-jildlar, hujjatlar, arxiv strukturasini boshqarish va xavfsiz autentifikatsiya kabi funksiyalarni o‘z ichiga oladi.

🚀 Asosiy imkoniyatlar
👤 Role & User Management

Admin, Direktor, Ijro nazorati, Xodim kabi rollarni yaratish va boshqarish

Telefon raqam orqali ro‘yxatdan o‘tish (password + token)

To‘liq ism, rol, telefon, qo‘shilgan sana saqlanishi

🗂 Kategoriyalar va Bo‘limlar

BigCategory — katta bo‘limlarni boshqarish

Category — bo‘limlarga tegishli kichik kategoriyalar

ichki_raqam

tartib_raqami (yig‘ma jild sarlavhasi)

izoh

order (tartib bo‘yicha chiqarish)

📄 Hujjatlar boshqaruvi

Har bir kategoriya uchun hujjat yuklash (PDF format)

Hujjat nomi, fayl, kategoriya bo‘yicha saqlash

Admin panelda qulay boshqaruv

🔐 Autentifikatsiya

DRF Token Authentication

Login (phone + password)

Logout

User profili qaytarish API

📤 REST API

Kategoriyalar bo‘yicha filtrlash

Hujjatlar ro‘yxati

Katta bo‘lim → kichik bo‘lim → hujjatlar zanjiri

JSON formatda toza, qulay chiqish

🎛 Django Admin optimizatsiyasi

Jazzmin bilan chiroyli admin panel

Category, BigCategory, Doc bo‘yicha tartiblangan ko‘rinish

Role & User uchun qulay CRUD

🧱 Texnologiyalar

Backend: Django 5+, Django REST Framework

Database: PostgreSQL

Auth: DRF TokenAuth

Admin UI: Jazzmin

Docs: Swagger / drf-yasg

Deploy: Gunicorn + Nginx + Supervisor

Static/Media: Nginx orqali servis