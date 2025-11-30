CREATE TABLE IF NOT EXISTS products (
    code        TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    price       NUMERIC(10, 2) NOT NULL,
    unit        TEXT DEFAULT 'шт'
);

INSERT INTO products (code, name, price, unit) VALUES
-- Видеокарты
('0000001', 'GeForce RTX 5060 Ti', 35000.00, 'шт'),
('0000002', 'GeForce RTX 4070 Super', 52000.00, 'шт'),
('0000003', 'Radeon RX 7800 XT', 48000.00, 'шт'),
('0000004', 'GeForce RTX 4090', 180000.00, 'шт'),
('0000005', 'GeForce RTX 4060', 25000.00, 'шт'),

-- Процессоры
('0000006', 'Intel Core i9-14900K', 28000.00, 'шт'),
('0000007', 'Intel Core i7-14700K', 19000.00, 'шт'),
('0000008', 'AMD Ryzen 9 7950X', 32000.00, 'шт'),
('0000009', 'AMD Ryzen 7 7800X3D', 26000.00, 'шт'),
('0000010', 'Intel Core i5-14600K', 14000.00, 'шт'),

-- Кулеры и СЖО
('0000011', 'Кулер DeepCool AG400', 1200.00, 'шт'),
('0000012', 'СЖО Corsair iCUE H150i ELITE', 9500.00, 'шт'),
('0000013', 'Кулер Noctua NH-D15', 8000.00, 'шт'),
('0000014', 'СЖО Lian Li Galahad II 360', 11000.00, 'шт'),
('0000015', 'Кулер Thermalright Phantom Spirit 120 SE', 3500.00, 'шт'),

-- Оперативная память
('0000016', 'ОЗУ Kingston FURY Beast DDR5 32 ГБ (2×16 ГБ) 6000 МГц', 8500.00, 'шт'),
('0000017', 'ОЗУ Corsair Vengeance RGB DDR5 32 ГБ 6400 МГц', 9200.00, 'шт'),
('0000018', 'ОЗУ G.Skill Trident Z5 RGB 64 ГБ (2×32 ГБ) 6000 МГц', 16000.00, 'шт'),

-- Материнские платы
('0000019', 'MSI MAG B760 TOMAHAWK WIFI DDR4', 15000.00, 'шт'),
('0000020', 'ASUS ROG Strix Z790-E Gaming WiFi', 32000.00, 'шт'),
('0000021', 'Gigabyte B650 AORUS Elite AX', 17000.00, 'шт'),

-- Блоки питания
('0000022', 'БП Corsair RM850e (850 Вт, 80+ Gold)', 8000.00, 'шт'),
('0000023', 'БП Seasonic FOCUS GX-1000 (1000 Вт, 80+ Gold)', 12000.00, 'шт'),
('0000024', 'БП DeepCool PF750 (750 Вт, 80+ Platinum)', 9500.00, 'шт'),

-- SSD и жесткие диски
('0000025', 'SSD Samsung 990 PRO 2 ТБ (M.2 NVMe)', 14000.00, 'шт'),
('0000026', 'SSD WD_BLACK SN850X 1 ТБ', 8500.00, 'шт'),
('0000027', 'HDD Seagate IronWolf 4 ТБ (NAS)', 6500.00, 'шт'),

-- Корпуса
('0000028', 'Корпус Lian Li Lancool 216', 9000.00, 'шт'),
('0000029', 'Корпус Fractal Design Meshify 2', 11000.00, 'шт'),
('0000030', 'Корпус Corsair 4000D Airflow', 7500.00, 'шт'),

-- Периферия
('0000031', 'Мышь Logitech G Pro X Superlight 2', 8000.00, 'шт'),
('0000032', 'Клавиатура Razer BlackWidow V4 Pro', 12000.00, 'шт'),
('0000033', 'Монитор ASUS ROG Swift PG279QM (27", 240 Гц)', 65000.00, 'шт'),

-- Прочее
('0000034', 'Термопаста Arctic MX-6 (4 г)', 600.00, 'шт'),
('0000035', 'Комплект вентиляторов Noctua NF-A12x25 (3 шт)', 3200.00, 'шт'),
('0000036', 'Кабель HDMI 2.1 4K 120 Гц 2 м', 1200.00, 'шт'),
('0000037', 'Коврик для мыши SteelSeries QcK xxl', 2500.00, 'шт'),
('0000038', 'Веб-камера Logitech Brio 4K', 11000.00, 'шт')
ON CONFLICT (code) DO NOTHING;