from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import User, Role, BigCategory, Doc, Category
from .serializers import LoginSerializer, BigCategorySerializer, DocSerializer, RoleSerializer,CategoryCRUDSerializer
from django.db import transaction
import json
from django.shortcuts import get_object_or_404
class WordDataImportAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            
            with transaction.atomic():
                for role_data in data:
                    # Role yaratish yoki olish
                    role_name = role_data.get('name')
                    role, created = Role.objects.get_or_create(name=role_name)
                    
                    # BigCategory lar yaratish
                    for big_category_data in role_data.get('big_categories', []):
                        big_category_title = big_category_data.get('title')
                        big_category, created = BigCategory.objects.get_or_create(
                            title=big_category_title,
                            role=role
                        )
                        
                        # Category lar yaratish
                        for category_data in big_category_data.get('categories', []):
                            Category.objects.create(
                                big_category=big_category,
                                ichki_raqam=category_data.get('ichki_raqam', ''),
                                tartib_raqami=category_data.get('tartib_raqami', ''),
                                izoh=category_data.get('izoh', ''),
                                order=category_data.get('order', 0)
                            )
            
            return Response({
                'message': 'Ma\'lumotlar muvaffaqiyatli import qilindi',
                'imported_roles': len(data)
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': f'Import jarayonida xatolik: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

# -------------------------
#   LOGIN API
# -------------------------

from rest_framework.permissions import AllowAny

class LoginAPIView(APIView):
    authentication_classes = []        # CSRF check bo‘lmaydi
    permission_classes = [AllowAny]    # Login uchun ruxsat beriladi

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone"]
        password = serializer.validated_data["password"]

        user = authenticate(request, phone=phone, password=password)

        if not user:
            return Response({"error": "Telefon raqam yoki parol noto‘g‘ri"}, status=400)

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Muvaffaqiyatli tizimga kirdingiz",
            "token": token.key,
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "phone": user.phone,
                "role": user.role.name if user.role else None,
            }
        })

    
# -------------------------
#   LOGOUT API
# -------------------------
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Tokenni o‘chiradi → avtomatik logout
        request.user.auth_token.delete()

        return Response({"message": "Muvaffaqiyatli tizimdan chiqdingiz"})
    
# -------------------------
#   My Profile 
# -------------------------
class MyProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "id": user.id,
            "full_name": user.full_name,
            "phone": user.phone,
            "role": user.role.name if user.role else None,
            "created_at": user.create_at,
        }, status=status.HTTP_200_OK)

# -------------------------
#   DocumentListAPIView
# -------------------------
class DocumentListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_role = request.user.role
        title = request.query_params.get("title")  # 🔑 query param

        if user_role is None:
            return Response(
                {"error": "Foydalanuvchi roli mavjud emas"},
                status=400
            )

        # 🔐 ADMIN / DIREKTOR
        if user_role.name.lower() in ["admin", "direktor", "director"]:
            big_categories = BigCategory.objects.all()
        else:
            big_categories = BigCategory.objects.filter(role=user_role)

        # 🔎 TITLE BO‘YICHA FILTER
        if title:
            big_categories = big_categories.filter(title__iexact=title)

        big_categories = big_categories.order_by("id")

        serializer = BigCategorySerializer(big_categories, many=True)
        return Response(serializer.data)



# -------------------------
#   DocUpdateDeleteAPIView
# -------------------------
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Doc
from .serializers import DocSerializer


class DocUpdateDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # ✅ GET (ID bo‘yicha bitta hujjat olish)
    def get(self, request, pk):
        try:
            doc = Doc.objects.get(id=pk)
        except Doc.DoesNotExist:
            return Response({"error": "Hujjat topilmadi"}, status=404)

        serializer = DocSerializer(doc, context={"request": request})
        return Response({
            "message": "Hujjat topildi",
            "data": serializer.data
        })

    # ✅ CREATE
    def post(self, request):
        serializer = DocSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Hujjat muvaffaqiyatli yaratildi",
            "data": serializer.data
        }, status=201)

    # ✅ DELETE (Bir nechta)
    def delete(self, request):
        ids = request.data.get("ids", None)

        if not ids:
            return Response(
                {"error": "ids bo‘sh bo‘lishi mumkin emas. Masalan: [3, 7, 10]"},
                status=400
            )

        docs = Doc.objects.filter(id__in=ids)

        if not docs.exists():
            return Response(
                {"error": "Berilgan ID bo‘yicha hujjatlar topilmadi"},
                status=404
            )

        count = docs.count()
        docs.delete()

        return Response({
            "message": f"{count} ta hujjat o‘chirildi",
            "deleted_ids": ids
        }, status=200)

    def put(self, request, pk):
        try:
            doc = Doc.objects.get(id=pk)
        except Doc.DoesNotExist:
            return Response({"error": "Hujjat topilmadi"}, status=404)

        # Hujjatda category bor, lekin requestda yo'q bo'lsa, o'zgartirmaslik
        data = request.data.copy()
        if 'category' not in data and doc.category:
            data['category'] = doc.category.id
        
        serializer = DocSerializer(doc, data=data)  # to'liq update
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Hujjat to'liq yangilandi",
            "data": serializer.data
        })

    def patch(self, request, pk):
        try:
            doc = Doc.objects.get(id=pk)
        except Doc.DoesNotExist:
            return Response({"error": "Hujjat topilmadi"}, status=404)

        serializer = DocSerializer(doc, data=request.data, partial=True)  # qisman update
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Hujjat qisman yangilandi",
            "data": serializer.data
        })


class CategoryUpdateAPIView(APIView):

    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Kategoriya topilmadi"}, status=404)

        serializer = CategoryCRUDSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)

    # Agar qisman yangilash kerak bo‘lsa (PATCH)
    def patch(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Kategoriya topilmadi"}, status=404)

        serializer = CategoryCRUDSerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)
class CategoryDeleteAPIView(APIView):

    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Kategoriya topilmadi"}, status=404)

        category.delete()
        return Response({"message": "Kategoriya muvaffaqiyatli o‘chirildi"}, status=204)
    
class CategoryCreateAPIView(APIView):

    def post(self, request):
        serializer = CategoryCRUDSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class CategoryReorderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Kategoriyalarni tartibini o'zgartirish
        """
        try:
            data = request.data
            if not isinstance(data, list):
                return Response(
                    {"error": "Ma'lumotlar ro'yxat ko'rinishida bo'lishi kerak"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Har bir kategoriya uchun yangi tartib raqamini o'rnatish
            for item in data:
                category_id = item.get('id')
                new_order = item.get('order')
                
                if category_id and new_order is not None:
                    category = get_object_or_404(Category, id=category_id)
                    category.order = new_order
                    category.save()
            
            return Response(
                {"message": "Kategoriyalar tartibi muvaffaqiyatli yangilandi"},
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )