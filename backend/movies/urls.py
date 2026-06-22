from django.urls import path, include  # นำเข้า path สำหรับกำหนด URL และ include สำหรับเชื่อม URL จากส่วนอื่น
from rest_framework.routers import DefaultRouter  # นำเข้า DefaultRouter เพื่อสร้าง URL ให้กับ ViewSet แบบอัตโนมัติ (เช่น GET, POST, PUT, DELETE)
from .views import DirectorViewSet, MovieViewSet, DVDViewSet, OrderViewSet  # นำเข้า ViewSets ทั้งหมดที่เราสร้างไว้จากไฟล์ views.py

router = DefaultRouter()  # สร้าง instance ของตัว Router ขึ้นมา
router.register('directors', DirectorViewSet)  # ลงทะเบียนเส้นทาง /directors/ ผูกเข้ากับ DirectorViewSet
router.register('movies', MovieViewSet)  # ลงทะเบียนเส้นทาง /movies/ ผูกเข้ากับ MovieViewSet
router.register('dvds', DVDViewSet)  # ลงทะเบียนเส้นทาง /dvds/ ผูกเข้ากับ DVDViewSet
router.register('orders', OrderViewSet, basename='order')  # ลงทะเบียนเส้นทาง /orders/ ผูกเข้ากับ OrderViewSet โดยตั้งชื่อ base ว่า order เพื่อใช้อ้างอิง

urlpatterns = [  # ระบุรายการเส้นทาง (URL Patterns) ที่แอปพลิเคชันรูปแบบนี้จะรองรับ
    path('', include(router.urls)),  # นำ URL อัตโนมัติทั้งหมดที่ router สร้างให้ มาต่อเข้ากับ Root URL ของแอปนี้
]
