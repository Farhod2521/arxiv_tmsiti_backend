from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import User, Role, BigCategory, Doc
from .serializers import LoginSerializer, BigCategorySerializer, DocSerializer


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

        if user_role is None:
            return Response({"error": "Foydalanuvchi roli mavjud emas"}, status=400)

        # ADMIN VA DIREKTOR BARCHA BO‘LIMLARNI KO‘RADI
        if user_role.name.lower() in ["admin", "direktor", "director"]:
            big_categories = BigCategory.objects.all().order_by("id")

        else:
            # Oddiy role faqat o‘ziga tegishli bo‘limlarni ko‘radi
            big_categories = BigCategory.objects.filter(role=user_role).order_by("id")

        serializer = BigCategorySerializer(big_categories, many=True)
        return Response(serializer.data)



# -------------------------
#   DocUpdateDeleteAPIView
# -------------------------
class DocUpdateDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    # ---- CREATE: Yangi hujjat qo‘shish ----
    def post(self, request):
        serializer = DocSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Hujjat muvaffaqiyatli yaratildi",
            "data": serializer.data
        }, status=201)

    # ---- DELETE: Bir nechta hujjat o'chirish ----
    def delete(self, request):
        ids = request.data.get("ids", None)

        if not ids:
            return Response({"error": "ids bo‘sh bo‘lishi mumkin emas. Masalan: [3, 7, 10]"},
                            status=400)

        if not all(isinstance(i, int) for i in ids):
            return Response({"error": "ids faqat integer bo‘lishi kerak"}, status=400)

        docs = Doc.objects.filter(id__in=ids)

        if not docs.exists():
            return Response({"error": "Berilgan ID bo‘yicha hujjatlar topilmadi"}, status=404)

        count = docs.count()
        docs.delete()

        return Response({
            "message": f"{count} ta hujjat muvaffaqiyatli o‘chirildi",
            "deleted_ids": ids
        })

    # ---- UPDATE: Bitta hujjat yangilash ----
    def put(self, request, pk):
        try:
            doc = Doc.objects.get(id=pk)
        except Doc.DoesNotExist:
            return Response({"error": "Hujjat topilmadi"}, status=404)

        serializer = DocSerializer(doc, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Hujjat muvaffaqiyatli yangilandi",
            "data": serializer.data
        })