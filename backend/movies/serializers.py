from decimal import Decimal  # นำเข้า Decimal สำหรับคำนวณราคาแบบ precise (หลีกเลี่ยง floating point error)

from rest_framework import serializers  # นำเข้า base class ของ DRF serializers
from django.db import transaction  # นำเข้า transaction สำหรับ atomic operation

from .models import Director, Movie, DVD, Order, OrderItem  # นำเข้า models ทั้งหมดที่ต้องการ


class DirectorSerializer(serializers.ModelSerializer):  # serializer แปลง Director model ↔ JSON
    class Meta:  # กำหนด config ของ serializer
        model = Director  # ผูกกับ model Director
        fields = ['id', 'name', 'bio', 'birth_date', 'image_url']  # fields ที่จะ expose ใน API


class MovieSerializer(serializers.ModelSerializer):  # serializer แปลง Movie model ↔ JSON
    director_name = serializers.CharField(source='director.name', read_only=True)  # field พิเศษ: ดึงชื่อผู้กำกับจาก FK — read_only ไม่รับ input

    class Meta:  # กำหนด config
        model = Movie  # ผูกกับ model Movie
        fields = ['id', 'title', 'synopsis', 'release_date', 'director', 'director_name', 'poster_url']  # director=FK id, director_name=ชื่อจริง


class DVDSerializer(serializers.ModelSerializer):  # serializer แปลง DVD model ↔ JSON
    movie_title = serializers.CharField(source='movie.title', read_only=True)  # field พิเศษ: ดึงชื่อหนังจาก FK — read_only

    class Meta:  # กำหนด config
        model = DVD  # ผูกกับ model DVD
        fields = ['id', 'movie', 'movie_title', 'price', 'stock', 'cover_image']  # movie=FK id, movie_title=ชื่อจริง


class OrderItemSerializer(serializers.ModelSerializer):  # serializer แปลง OrderItem ↔ JSON (ใช้ใน response)
    class Meta:  # กำหนด config
        model = OrderItem  # ผูกกับ model OrderItem
        fields = ['id', 'dvd', 'quantity', 'price']  # fields ที่แสดงในรายการสินค้าของ order


class OrderSerializer(serializers.ModelSerializer):  # serializer แปลง Order ↔ JSON (ใช้ใน GET response)
    items = OrderItemSerializer(many=True, read_only=True)  # nested serializer: แสดงรายการสินค้าทั้งหมดในแต่ละ order

    class Meta:  # กำหนด config
        model = Order  # ผูกกับ model Order
        fields = ['id', 'user', 'total_price', 'status', 'created_at', 'items']  # fields ทั้งหมดของ order
        read_only_fields = ['user', 'total_price', 'created_at']  # fields เหล่านี้ set โดย server เท่านั้น ไม่รับ input


class _OrderItemInputSerializer(serializers.Serializer):  # serializer ย่อยสำหรับ validate แต่ละรายการสินค้าใน request body
    dvd = serializers.IntegerField()  # id ของ DVD ที่สั่ง
    quantity = serializers.IntegerField(min_value=1)  # จำนวนที่สั่ง ต้องมากกว่าหรือเท่ากับ 1


class OrderCreateSerializer(serializers.Serializer):  # serializer สำหรับ POST /orders/ — จัดการ business logic ทั้งหมด
    items = _OrderItemInputSerializer(many=True)  # รับ array ของ items ใน request body

    def validate_items(self, items):  # validate ว่า items ไม่ว่าง
        if not items:  # ถ้าไม่มีสินค้าเลย
            raise serializers.ValidationError("Order must have at least one item.")  # โยน error
        return items  # คืน items ที่ผ่าน validation

    def create(self, validated_data):  # ฟังก์ชันสร้าง order จริง — เรียกตอน serializer.save()
        user = self.context['request'].user  # ดึง user จาก request context (ผู้ที่ login อยู่)
        items_data = validated_data['items']  # ดึง array items จากข้อมูลที่ validate แล้ว

        with transaction.atomic():  # เปิด atomic block — ถ้า error ใดๆ ใน block → rollback ทุกอย่าง
            total = 0  # ตัวแปรสะสมราคารวมก่อนส่วนลด
            built_items = []  # list เก็บข้อมูล items ที่ตรวจ stock แล้ว

            for item_data in items_data:  # วน loop ตรวจสอบแต่ละ item
                try:
                    dvd = DVD.objects.select_for_update().get(id=item_data['dvd'])  # ดึง DVD พร้อม lock row (ป้องกัน race condition จาก concurrent orders)
                except DVD.DoesNotExist:  # ถ้าไม่เจอ DVD
                    raise serializers.ValidationError(
                        f"DVD with id {item_data['dvd']} does not exist."  # โยน error บอก id ที่หาไม่เจอ
                    )

                qty = item_data['quantity']  # จำนวนที่ต้องการสั่ง
                if dvd.stock < qty:  # ถ้า stock ไม่พอ
                    raise serializers.ValidationError(
                        f"Insufficient stock for '{dvd.movie.title}'. Available: {dvd.stock}"  # โยน error บอก stock ที่เหลือ
                    )

                dvd.stock -= qty  # หัก stock ตามจำนวนที่สั่ง
                dvd.save()  # บันทึก stock ใหม่ลง DB
                total += dvd.price * qty  # สะสมราคารวม
                built_items.append({'dvd': dvd, 'quantity': qty, 'price': dvd.price})  # เก็บข้อมูล item ที่ผ่านการตรวจแล้ว

            original_total = total  # เก็บราคาก่อนหักส่วนลด
            total_qty = sum(item['quantity'] for item in built_items)  # รวมจำนวน DVD ทั้งหมดในคำสั่งซื้อ
            discount_applied = total_qty >= 3  # ถ้า DVD รวม >= 3 ชิ้น → ได้รับส่วนลด 10%
            final_total = (original_total * Decimal('0.90')).quantize(Decimal('0.01')) if discount_applied else original_total  # คำนวณราคาสุดท้าย (หัก 10% ถ้าได้รับส่วนลด) แล้ว round 2 ทศนิยม

            order = Order.objects.create(user=user, total_price=final_total)  # สร้าง Order record ใน DB
            for item in built_items:  # วน loop สร้าง OrderItem แต่ละรายการ
                OrderItem.objects.create(order=order, **item)  # สร้าง OrderItem ผูกกับ Order

            return {  # คืน dict ผลลัพธ์ (ไม่ใช่แค่ order เพราะ view ต้องการข้อมูลส่วนลดด้วย)
                'order': order,  # Order object ที่สร้างแล้ว
                'discount_applied': discount_applied,  # bool บอกว่าได้รับส่วนลดหรือไม่
                'original_total': original_total,  # ราคาก่อนส่วนลด
                'final_total': final_total,  # ราคาสุดท้ายหลังส่วนลด
            }
