import json
from datetime import datetime

from sqlalchemy.orm import Session

from backend.app.core.config import get_settings
from backend.app.core.security import get_password_hash
from backend.app.models import AdminUser, HeroBanner, NewsArticle, Product, SiteSection


settings = get_settings()


DEFAULT_SECTIONS = [
    {
        "key": "core_selling",
        "name": "首页核心卖点",
        "title": "云海梯田孕育的原生态红米",
        "subtitle": "四季山泉润养，延续哈尼族农耕智慧",
        "body": "用一块内容区展示梯田地貌、种植方式、生态优势和口感价值。后台可继续增删文字、图片或补充 JSON 数据。",
        "image_url": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1200&q=80",
        "extra_json": json.dumps({"tags": ["高海拔梯田", "山泉灌溉", "传统手作"], "stats": [{"label": "海拔", "value": "1400m+"}, {"label": "种植周期", "value": "120天"}]}, ensure_ascii=False),
        "sort_order": 1,
        "is_active": True,
    },
    {
        "key": "brand_story",
        "name": "品牌故事",
        "title": "从哈尼村寨到城市餐桌的文化传递",
        "subtitle": "文化展示站可通过这一板块承接品牌故事与匠心表达",
        "body": "这一板块建议放产地文化、族群记忆、节庆仪式和稻作传承。当前先放示例文案，后续可在后台实时修改。",
        "image_url": "https://images.unsplash.com/photo-1464226184884-fa280b87c399?auto=format&fit=crop&w=1200&q=80",
        "extra_json": json.dumps({"tags": ["哈尼文化", "稻作文明", "节庆习俗"]}, ensure_ascii=False),
        "sort_order": 2,
        "is_active": True,
    },
    {
        "key": "revitalization",
        "name": "产业振兴",
        "title": "以产业化运营带动山地农业振兴",
        "subtitle": "展示合作社、种植基地、电商渠道和文旅融合成果",
        "body": "适合放入产业链、合作农户、品牌渠道、研学旅游等信息，强化文化展示站与产业价值的连接。",
        "image_url": "https://images.unsplash.com/photo-1523741543316-beb7fc7023d8?auto=format&fit=crop&w=1200&q=80",
        "extra_json": json.dumps({"stats": [{"label": "联动农户", "value": "300+"}, {"label": "示范梯田", "value": "12片"}]}, ensure_ascii=False),
        "sort_order": 3,
        "is_active": True,
    },
    {
        "key": "product_intro",
        "name": "产品区导语",
        "title": "红米产品矩阵",
        "subtitle": "用不同规格、场景和口感表达品牌层次",
        "body": "此处内容控制产品展示区的标题和导语。",
        "image_url": None,
        "extra_json": None,
        "sort_order": 10,
        "is_active": True,
    },
    {
        "key": "news_intro",
        "name": "动态区导语",
        "title": "企业动态与梯田新讯",
        "subtitle": "发布品牌活动、助农项目、产地纪实等信息",
        "body": "此处内容控制新闻动态板块的标题和导语。",
        "image_url": None,
        "extra_json": None,
        "sort_order": 11,
        "is_active": True,
    },
]

DEFAULT_BANNERS = [
    {
        "title": "哈尼梯田红米文化展示网站",
        "subtitle": "用数字化方式重构山地农耕文化的观看体验",
        "description": "轮播图内容、按钮、排序均可在后台调整。这里先提供一组示例数据，确保前后端联调后有真实展示效果。",
        "image_url": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1600&q=80",
        "cta_text": "查看产品",
        "cta_link": "#products",
        "sort_order": 1,
        "is_active": True,
    },
    {
        "title": "山水之间的红米生长季",
        "subtitle": "云雾、梯田、村寨与稻穗共同构成文化景观",
        "description": "第二张轮播图可用于承载品牌故事、宣传语或活动专题。",
        "image_url": "https://images.unsplash.com/photo-1472396961693-142e6e269027?auto=format&fit=crop&w=1600&q=80",
        "cta_text": "了解故事",
        "cta_link": "#story",
        "sort_order": 2,
        "is_active": True,
    },
]

DEFAULT_PRODUCTS = [
    {
        "name": "梯田生态红米礼盒",
        "subtitle": "适合品牌礼赠与文化展销场景",
        "description": "展示礼盒规格、风味口感、产地优势和食用建议。参数字段使用 JSON 文本，便于后台维护。",
        "cover_image": "https://images.unsplash.com/photo-1516684669134-de6f7c473a2a?auto=format&fit=crop&w=900&q=80",
        "specs_json": json.dumps({"净含量": "2kg", "口感": "糯香软弹", "适用场景": "礼赠/团购"}, ensure_ascii=False),
        "sort_order": 1,
        "is_active": True,
    },
    {
        "name": "农家日常装红米",
        "subtitle": "主打家庭日常食用与健康粗粮搭配",
        "description": "可承载粒型、营养特征、烹饪建议等信息。",
        "cover_image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=900&q=80",
        "specs_json": json.dumps({"净含量": "5kg", "建议搭配": "与白米混煮", "储存方式": "阴凉干燥"}, ensure_ascii=False),
        "sort_order": 2,
        "is_active": True,
    },
]

DEFAULT_NEWS = [
    {
        "title": "哈尼梯田红米春耕文化季启动",
        "summary": "可在后台发布企业活动、品牌报道或节庆资讯，首页将自动同步。",
        "content": "本示例新闻用于展示前端新闻卡片与后台编辑流程，后续可根据真实项目替换。",
        "cover_image": "https://images.unsplash.com/photo-1464226184884-fa280b87c399?auto=format&fit=crop&w=900&q=80",
        "published_at": datetime.utcnow(),
        "sort_order": 1,
        "is_active": True,
    },
    {
        "title": "合作社推进梯田红米标准化加工",
        "summary": "结合产业振兴和农产品品牌化路径，补充企业动态内容。",
        "content": "这里可以发布加工升级、渠道合作、助农行动等企业新闻。",
        "cover_image": "https://images.unsplash.com/photo-1499529112087-3cb3b73cec95?auto=format&fit=crop&w=900&q=80",
        "published_at": datetime.utcnow(),
        "sort_order": 2,
        "is_active": True,
    },
]


def seed_admin(db: Session) -> None:
    """Create or repair the single admin account required by the management console."""
    admin = db.query(AdminUser).filter(AdminUser.username == settings.admin_username).first()
    if admin:
        admin.password_hash = get_password_hash(settings.admin_password)
    else:
        db.add(
            AdminUser(
                username=settings.admin_username,
                password_hash=get_password_hash(settings.admin_password),
            )
        )
    db.commit()


def seed_content(db: Session) -> None:
    """Seed demo content only when the site is still empty, preserving later edits."""
    if not db.query(HeroBanner).first():
        db.add_all(HeroBanner(**item) for item in DEFAULT_BANNERS)
    if not db.query(SiteSection).first():
        db.add_all(SiteSection(**item) for item in DEFAULT_SECTIONS)
    if not db.query(Product).first():
        db.add_all(Product(**item) for item in DEFAULT_PRODUCTS)
    if not db.query(NewsArticle).first():
        db.add_all(NewsArticle(**item) for item in DEFAULT_NEWS)
    db.commit()
