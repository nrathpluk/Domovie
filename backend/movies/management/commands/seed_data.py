import os
import shutil
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files import File
from movies.models import Director, Movie
from store.models import Product


STATIC_IMAGES = os.path.join(
    os.path.dirname(__file__), '..', '..', '..', 'movies', 'static', 'movies', 'images'
)


def copy_image(model_instance, field_name, src_path):
    if not os.path.exists(src_path):
        return
    with open(src_path, 'rb') as f:
        filename = os.path.basename(src_path)
        getattr(model_instance, field_name).save(filename, File(f), save=True)


class Command(BaseCommand):
    help = 'Seed database with sample directors, movies, and users'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # --- Users ---
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@domovie.com', 'admin1234')
            self.stdout.write('  Created admin user')

        if not User.objects.filter(username='user').exists():
            User.objects.create_user('user', 'user@domovie.com', 'user1234')
            self.stdout.write('  Created regular user')

        # --- Directors ---
        directors_data = [
            {
                'name': 'Christopher Nolan',
                'bio': (
                    'คริสโตเฟอร์ โนแลน (Christopher Nolan) เกิดเมื่อวันที่ 30 กรกฎาคม ค.ศ. 1970 '
                    'ที่กรุงลอนดอน ประเทศอังกฤษ เป็นผู้กำกับ นักเขียนบท และโปรดิวเซอร์ภาพยนตร์ชื่อดังระดับโลก '
                    'มีสัญชาติอังกฤษ–อเมริกัน เขาเริ่มสนใจการทำหนังตั้งแต่วัยเด็ก และศึกษาในสาขาวรรณคดีอังกฤษ '
                    'ที่ University College London (UCL) ซึ่งเป็นช่วงที่เขาเริ่มทดลองสร้างภาพยนตร์สั้น '
                    'ด้วยงบประมาณจำกัด ผลงานที่ทำให้เขาเป็นที่รู้จักในวงกว้างคือ Memento (2000) '
                    'ซึ่งโดดเด่นด้านการเล่าเรื่องแบบย้อนเวลา'
                ),
                'nationality': 'British-American',
                'birth_year': 1970,
                'image_path': os.path.join(STATIC_IMAGES, 'Movie', 'Inception', 'Christopher_Nolan.jpg'),
            },
            {
                'name': 'The Wachowskis',
                'bio': (
                    'Lana และ Lilly Wachowski คือคู่ผู้กำกับชาวอเมริกัน ที่สร้างปรากฏการณ์ '
                    'ด้วยภาพยนตร์ The Matrix (1999) ผสมผสานปรัชญา, karate และ CGI '
                    'อย่างสร้างสรรค์จนกลายเป็นตำนาน'
                ),
                'nationality': 'American',
                'birth_year': 1965,
                'image_path': None,
            },
            {
                'name': 'Stanley Kubrick',
                'bio': (
                    'สแตนลีย์ คูบริก (Stanley Kubrick) เป็นผู้กำกับภาพยนตร์ชาวอเมริกัน '
                    'ผู้ถูกยกย่องว่าเป็นหนึ่งในผู้กำกับที่ยิ่งใหญ่ที่สุดตลอดกาล '
                    'ผลงานเด่น ได้แก่ 2001: A Space Odyssey (1968) และ The Shining (1980)'
                ),
                'nationality': 'American',
                'birth_year': 1928,
                'image_path': None,
            },
            {
                'name': 'James Wan',
                'bio': (
                    'เจมส์ วาน (James Wan) ผู้กำกับชาวออสเตรเลียเชื้อสายมาเลเซีย '
                    'โด่งดังจากซีรีส์ Saw และ The Conjuring Universe '
                    'ถือเป็นราชาแห่งหนังสยองขวัญยุคใหม่'
                ),
                'nationality': 'Australian',
                'birth_year': 1977,
                'image_path': None,
            },
            {
                'name': 'Denis Villeneuve',
                'bio': (
                    'เดอนีส์ วิลเนิฟ (Denis Villeneuve) ผู้กำกับชาวแคนาดา '
                    'เจ้าของผลงาน Arrival (2016), Blade Runner 2049 (2017) และ Dune (2021) '
                    'ขึ้นชื่อในด้านภาพสวยงามและเรื่องราวที่ลึกซึ้ง'
                ),
                'nationality': 'Canadian',
                'birth_year': 1967,
                'image_path': None,
            },
        ]

        director_objects = {}
        for d in directors_data:
            obj, created = Director.objects.get_or_create(name=d['name'], defaults={
                'bio': d['bio'],
                'nationality': d['nationality'],
                'birth_year': d['birth_year'],
            })
            if created:
                self.stdout.write(f'  Created director: {obj.name}')
                if d['image_path']:
                    copy_image(obj, 'profile_image', d['image_path'])
            director_objects[d['name']] = obj

        # --- Movies ---
        movies_data = [
            {
                'title': 'Inception',
                'synopsis': 'ความฝันซ้อนความฝัน ภารกิจจารกรรมความคิดที่สุดล้ำเหนือจินตนาการ โดมินิก คอบบ์ และทีมงานต้องฝังความคิดลงในจิตใต้สำนึกของเป้าหมาย',
                'release_year': 2010,
                'genre': 'scifi',
                'director': 'Christopher Nolan',
                'image_path': os.path.join(STATIC_IMAGES, 'Movie', 'Inception', 'INCEPTION.jpg'),
            },
            {
                'title': 'Interstellar',
                'synopsis': 'การเดินทางข้ามกาลเวลาและมิติเพื่อหาบ้านใหม่ให้มนุษยชาติ เมื่อโลกกำลังจะสิ้นสุด นักบินอวกาศต้องออกเดินทางผ่านรูหนอนในอวกาศ',
                'release_year': 2014,
                'genre': 'scifi',
                'director': 'Christopher Nolan',
                'image_path': os.path.join(STATIC_IMAGES, 'Movie', 'Interstalla', 'INTERSTALLA.jpg'),
            },
            {
                'title': 'The Matrix',
                'synopsis': 'ตื่นจากโลกเสมือนจริง และเข้าสู่ความจริงที่ถูกซ่อนไว้โดยเครื่องจักร โทมัส แอนเดอร์สัน ค้นพบว่าโลกที่เขาอาศัยอยู่ไม่ใช่ความจริง',
                'release_year': 1999,
                'genre': 'scifi',
                'director': 'The Wachowskis',
                'image_path': os.path.join(STATIC_IMAGES, 'Movie', 'The matric', 'the matric.jpg'),
            },
            {
                'title': 'Blade Runner 2049',
                'synopsis': 'การค้นพบความลับที่ถูกฝังไว้นานอาจนำไปสู่หายนะของสังคมที่เหลืออยู่ เจ้าหน้าที่ K ค้นพบสิ่งที่อาจทำลายระเบียบที่มีอยู่ทั้งหมด',
                'release_year': 2017,
                'genre': 'scifi',
                'director': 'Denis Villeneuve',
                'image_path': os.path.join(STATIC_IMAGES, 'Movie', 'Blade Runner 2049', 'DVD_BLN.jpg'),
            },
            {
                'title': 'Arrival',
                'synopsis': 'เมื่อยานอวกาศลึกลับลงจอดทั่วโลก นักภาษาศาสตร์ต้องหาทางสื่อสารกับมนุษย์ต่างดาวก่อนสงครามจะเริ่มต้น',
                'release_year': 2016,
                'genre': 'scifi',
                'director': 'Denis Villeneuve',
                'image_path': os.path.join(STATIC_IMAGES, 'Movie', 'Arrival', 'Arrival.jpg'),
            },
            {
                'title': 'A Quiet Place',
                'synopsis': 'ถ้าพวกมันได้ยิน... พวกมันจะออกล่า ครอบครัวหนึ่งต้องใช้ชีวิตในความเงียบเพื่อความอยู่รอดจากสัตว์ประหลาดที่มองด้วยเสียง',
                'release_year': 2018,
                'genre': 'horror',
                'director': 'James Wan',
                'image_path': os.path.join(STATIC_IMAGES, 'Movie', 'A Quiet Place', 'A Quiet Place.jpg'),
            },
            {
                'title': 'The Shining',
                'synopsis': 'ความสยองขวัญระดับตำนานในโรงแรมลึกลับกลางหุบเขาหิมะ แจ็ค ทอร์แรนซ์ค่อยๆ สูญเสียสติไปกับอำนาจลึกลับของโรงแรม Overlook',
                'release_year': 1980,
                'genre': 'horror',
                'director': 'Stanley Kubrick',
                'image_path': os.path.join(STATIC_IMAGES, 'Movie', 'TheShining', 'TheShining.jpg'),
            },
            {
                'title': 'Scream',
                'synopsis': 'ฆาตกรสวมหน้ากากปีศาจที่ทำให้เหยื่อแฮตต่อกันด้วยคำถามเกี่ยวกับหนังสยองขวัญ ซิดนีย์ ต้องเอาตัวรอดจากฆาตกรลึกลับ',
                'release_year': 1996,
                'genre': 'horror',
                'director': 'James Wan',
                'image_path': os.path.join(STATIC_IMAGES, 'Movie', 'Scream', 'scream.jpg'),
            },
            {
                'title': 'The Conjuring',
                'synopsis': 'คู่สามีภรรยานักปราบผีต้องเผชิญกับคดีที่น่าสะพรึงกลัวที่สุดในชีวิต เมื่อครอบครัวหนึ่งถูกสิ่งชั่วร้ายหลอกหลอน',
                'release_year': 2013,
                'genre': 'horror',
                'director': 'James Wan',
                'image_path': os.path.join(STATIC_IMAGES, 'Movie', 'The Conjuring', 'The Conjuring.jpg'),
            },
            {
                'title': 'The Thing',
                'synopsis': 'ทีมนักวิทยาศาสตร์ในแอนตาร์กติกาต้องเผชิญกับสิ่งมีชีวิตต่างดาวที่เลียนแบบมนุษย์ได้ ความหวาดระแวงแพร่กระจายในกลุ่ม',
                'release_year': 1982,
                'genre': 'horror',
                'director': 'Stanley Kubrick',
                'image_path': os.path.join(STATIC_IMAGES, 'Movie', 'The Thing', 'The Thing.jpg'),
            },
        ]

        for m in movies_data:
            director = director_objects.get(m['director'])
            obj, created = Movie.objects.get_or_create(title=m['title'], defaults={
                'synopsis': m['synopsis'],
                'release_year': m['release_year'],
                'genre': m['genre'],
                'director': director,
            })
            if created:
                self.stdout.write(f'  Created movie: {obj.title}')
                if m['image_path']:
                    copy_image(obj, 'poster_image', m['image_path'])

        # --- Products ---
        products_data = [
            {
                'name': 'Inception Blu-ray',
                'description': 'แผ่น Blu-ray คุณภาพสูง พร้อม behind-the-scenes พิเศษ',
                'price': '300.00',
                'stock': 10,
                'image_path': os.path.join(STATIC_IMAGES, 'Item for sell', 'Interstalla_forsale.jpg'),
            },
            {
                'name': 'The Shining DVD',
                'description': 'ฉบับ Director\'s Cut พร้อมคำบรรยายภาษาไทย',
                'price': '200.00',
                'stock': 10,
                'image_path': os.path.join(STATIC_IMAGES, 'Item for sell', 'TheShining.jpg'),
            },
            {
                'name': 'The Matrix DVD',
                'description': 'ภาพยนตร์ไซ-ไฟคลาสสิก พร้อม special features',
                'price': '200.00',
                'stock': 10,
                'image_path': os.path.join(STATIC_IMAGES, 'Item for sell', 'The_matrixforsael.jpg'),
            },
            {
                'name': 'Scream Collector\'s Edition',
                'description': 'Collector\'s Edition พร้อมโปสการ์ดและสติ๊กเกอร์',
                'price': '150.00',
                'stock': 10,
                'image_path': os.path.join(STATIC_IMAGES, 'Item for sell', 'Scream.jpg'),
            },
        ]

        for p in products_data:
            obj, created = Product.objects.get_or_create(name=p['name'], defaults={
                'description': p['description'],
                'price': p['price'],
                'stock': p['stock'],
            })
            if created:
                self.stdout.write(f'  Created product: {obj.name}')
                if p['image_path']:
                    copy_image(obj, 'image', p['image_path'])

        self.stdout.write(self.style.SUCCESS('Seed data complete!'))
        self.stdout.write('  admin / admin1234')
        self.stdout.write('  user  / user1234')
