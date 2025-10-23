from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

MOCK_LISTINGS = [
    {
        "id": "10000000-0000-0000-0000-000000000001",
        "title": "Badminton Racket",
        "price": 2000000,
        "condition": "BRAND_NEW",
        "location": "East Jakarta",
        "description": "Raket bulutangkis ringan dengan frame grafit dan pola string isometric untuk sweet spot yang lebih lebar. Pegangan anti-slip memberi kontrol maksimal saat netting dan drive cepat. Cocok untuk latihan harian maupun turnamen sekolah.",
        "image_url": "https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": "10000000-0000-0000-0000-000000000002",
        "title": "Baseball Bat",
        "price": 1000000,
        "condition": "USED",
        "location": "South Jakarta",
        "description": "Tongkat baseball aluminium berlapis anodized dengan keseimbangan mid-load untuk ayunan stabil. Permukaan masih mulus dan bebas penyok besar; hanya gores pemakaian wajar. Nyaman untuk sesi latihan atau liga komunitas.",
        "image_url": "https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": "10000000-0000-0000-0000-000000000003",
        "title": "Tennis Racket",
        "price": 2000000,
        "condition": "BRAND_NEW",
        "location": "Central Jakarta",
        "description": "Raket tenis grafit komposit dengan head 100 sq in dan pola string 16x19 untuk spin mudah. Bobot seimbang membuat ayunan ringan namun bertenaga. Datang dengan cover dan grip baru terpasang.",
        "image_url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": "10000000-0000-0000-0000-000000000004",
        "title": "Cycling Helmet",
        "price": 800000,
        "condition": "BRAND_NEW",
        "location": "West Jakarta",
        "description": "Helm sepeda aero dengan 18 ventilasi, sistem pengunci micro-dial, dan bantalan antibakteri. Shell in-mold menjaga bobot tetap ringan tanpa mengorbankan perlindungan. Sertifikasi keselamatan internasional.",
        "image_url": "https://images.unsplash.com/photo-1508606572321-901ea443707f?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": "10000000-0000-0000-0000-000000000007",
        "title": "Yoga Mat",
        "price": 280000,
        "condition": "BRAND_NEW",
        "location": "South Jakarta",
        "description": "Mat yoga TPE anti-slip dengan ketebalan 6 mm yang empuk untuk sendi. Permukaan dua sisi membuat pose stabil, mudah dibersihkan, dan dilengkapi strap agar praktis dibawa.",
        "image_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": "10000000-0000-0000-0000-000000000008",
        "title": "Boxing Gloves",
        "price": 650000,
        "condition": "USED",
        "location": "Central Jakarta",
        "description": "Sarung tinju 12 oz dengan bantalan multi-layer untuk pergelangan yang aman. Kulit sintetis masih rapi; hanya ada bekas training ringan. Cocok untuk bag work dan sparing santai.",
        "image_url": "https://images.unsplash.com/photo-1517438322307-e67111335449?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": "10000000-0000-0000-0000-000000000010",
        "title": "Golf Putter",
        "price": 1500000,
        "condition": "USED",
        "location": "South Jakarta",
        "description": "Putter milled face dengan alur halus untuk roll konsisten. Berat kepala sedikit forward untuk feel stabil. Ada sedikit gores pada sole, performa tetap prima di green cepat.",
        "image_url": "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": "10000000-0000-0000-0000-000000000011",
        "title": "Skateboard",
        "price": 700000,
        "condition": "BRAND_NEW",
        "location": "Central Jakarta",
        "description": "Deck maple 7-ply dengan truck aluminium dan roda 99A untuk street/park. Grip tape sudah terpasang rapi, bearing ABEC yang halus memudahkan ollie dan flip pertama Anda.",
        "image_url": "https://images.unsplash.com/photo-1508609349937-5ec4ae374ebf?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": "10000000-0000-0000-0000-000000000012",
        "title": "Surfboard",
        "price": 4500000,
        "condition": "USED",
        "location": "North Jakarta",
        "description": "Papan selancar funboard 7'0\" dengan volume ramah pemula. Rails sedikit tebal sehingga stabil saat take-off. Cat masih mulus; ada bekas wax wajar tanpa retak struktural.",
        "image_url": "https://images.unsplash.com/photo-1500048993953-d23a436266cf?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": "10000000-0000-0000-0000-000000000014",
        "title": "Hiking Backpack",
        "price": 950000,
        "condition": "USED",
        "location": "West Jakarta",
        "description": "Ransel hiking 35L dengan frame internal ringan, sabuk pinggang empuk, dan kompartemen hidrasi. Kain ripstop masih kuat; resleting lancar. Ideal untuk pendakian satu malam.",
        "image_url": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": "10000000-0000-0000-0000-000000000015",
        "title": "Table Tennis Paddle",
        "price": 320000,
        "condition": "BRAND_NEW",
        "location": "Central Jakarta",
        "description": "Bet tenis meja dengan karet tacky untuk kontrol spin dan handle flared yang nyaman. Cocok untuk pemain all-round yang ingin stabilitas blok dan putaran servis.",
        "image_url": "https://images.unsplash.com/photo-1546519638-68e109498ffc?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": "10000000-0000-0000-0000-000000000016",
        "title": "Volleyball",
        "price": 280000,
        "condition": "BRAND_NEW",
        "location": "South Jakarta",
        "description": "Bola voli dengan panel PU lembut dan jahitan presisi untuk first touch nyaman. Cocok untuk permainan indoor sekolah maupun pantai akhir pekan.",
        "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": "10000000-0000-0000-0000-000000000018",
        "title": "Smart Sports Watch",
        "price": 2300000,
        "condition": "BRAND_NEW",
        "location": "Central Jakarta",
        "description": "Jam olahraga dengan GPS, pelacakan denyut nadi optik, dan mode lari/sepeda/renang. Layar terang, baterai tahan hingga seminggu, dan sinkronisasi cepat ke ponsel.",
        "image_url": "https://images.unsplash.com/photo-1516822003754-cca485356ecb?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": "10000000-0000-0000-0000-000000000019",
        "title": "Kayak Paddle",
        "price": 750000,
        "condition": "USED",
        "location": "North Jakarta",
        "description": "Dayung kayak dua sisi berbahan serat kaca dengan sudut feather yang bisa diatur. Pegangan ergonomis meminimalkan lelah saat dayung panjang; ada gores ringan di blade.",
        "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=900&q=80",
    },
    {
        "id": "10000000-0000-0000-0000-000000000020",
        "title": "Tennis Balls (Pack of 3)",
        "price": 150000,
        "condition": "BRAND_NEW",
        "location": "East Jakarta",
        "description": "Set 3 bola tenis bertekanan dengan felt tahan lama. Pantulan konsisten membuat drill forehand/backhand terasa natural. Dikemas rapat agar kesegaran tahan lama.",
        "image_url": "https://images.unsplash.com/photo-1557180295-76eee20ae8aa?auto=format&fit=crop&w=900&q=80",
    },
]

def todays_pick(request):
	"""
	View to display Today's Pick listings in a grid
	"""
	listings = MOCK_LISTINGS
	context = {
		'listings': listings,
	}
	return render(request, 'marketplace_module/todays_pick.html', context)

def listing_detail(request, pk):
	"""
	View to display details of a single listing
	"""
	listing = next((item for item in MOCK_LISTINGS if item['id'] == str(pk)), None)
	if not listing:
		listing = MOCK_LISTINGS[0]
	context = {
		'listing': listing,
		'images': [{'image': {'url': listing['image_url']}}],
	}
	return render(request, 'marketplace_module/listing_detail.html', context)
