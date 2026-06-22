import traceback  # นำเข้า traceback เพื่อใช้สำหรับ print รายละเอียด error แจ้งเตือนใน log

from rest_framework import viewsets, filters, status  # นำเข้า viewsets สำหรับสร้าง API, filters สำหรับค้นหา, และ status สำหรับ HTTP status codes
from rest_framework.permissions import IsAuthenticated  # นำเข้า permission ที่บังคับให้ต้อง login ก่อนถึงจะใช้งานได้
from rest_framework.response import Response  # นำเข้า Response ห่อหุ้มข้อมูลเพื่อส่งกลับไปให้หน้าบ้าน

from .models import Director, Movie, DVD, Order  # นำเข้า Models ทั้งหมดที่เกี่ยวข้อง
from .serializers import (  # นำเข้า Serializers ทั้งหมดที่เกี่ยวข้อง
    DirectorSerializer, MovieSerializer, DVDSerializer,
    OrderSerializer, OrderCreateSerializer,
)
from .permissions import IsAdminRoleOrReadOnly  # นำเข้า permission แบบ custom (ถ้าเป็นแอดมินแก้ไขได้ ถ้าไม่ใช่ดูได้อย่างเดียว)


class DirectorViewSet(viewsets.ModelViewSet):  # สร้างชุด API สำหรับจัดการข้อมูลผู้กำกับ (Director) ดึง/เพิ่ม/แก้ไข/ลบ
    queryset = Director.objects.all().order_by('id')  # ดึงข้อมูลผู้กำกับทั้งหมดจากฐานข้อมูล เรียงลำดับตาม ID
    serializer_class = DirectorSerializer  # ผูกกับ DirectorSerializer เพื่อคัดกรองฟิลด์ก่อนรับส่งข้อมูล
    permission_classes = [IsAdminRoleOrReadOnly]  # จำกัดสิทธิ์ให้แก้ไขได้เฉพาะ admin แต่อนุญาตให้คนอื่นอ่านได้
    filter_backends = [filters.SearchFilter]  # เปิดใช้งานระบบตัวกรองสำหรับการค้นหาข้อมูล
    search_fields = ['name']  # อนุญาตให้ค้นหาข้อมูลจากฟิลด์ name (ชื่อผู้กำกับ) ได้


class MovieViewSet(viewsets.ModelViewSet):  # สร้างชุด API สำหรับจัดการข้อมูลภาพยนตร์ (Movie)
    queryset = Movie.objects.select_related('director').all().order_by('id')  # ดึงภาพยนตร์จาก DB พร้อมกับ join ตัวผู้กำกับมาด้วย เพื่อประสิทธิภาพ และเรียงตาม ID
    serializer_class = MovieSerializer  # ผูกกับ MovieSerializer
    permission_classes = [IsAdminRoleOrReadOnly]  # สิทธิ์เข้าถึงแบบดูได้ทุกคน แต่แก้ไขได้เฉพาะ Admin
    filter_backends = [filters.SearchFilter]  # เปิดระบบค้นหา
    search_fields = ['title']  # ค้นหาได้จากฟิลด์ title (ชื่อเรื่อง)

    def get_queryset(self):  # เขียนฟังก์ชันทับเพื่อปรับแต่งการดึงข้อมูลเพิ่มตาม query params (URL ?...)
        qs = Movie.objects.select_related('director').all().order_by('id')  # ดึงภาพยนตร์พร้อม join ผู้กำกับ
        director_id = self.request.query_params.get('director')  # เช็คว่ามีค่า ?director=... ส่งมาใน URL ด้วยไหม
        if director_id:  # ถ้ามีค่าส่งมาด้วย
            qs = qs.filter(director_id=director_id)  # กรองเอาเฉพาะข้อมูลหนังที่กำกับโดยผู้กำกับที่มี ID ตามที่ส่งมา
        return qs  # ส่งคืนข้อมูลหนังที่ฟิลเตอร์เรียบร้อยแล้วไปแสดงผล

    def list(self, request, *args, **kwargs):  # ฟังก์ชันที่ใช้ดึงรายการข้อมูลทั้งหมดกลับไป (GET /movies/)
        try:
            return super().list(request, *args, **kwargs)  # ทำงานปกติตามที่ ModelViewSet เตรียมไว้ให้
        except Exception as e:  # หากเจอข้อผิดพลาดหรือ error ระหว่างทำงาน
            traceback.print_exc()  # พิมพ์รายละเอียด traceback ลง console/log ช่วยในการ debug
            raise  # โยน error กลับขึ้นไปเพื่อให้ DRF จัดการต่อ (หน้าบ้านจะเห็น error status 500)


