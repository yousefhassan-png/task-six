# -*- coding: utf-8 -*-
import sqlite3

# الاتصال بقاعدة البيانات
اتصال = sqlite3.connect("store.db")
مؤشر = اتصال.cursor()
print("الاتصال ناجح!")

# حذف الجداول القديمة لتشغيل البرنامج أكثر من مرة دون تكرار البيانات
مؤشر.execute("DROP TABLE IF EXISTS sales")
مؤشر.execute("DROP TABLE IF EXISTS products")

# إنشاء جدول المنتجات
مؤشر.execute("""
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT,
        category TEXT,
        price REAL
    )
""")

# إضافة المنتجات
المنتجات = [
    (1, "Laptop", "electronics", 650.0),
    (2, "Mouse", "electronics", 18.5),
    (3, "Keyboard", "electronics", 42.0),
    (4, "Headphones", "electronics", 85.0),
    (5, "Monitor", "electronics", 180.0),
    (6, "Desk", "furniture", 220.0),
    (7, "Chair", "furniture", 95.0),
    (8, "Notebook", "stationery", 3.5),
    (9, "Pen Set", "stationery", 7.0),
    (10, "Printer", "electronics", 140.0),
]
مؤشر.executemany(
    "INSERT INTO products (product_id, product_name, category, price) VALUES (?, ?, ?, ?)",
    المنتجات
)
اتصال.commit()

# إنشاء جدول المبيعات
مؤشر.execute("""
    CREATE TABLE sales (
        sale_id INTEGER PRIMARY KEY,
        product_id INTEGER,
        quantity INTEGER,
        sale_date TEXT,
        city TEXT
    )
""")

# إضافة 30 عملية بيع في مدن وتواريخ ومنتجات مختلفة
المبيعات = [
    (1, 1, 2, "2026-09-01", "عمان"),
    (2, 2, 8, "2026-09-01", "الزرقاء"),
    (3, 3, 5, "2026-09-02", "إربد"),
    (4, 4, 3, "2026-09-02", "عمان"),
    (5, 5, 2, "2026-09-03", "الزرقاء"),
    (6, 6, 1, "2026-09-03", "عمان"),
    (7, 7, 4, "2026-09-04", "إربد"),
    (8, 8, 20, "2026-09-04", "الزرقاء"),
    (9, 9, 15, "2026-09-05", "عمان"),
    (10, 10, 2, "2026-09-05", "إربد"),
    (11, 1, 1, "2026-09-06", "الزرقاء"),
    (12, 2, 10, "2026-09-06", "عمان"),
    (13, 3, 6, "2026-09-07", "إربد"),
    (14, 4, 4, "2026-09-07", "الزرقاء"),
    (15, 5, 1, "2026-09-08", "عمان"),
    (16, 6, 2, "2026-09-08", "إربد"),
    (17, 7, 3, "2026-09-09", "الزرقاء"),
    (18, 8, 25, "2026-09-09", "عمان"),
    (19, 9, 12, "2026-09-10", "إربد"),
    (20, 10, 1, "2026-09-10", "الزرقاء"),
    (21, 1, 3, "2026-09-11", "عمان"),
    (22, 2, 7, "2026-09-11", "إربد"),
    (23, 3, 4, "2026-09-12", "الزرقاء"),
    (24, 4, 2, "2026-09-12", "عمان"),
    (25, 5, 3, "2026-09-13", "إربد"),
    (26, 6, 1, "2026-09-13", "الزرقاء"),
    (27, 7, 5, "2026-09-14", "عمان"),
    (28, 8, 18, "2026-09-14", "إربد"),
    (29, 9, 10, "2026-09-15", "الزرقاء"),
    (30, 10, 2, "2026-09-15", "عمان"),
]
مؤشر.executemany(
    "INSERT INTO sales (sale_id, product_id, quantity, sale_date, city) VALUES (?, ?, ?, ?, ?)",
    المبيعات
)
اتصال.commit()

# الجزء 3: استعلامات SELECT و WHERE و ORDER BY
print("\nالجزء 3: استخراج البيانات")

print("\n1) جميع المنتجات:")
مؤشر.execute("SELECT * FROM products")
print(مؤشر.fetchall())

print("\n2) أسماء وأسعار المنتجات التي يزيد سعرها عن 50:")
مؤشر.execute("SELECT product_name, price FROM products WHERE price > 50")
print(مؤشر.fetchall())

