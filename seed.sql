CREATE TABLE IF NOT EXISTS collection_items (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price VARCHAR(50) NOT NULL,
    material VARCHAR(255) NOT NULL,
    story TEXT NOT NULL,
    img_url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cart_items (
    id BIGSERIAL PRIMARY KEY,
    session_id VARCHAR(255),
    product_name VARCHAR(255) NOT NULL,
    price VARCHAR(50) NOT NULL,
    img_url TEXT,
    quantity INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO collection_items (id, name, price, material, story, img_url) VALUES
(1, 'The Solar Flare Gown', 'INR 18,999', 'Liquid Silk & Gold Thread', 'Inspired by the celestial dance of the sun, this gown captures the essence of the golden hour. Every thread is woven with the promise of a new dawn, designed for the woman who shines from within.', 'https://images.unsplash.com/photo-1539008835657-9e8e9680c956?auto=format&fit=crop&q=80&w=800'),
(2, 'Midnight Nebula Suit', 'INR 24,499', 'Stellar Velvet & Obsidian Satin', 'A tribute to the infinite mystery of the cosmos. The Midnight Nebula Suit is more than attire; it is an aura. Crafted for those who find power in the shadows and light in the unknown.', 'https://images.unsplash.com/photo-1594932224828-b4b059b6f6f9?auto=format&fit=crop&q=80&w=800'),
(3, 'Arctic Whisper Coat', 'INR 15,799', 'Glacier Wool & Recycled Cashmere', 'Born from the hushed beauty of a winter morning. This coat offers the warmth of a fire on a frozen night, blending structural elegance with the soft touch of falling snow.', 'https://images.unsplash.com/photo-1539533018447-63fcce2678e3?auto=format&fit=crop&q=80&w=800'),
(4, 'Emerald Eden Wrap', 'INR 12,299', 'Organic Bamboo Silk', 'A love letter to the ancient forests. The Emerald Eden Wrap drapes you in the vibrant life of a tropical canopy, ensuring every step you take is in harmony with nature.', 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&q=80&w=800'),
(5, 'Sapphire Serenity Kaftan', 'INR 14,499', 'Lustrous Silk Georgette', 'A piece that mirrors the depths of the ocean. This kaftan is designed for moments of absolute peace, where elegance meets effortless grace.', 'https://images.unsplash.com/photo-1490481651871-ab68625d5e21?auto=format&fit=crop&q=80&w=800'),
(6, 'Ivory Illusion Blouse', 'INR 9,899', 'Sheer Crepe de Chine', 'A delicate play of light and shadow. The Ivory Illusion Blouse brings a touch of ethereal beauty to the modern wardrobe, perfect for transitions from day to night.', 'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?auto=format&fit=crop&q=80&w=800'),
(7, 'Crimson Cascade Gown', 'INR 21,999', 'Vibrant Ruby Chiffon', 'Bold, passionate, and unforgettable. The Crimson Cascade Gown is a statement of strength and beauty, flowing like a river of fire with every move.', 'https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&q=80&w=800'),
(8, 'Onyx Power Blazer', 'INR 17,299', 'Structured Virgin Wool', 'Precision meeting power. This blazer is the armor for the modern visionary, offering sharp lines and an impeccable silhouette that commands respect.', 'https://images.unsplash.com/photo-1534030347209-467a5b0ad3e6?auto=format&fit=crop&q=80&w=800'),
(9, 'Rose Quartz Jumpsuit', 'INR 13,899', 'Blush Satin Twill', 'Softness defined in a structured form. The Rose Quartz Jumpsuit captures the gentle strength of a morning sky, blending playful charm with sophisticated grace.', 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?auto=format&fit=crop&q=80&w=800')
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    price = EXCLUDED.price,
    material = EXCLUDED.material,
    story = EXCLUDED.story,
    img_url = EXCLUDED.img_url;