class DVDViewSet(viewsets.ModelViewSet):  # สร้างชุด API สำหรับจัดการข้อมูล DVD สินค้า
    queryset = DVD.objects.all()  # ดึงข้อมูล DVD พื้นฐานทั้งหมด
    serializer_class = DVDSerializer  # ผูกกับ DVDSerializer
    permission_classes = [IsAdminRoleOrReadOnly]  # ให้เฉพาะแอดมินพิ่มหรือแก้ได้, คนอื่นแค่ดู
    filter_backends = [filters.SearchFilter]  # เปิดระบบค้นหา
    search_fields = ['movie__title']  # ผูกกับชื่อเรื่องหนัง ให้ค้นหาจากชื่อหนังข้ามความสัมพันธ์ได้

    def get_queryset(self):  # ปรับแต่ง Queryset ตอนเรียกดู
        qs = DVD.objects.select_related('movie').all().order_by('id')  # ดึงข้อมูล DVD พร้อม join ตารางหนัง
        movie_id = self.request.query_params.get('movie')  # ตรวจจับว่ามีการหาข้อมูลด้วย query parameter ของ ?movie=... หรือไม่
        if movie_id:  # ถ้าค้นหาด้วย id หนัง
            qs = qs.filter(movie_id=movie_id)  # กรองและแสดงเฉพาะแผ่น DVD ของหนังเรื่องนั้น
        return qs  # คืนค่ารายการ DVD


class OrderViewSet(viewsets.ModelViewSet):  # ชุด API สำหรับสั่งซื้อสินค้า และดูประวัติของตัวเอง (Order)
    permission_classes = [IsAuthenticated]  # บังคับว่าต้อง Login แล้วถึงใช้ API ชุดนี้ได้
    http_method_names = ['get', 'post', 'head', 'options']  # อนุญาตให้ใช้เฉพาะ GET และ POST เท่านั้น (ไม่อนุญาตให้แก้หรือลบคำสั่งซื้อที่เสร็จไปแล้ว)

    def get_queryset(self):  # จำกัดว่าจะให้ดึงข้อมูลอะไรมาดูได้บ้าง (ตอน GET)
        return (
            Order.objects
            .filter(user=self.request.user)  # กรองให้เห็นเฉพาะออเดอร์ของ user ปัจจุบันที่กำลังล็อกอินอยู่เท่านั้น (ไม่เห็นของคนอื่น)
            .prefetch_related('items')  # Join ดึงรายการสินค้าทั้งหมดข้างใน order ไว้ล่วงหน้า
            .order_by('-created_at')  # จัดเรียงโดยแสดงอันล่าสุดขึ้นก่อน
        )

    def get_serializer_class(self):  # เลือกใช้ Serializer ให้ตรงกับ Action
        if self.action == 'create':  # ถ้ากำลังทำ POST สร้างออเดอร์ใหม่
            return OrderCreateSerializer  # ใช้ Serializer เฉพาะที่มี logic ตรวจเช็คสต๊อกของสินค้า
        return OrderSerializer  # ถ้าไม่ได้สร้างใหม่ ก็ใช้ตัวปกติสำหรับดึงข้อมูลโชว์ธรรมดา

    def create(self, request, *args, **kwargs):  # ควบคุมตอนรับคำสั่งซื้อ (เมื่อมี POST เข้ามา)  
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})  # เอาข้อมูลเข้า Serializer และระบุ context เพื่อส่งเข้าถึง user ปัจจุบัน
        serializer.is_valid(raise_exception=True)  # ตรวจสอบว่าสินค้ามีสต๊อกพอไหม ถ้าผิดพลาดจะโยน error และรีเทิร์น 400 ย้อนกลับทันที
        result = serializer.save()  # บันทึกจริงๆ โดยจะรีเทิร์น dict ผลลัพธ์กลับมา
        data = OrderSerializer(result['order']).data  # ดึงเอาตัวออเดอร์ที่ถูกบันทึกลงฐานข้อมูลแล้วมาแปลงเป็น dict ของดิกขนาดย่อ
        data['discount_applied'] = result['discount_applied']  # สรุปค่าตัวแปรว่าลดราคาไหมและใส่เข้าไปใน payload ตอบกลับ
        data['original_total'] = str(result['original_total'])  # แปะราคาก่อนลด (แปลงเป็น string ป้องกันตัวเลขทศนิยมเพี้ยน)
        data['final_total'] = str(result['final_total'])  # แปะราคาที่หักส่วนลดแล้วลงไป
        return Response(data, status=status.HTTP_201_CREATED)  # ตอบกลับไปหา frontend พร้อมด้วยสถานะว่าสร้างสำเร็จ 201