print("\n3) مبيعات مدينة عمان مرتبة حسب التاريخ:")
مؤشر.execute("SELECT * FROM sales WHERE city = 'عمان' ORDER BY sale_date ASC")
print(مؤشر.fetchall())

print("\n4) منتجات electronics التي يقل سعرها عن 100:")
مؤشر.execute("""
    SELECT * FROM products
    WHERE category = 'electronics' AND price < 100
""")
print(مؤشر.fetchall())

print("\n5) أعلى خمس عمليات بيع حسب الكمية:")
مؤشر.execute("SELECT * FROM sales ORDER BY quantity DESC LIMIT 5")
print(مؤشر.fetchall())

# الجزء 4: التلخيص ودوال التجميع
print("\nالجزء 4: التلخيص")

print("\n1) إجمالي الكمية المباعة لكل منتج:")
مؤشر.execute("""
    SELECT p.product_name, SUM(s.quantity)
    FROM sales AS s
    JOIN products AS p ON s.product_id = p.product_id
    GROUP BY s.product_id
    ORDER BY SUM(s.quantity) DESC
""")
print(مؤشر.fetchall())

print("\n2) عدد عمليات البيع بكل مدينة:")
مؤشر.execute("""
    SELECT city, COUNT(*)
    FROM sales
    GROUP BY city
""")
print(مؤشر.fetchall())

print("\n3) متوسط سعر المنتجات بكل فئة:")
مؤشر.execute("""
    SELECT category, AVG(price)
    FROM products
    GROUP BY category
""")
print(مؤشر.fetchall())

print("\n4) المدينة ذات أكبر عدد من عمليات البيع:")
مؤشر.execute("""
    SELECT city, COUNT(*) AS عدد_العمليات
    FROM sales
    GROUP BY city
    ORDER BY عدد_العمليات DESC
    LIMIT 1
""")
print(مؤشر.fetchall())

# الجزء 5: أسئلة الأعمال
print("\nالجزء 5: أسئلة الأعمال")

print("\n1) أكثر ثلاثة منتجات مبيعًا حسب إجمالي الكمية:")
مؤشر.execute("""
    SELECT p.product_name, SUM(s.quantity) AS إجمالي_الكمية
    FROM products AS p
    JOIN sales AS s ON p.product_id = s.product_id
    GROUP BY p.product_id
    ORDER BY إجمالي_الكمية DESC
    LIMIT 3
""")
print(مؤشر.fetchall())

print("\n2) إجمالي الإيراد لكل منتج:")
مؤشر.execute("""
    SELECT p.product_name, SUM(s.quantity * p.price) AS إجمالي_الإيراد
    FROM products AS p
    JOIN sales AS s ON p.product_id = s.product_id
    GROUP BY p.product_id
    ORDER BY إجمالي_الإيراد DESC
""")
print(مؤشر.fetchall())

print("\n3) المدينة الأعلى بإجمالي الكمية المباعة:")
مؤشر.execute("""
    SELECT city, SUM(quantity) AS إجمالي_الكمية
    FROM sales
    GROUP BY city
    ORDER BY إجمالي_الكمية DESC
    LIMIT 1
""")
print(مؤشر.fetchall())

print("\n4) الفئة الأكثر مبيعًا من ناحية عدد العمليات:")
مؤشر.execute("""
    SELECT p.category, COUNT(*) AS عدد_العمليات
    FROM products AS p
    JOIN sales AS s ON p.product_id = s.product_id
    GROUP BY p.category
    ORDER BY عدد_العمليات DESC
    LIMIT 1
""")
print(مؤشر.fetchall())

print("\n5) متوسط الكمية في عملية البيع:")
مؤشر.execute("SELECT AVG(quantity) FROM sales")
print(مؤشر.fetchall())

# ملخص النتائج
print("\\nملخص للمدير:")
print("تُظهر البيانات أن القرطاسية حققت كميات مرتفعة بسبب بيع الدفاتر والأقلام بكميات كبيرة.")
print("كما تختلف الإيرادات حسب سعر المنتج والكمية المباعة، لذلك لا تعني الكمية الأعلى بالضرورة الإيراد الأعلى.")
print("تساعد مقارنة المدن والفئات على فهم توزيع الطلب وتخطيط المخزون.")

اتصال.close()
print("\nتم حفظ البيانات وإغلاق الاتصال.")
