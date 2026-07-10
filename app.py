from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import os 
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

database_url = os.getenv('DATABASE_URL')
if not database_url:
    if os.environ.get('VERCEL'):
        database_url = 'sqlite:////tmp/ai_stylist.db'
    else:
        database_url = 'sqlite:///ai_stylist.db'

if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


class CollectionItem(db.Model):
    __tablename__ = 'collection_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    material = db.Column(db.String(255), nullable=False)
    story = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.Text, nullable=False)

# --- 1. CORE AI SIMULATION: BODY SHAPE DETECTION (FORCED HOURGLASS) ---
def simulate_body_shape_detection(image_path):
    """
    *** TEMPORARY FIX: FORCES the detected shape to 'Hourglass' ***
    """
    return 'Hourglass' 

    # ORIGINAL LOGIC (Uncomment this later):
    # file_size = os.path.getsize(image_path)
    # body_shapes = ['Hourglass', 'Rectangle', 'Pear', 'Apple']
    # shape_index = file_size % len(body_shapes)
    # return body_shapes[shape_index]

# --- 2. RECOMMENDATION DATABASE (LIST OF OUTFITS) ---

RECOMMENDATIONS = {
    
    # --- HOURGLASS SHAPE OUTFITS (FORMAL WEDDING) ---
    ('Hourglass', 'Formal Wedding'): [ 
        {
            'name': 'A long, smooth gown that enhances balance and shape with subtle sophistication',
            'tip': 'Ideal for highlighting your balanced silhouette.',
            'sustainable_material': 'Recycled Polyester or Tencel Luxe',
            'vto_url': 'https://vto.example.com/hg_wedding_1',
            'overlay_img_url': 'overlays/hg_wedding_1.png', 
        },
        {
            'name': 'Luxurious velvet with a soft A-line shape for winter or evening weddings.',
            'tip': 'A velvet A-line flows beautifully off your waist and is perfect for a formal evening or winter wedding.',
            'sustainable_material': 'Organic Velvet or Peace Silk',
            'vto_url': 'https://vto.example.com/hg_wedding_2',
            'overlay_img_url': 'overlays/hg_wedding_2.png',
        },
        {
            'name': 'A polished satin wrap creating graceful curves and shine',
            'tip': 'The wrap feature emphasizes your narrow waist, while long sleeves add elegance. Look for a deep emerald or sapphire tone.',
            'sustainable_material': 'Recycled Satin or Ecovero Viscose',
            'vto_url': 'https://vto.example.com/hg_wedding_3',
            'overlay_img_url': 'overlays/hg_wedding_3.png',
        },
        {
            'name': 'A modern and bold fitted jumpsuit with clean waist definition',
            'tip': 'A bold, modern choice! The defined tailoring around the waist and shoulders maintains your balanced silhouette.',
            'sustainable_material': 'Recycled Wool Blend',
            'vto_url': 'https://vto.example.com/hg_wedding_4',
            'overlay_img_url': 'overlays/hg_wedding_4.png',
        },
        {
            'name': 'A flowing chiffon dress offering romantic movement and elegance',
            'tip': 'Perfect for spring/summer formal events. Choose a solid color with a thick belt or sash to define the middle.',
            'sustainable_material': 'Organic Cotton Chiffon',
            'vto_url': 'https://vto.example.com/hg_wedding_5',
            'overlay_img_url': 'overlays/hg_wedding_5.png',
        },
         {
             'name': 'A detailed gown suited for grand events.',
            'tip': 'Embellishments draw the eye upward for balanced curves ',
            'sustainable_material': 'Eco-sequins / recycled mesh.',
            'vto_url': 'https://vto.example.com/hg_wedding_6',
            'overlay_img_url': 'overlays/hg_wedding_6.png',
         },
          {
            'name': 'A princess-style off-shoulder dress.',
            'tip': 'Off-shoulder frames the neckline beautifully for weddings.',
            'sustainable_material': 'Peace silk.',
            'vto_url': 'https://vto.example.com/hg_wedding_7',
            'overlay_img_url': 'overlays/hg_wedding_7.png',
        },
        {
            'name': 'A soft gown with pearl accents',
            'tip': 'Pearls add understated luxury without overpowering shape',
            'sustainable_material': 'Organic satin ',
            'vto_url': 'https://vto.example.com/hg_wedding_8',
            'overlay_img_url': 'overlays/hg_wedding_8.png',
        },
        


    ],
    
    # --- HOURGLASS SHAPE OUTFITS (COCKTAIL PARTY) ---
    ('Hourglass', 'Cocktail Party Classic'): [ 
        {
            'name': 'Black Spaghetti-Strap Quilted Midi',
            'tip': 'The fitted bodice and full midi skirt naturally complement your waist-to-hip curve. A timeless look.',
            'sustainable_material': 'Recycled Polyester Blend',
            'vto_url': 'https://vto.example.com/hg_cocktail_1',
            'overlay_img_url': 'overlays/hg_cocktail_1.png', 
        },
        {
            'name': 'One-Shoulder Pleated Olive Gown',
            'tip': 'The defined waistline and structured bodice are ideal. The flowing pleated skirt adds elegant movement.',
            'sustainable_material': 'Ecovero Viscose or Peace Silk',
            'vto_url': 'https://vto.example.com/hg_cocktail_2',
            'overlay_img_url': 'overlays/hg_cocktail_2.png',
        },
        {
            'name': 'Retro Black Cap-Sleeve A-Line Dress',
            'tip': 'The wide sweetheart neckline highlights the chest, and the cinched waist and full skirt are perfect hourglass proportions.',
            'sustainable_material': 'Organic Cotton Poplin',
            'vto_url': 'https://vto.example.com/hg_cocktail_3',
            'overlay_img_url': 'overlays/hg_cocktail_3.png',
        },
        {
            'name': 'Red Ruffled Strapless Mermaid Gown',
            'tip': 'A true hourglass statement! The mermaid silhouette perfectly mirrors your figure. Use this for a very formal cocktail event.',
            'sustainable_material': 'Recycled Satin',
            'vto_url': 'https://vto.example.com/hg_cocktail_4',
            'overlay_img_url': 'overlays/hg_cocktail_4.png',
        },
        {
            'name': 'Red Floral Tiered Ruffle Dress',
            'tip': 'A fun, vibrant option for a spring or summer cocktail event. The ruffles add beautiful texture without adding bulk.',
            'sustainable_material': 'Tencel or Organic Silk Crepe',
            'vto_url': 'https://vto.example.com/hg_cocktail_5',
            'overlay_img_url': 'overlays/hg_cocktail_5.png',
        },
    ],

    # --- HOURGLASS SHAPE OUTFITS (CASUAL BRUNCH - NOW 8 OUTFITS) ---
    ('Hourglass', 'Casual Brunch'): [ 
        {
            'name': 'A casual, curve-friendly brunch look with a waist-tie detail.',
            'tip': 'High-waisted white skirt elongates your legs and enhances your natural waist.',
            'sustainable_material': 'Repurposed Cotton / Organic Linen',
            'vto_url': 'https://vto.example.com/hg_brunch_1',
            'overlay_img_url': 'overlays/hg_brunch_1.png', 
        },
        {
            'name': 'A cozy wrap top that flatters your waistline effortlessly with classy denim accents.',
            'tip': 'A soft, casual wrap top is ideal. The adjustable waist means a perfect fit every time!',
            'sustainable_material': 'Recycled Cashmere Blend',
            'vto_url': 'https://vto.example.com/hg_brunch_2',
            'overlay_img_url': 'overlays/hg_brunch_2.png',
        },
        {
            'name': 'Airy culottes paired with a slim top for a balanced silhouette & Fitted Crew Neck Tee',
            'tip': 'Culottes create volume on the bottom, so pair them with a fitted top to maintain balance.',
            'sustainable_material': 'Tencel or Ecovero Viscose',
            'vto_url': 'https://vto.example.com/hg_brunch_3',
            'overlay_img_url': 'overlays/hg_brunch_3.png',
        },
        {
            'name': 'Button-Up Denim Skirt & Ribbed cute Tank Top ',
            'tip': 'A skirt that buttons up the front draws the eye vertically and cinches at your natural waist.',
            'sustainable_material': 'Organic Cotton Denim',
            'vto_url': 'https://vto.example.com/hg_brunch_4',
            'overlay_img_url': 'overlays/hg_brunch_4.png',
        },
        {
            'name': 'High-Waisted Cropped White Jeans & Tie-Front Top',
            'tip': 'Look for adjustable belts for the perfect hourglass contour',
            'sustainable_material': 'Hemp or Linen Blend',
            'vto_url': 'https://vto.example.com/hg_brunch_5',
            'overlay_img_url': 'overlays/hg_brunch_5.png',
        },
        # --- CRITICAL: PASTE YOUR OUTFIT 6 DETAILS HERE ---
        {
            'name': 'A breezy floral white midi dress with red shrug perfect for warm day',
            'tip': 'A light A-line skirt keeps the look soft and feminine.',
            'sustainable_material': 'Organic cotton voile.',
            'vto_url': 'https://vto.example.com/hg_brunch_6',
            'overlay_img_url': 'overlays/hg_brunch_6.png', 
        },
        # --- CRITICAL: PASTE YOUR OUTFIT 7 DETAILS HERE ---
        {
            'name': 'A white ruffled top paired with structured pants.',
            'tip': 'Ruffles add balance to the upper body without overwhelming shape',
            'sustainable_material': 'Organic cotton voile',
            'vto_url': 'https://vto.example.com/hg_brunch_7',
            'overlay_img_url': 'overlays/hg_brunch_7.png',
        },
        # --- CRITICAL: PASTE YOUR OUTFIT 8 DETAILS HERE ---
        {
            'name': 'A gathered-waist dress for effortless brunch elegance.',
            'tip': 'Cinching at the smallest part of your waist enhances proportions',
            'sustainable_material': 'Organic poplin',
            'vto_url': 'https://vto.example.com/hg_brunch_8',
            'overlay_img_url': 'overlays/hg_brunch_8.png',
        },
    ],

    # --- HOURGLASS SHAPE OUTFITS (OFFICE/PROFESSIONAL MEETING) ---
    ('Hourglass', 'Office/Professional Meeting'): [

        {
        'name': 'A clean professional look with a blue blazer and trouser.',
        'tip': 'Tucking in the blouse defines the waistline better.',
        'sustainable_material': 'Recycled wool',
        'vto_url': 'https://vto.example.com/hg_office_1',
        'overlay_img_url': 'overlays/hg_office_1.png',
    },
    {
        'name': 'A polished wrap dress ideal for meetings.',
        'tip': 'Structural shoulders add confidence and authority.',
        'sustainable_material': 'Tencel blend',
        'vto_url': 'https://vto.example.com/hg_office_2',
        'overlay_img_url': 'overlays/hg_office_2.png',
    },
    {
        'name': 'A luxurious corporate combination.',
        'tip': 'Wide-leg trousers elongate the frame when paired with heels.',
        'sustainable_material': 'Organic silk',
        'vto_url': 'https://vto.example.com/hg_office_3',
        'overlay_img_url': 'overlays/hg_office_3.png',
    },
    {
        'name': 'A classic brown top with tailored trousers.',
        'tip': 'A single-button blazer gives the best waist definition.',
        'sustainable_material': 'Recycled suit fabric',
        'vto_url': 'https://vto.example.com/hg_office_4',
        'overlay_img_url': 'overlays/hg_office_4.png',
    },
    {
        'name': 'A simple and elegant professional dress.',
        'tip': 'Always add a thin belt for refined contouring.',
        'sustainable_material': 'Organic cotton',
        'vto_url': 'https://vto.example.com/hg_office_5',
        'overlay_img_url': 'overlays/hg_office_5.png',
    },
    {
        'name': 'A clean minimal office combination.',
        'tip': 'Neutral colors keep the look sharp and modern.',
        'sustainable_material': 'Fair-trade cotton',
        'vto_url': 'https://vto.example.com/hg_office_6',
        'overlay_img_url': 'overlays/hg_office_6.png',
    },
    {
        'name': 'A bold contemporary take on formalwear.',
        'tip': 'Great choice when you want strong structure without layering.',
        'sustainable_material': 'Sustainable polyester blend',
        'vto_url': 'https://vto.example.com/hg_office_7',
        'overlay_img_url': 'overlays/hg_office_7.png',
    },
    {
        'name': 'A polished blue trouser with a tucked shirt.',
        'tip': 'Pleats create graceful movement without adding volume.',
        'sustainable_material': 'Eco viscose',
        'vto_url': 'https://vto.example.com/hg_office_8',
        'overlay_img_url': 'overlays/hg_office_8.png',
    },
     ],

    # --- HOURGLASS SHAPE OUTFITS (MUSIC FESTIVAL/CONCERT) ---
    ('Hourglass', 'Music Festival/Concert'): [ 
        {
            'name': 'High-Waisted Denim Shorts & Fitted Bodysuit',
            'tip': 'The bodysuit tucks cleanly into the high waist, emphasizing your midsection while keeping you comfortable for movement.',
            'sustainable_material': 'Repurposed Denim / Organic Cotton',
            'vto_url': 'https://vto.example.com/hg_concert_1',
            'overlay_img_url': 'overlays/hg_concert_1.png', 
        },
        {
            'name': 'Mini Dress with Defined Waist (A-line Skirt)',
            'tip': 'A lightweight mini dress with a definite waistline (like a smocked band) is easy to move in and looks fantastic.',
            'sustainable_material': 'Organic Linen or Hemp',
            'vto_url': 'https://vto.example.com/hg_concert_2',
            'overlay_img_url': 'overlays/hg_concert_2.png',
        },
        {
            'name': 'Flared Jeans & Cropped Tee',
            'tip': 'Flared jeans balance your curves beautifully. Pair with a cropped top that hits right at the waistline.',
            'sustainable_material': 'Tencel Denim',
            'vto_url': 'https://vto.example.com/hg_concert_3',
            'overlay_img_url': 'overlays/hg_concert_3.png',
        },
        {
            'name': 'Bohemian Jumpsuit with Waist Drawstring',
            'tip': 'Comfortable and flowy, but the drawstring is non-negotiable—it ensures your shape doesn’t get lost!',
            'sustainable_material': 'Recycled Cotton or Bamboo',
            'vto_url': 'https://vto.example.com/hg_concert_4',
            'overlay_img_url': 'overlays/hg_concert_4.png',
        },
        {
            'name': 'High-Waisted Skort & Graphic Band Tee',
            'tip': 'A skort gives you the look of a skirt with the freedom of shorts, perfect for dancing. Knot the tee at the waist.',
            'sustainable_material': 'Recycled Nylon Skort / Fair Trade Cotton Tee',
            'vto_url': 'https://vto.example.com/hg_concert_5.png',
            'overlay_img_url': 'overlays/hg_concert_5.png',
        },
    ],

    # --- RECTANGLE SHAPE OUTFITS (COCKTAIL PARTY - PARTIAL) ---
    ('Hourglass', 'Cocktail Party'): [
        {
            'name': 'A curve-enhancing mermaid gown for bold nights',
            'tip': 'The peplum adds curve and volume to your hip area, while the structured top creates a fuller bust line.',
            'sustainable_material': 'Recycled Wool Blend or Brocade',
            'vto_url': 'https://vto.example.com/hg_cocktail_1',
            'overlay_img_url': 'overlays/hg_cocktail_1.png', 
        },
        {

            'name': 'A dramatic single-shoulder pleated gown.',
            'tip': 'Asymmetric cuts highlight the shoulders beautifully.',
            'sustainable_material': 'Ecovero viscose.',
            'vto_url': 'https://vto.example.com/hg_cocktail_2',
            'overlay_img_url': 'overlays/hg_cocktail_6.png', 
        },
         {

            'name': 'A flirty tiered dress ideal for semi-formal evenings.',
            'tip': 'Tiering creates movement and adds soft feminine detail.',
            'sustainable_material': 'Tencel crepe.',
            'vto_url': 'https://vto.example.com/hg_cocktail_3',
            'overlay_img_url': 'overlays/hg_cocktail_3.png', 
        },
         {

            'name': 'A sleek satin slip with minimalistic charm.',
            'tip': 'Perfect with statement jewelry for elevated elegance.',
            'sustainable_material': 'Eco-friendly satin.',
            'vto_url': 'https://vto.example.com/hg_cocktail_4',
            'overlay_img_url': 'overlays/hg_cocktail_4.png', 
        },
         {

            'name': 'A fitted black quilted dress for a chic, timeless look.',
            'tip': 'Dark colors slim the torso while textured fabric adds interest.',
            'sustainable_material': 'Recycled polyester.',
            'vto_url': 'https://vto.example.com/hg_cocktail_5',
                'overlay_img_url': 'overlays/hg_cocktail_7.png', 
        },
         {

            'name': 'A glowing Blue pleated dress with light-catching shine.',
            'tip': 'Dark colors slim the torso while textured fabric adds interest.',
            'sustainable_material': 'Recycled polyester.',
            'vto_url': 'https://vto.example.com/hg_cocktail_6',
            'overlay_img_url': 'overlays/hg_cocktail_6.png', 
        },
        {

            'name': 'A confident off-shoulder bodycon dress.',
            'tip': 'Off-shoulder designs highlight collarbones and neckline.',
            'sustainable_material': 'Organic stretch jersey.',
            'vto_url': 'https://vto.example.com/hg_cocktail_7',
            'overlay_img_url': 'overlays/hg_cocktail_7.png', 
        },
        {

            'name': 'A vintage-inspired A-line dress with a defined waist.',
            'tip': 'A-line shapes balance curves without adding bulk..',
            'sustainable_material': 'Organic cotton satin.',
            'vto_url': 'https://vto.example.com/hg_cocktail_8',
            'overlay_img_url': 'overlays/hg_cocktail_8.png', 
        },
    ],
    
    # --- DEFAULT FALLBACK (CRITICAL FOR PREVENTING CRASHES) ---

}

# --- 3. COLOR PALETTE DATABASE ---
SEASONAL_PALETTES = {
    'Hourglass': {'season': 'Spring', 'colors': ['#F7B8A1', '#85C1E9', '#F9E79F', '#FDFEFE'], 'description': 'Warm and bright. These colors enhance your vibrant appearance.'},
    'Rectangle': {'season': 'Summer', 'colors': ['#AED6F1', '#D2B4DE', '#A3E4D7', '#FADBD8'], 'description': 'Cool and muted pastels. These soft colors create a graceful, blended look.'},
    'Default': {'season': 'Neutral', 'colors': ['#5D6D7E', '#AAB7B8', '#D6DBDF', '#FFFFFF'], 'description': 'Classic neutrals that work for any skin tone.'}
}


# --- VTO Image Merging Function (REVISED for error fix) ---
def apply_virtual_try_on(user_img_path, overlay_filename):
    """Merges the outfit overlay onto the user's uploaded image."""
    
    # 1. Define a unique output filename
    outfit_name_part = overlay_filename.split('/')[-1].split('.')[0]
    user_file_part = os.path.basename(user_img_path)
    vto_filename = f"vto_{outfit_name_part}_{user_file_part}"
    vto_filepath = os.path.join(app.config['UPLOAD_FOLDER'], vto_filename)

    try:
        user_img = Image.open(user_img_path).convert("RGBA")
        overlay_path = os.path.join(app.root_path, 'static', overlay_filename)
        outfit_overlay = Image.open(overlay_path).convert("RGBA")
        
        # Resize the outfit to match the user's uploaded photo size
        outfit_overlay = outfit_overlay.resize(user_img.size)
        
        # Perform the merge
        final_vto_img = Image.alpha_composite(user_img, outfit_overlay)
        
        # Save the merged image
        final_vto_img.convert("RGB").save(vto_filepath, 'JPEG')
        
        # Return the public URL
        return url_for('static', filename=f"uploads/{vto_filename}")
        
    except Exception as e:
        # 2. ERROR HANDLING: If the merge fails (corrupt or missing overlay/user file)
        print(f"ERROR: VTO merge failed for {overlay_filename}. Error: {e}")
        
        # Create a simple, gray placeholder image to prevent a total crash
        try:
            # Use the user image as a base size
            user_img = Image.open(user_img_path).convert("RGB")
            # Create a semi-transparent gray layer the same size
            placeholder = Image.new('RGB', user_img.size, color=(200, 200, 200))
            
            placeholder.save(vto_filepath, 'JPEG')
            print(f"Saved a gray placeholder to {vto_filepath}")
            return url_for('static', filename=f"uploads/{vto_filename}")
            
        except Exception as inner_e:
             # If even creating the placeholder fails, just return a dummy path
             print(f"CRITICAL ERROR: Failed to create placeholder. Inner Error: {inner_e}")
             return url_for('static', filename="overlays/default_overlay.png")


# --- 4. FLASK ROUTES ---
@app.route('/', methods=['GET'])
def index():
    events = [
        "Formal Wedding", "Cocktail Party", "Casual Brunch", 
        "Office/Professional Meeting", "Music Festival/Concert"
    ]
    return render_template('login.html', events=events)


@app.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():
    events = [
        "Formal Wedding", "Cocktail Party", "Casual Brunch", 
        "Office/Professional Meeting", "Music Festival/Concert"
    ]
    return render_template("upload_photo.html", events=events)



    # Renders the aesthetic login page
    events = [
        "Formal Wedding", "Cocktail Party", "Casual Brunch", 
        "Office/Professional Meeting", "Music Festival/Concert"
    ]
    return render_template('login.html', events=events)

@app.route('/recommend', methods=['POST'])
def recommend():
    
    if 'user_photo' not in request.files or 'event_type' not in request.form:
        return "Form Submission Error: Missing photo or event fields.", 400

    file = request.files['user_photo']
    event_type = request.form['event_type']
    
    # Capture the user details from the login form
    user_name = request.form.get('user_name', 'Client')
    user_email = request.form.get('user_email', 'N/A')

    if file.filename == '':
        return redirect(url_for('index'))
    
    # 2. Save the uploaded file
    if file:
        filename = f"{random.randint(1000, 9999)}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            img = Image.open(file.stream)
            img.save(filepath)
        except Exception as e:
            print(f"File error during save: {e}")
            return "Error: Please upload a valid image file.", 400

        # 3. Run the AI Simulation (Always returns 'Hourglass' for now)
        detected_shape = simulate_body_shape_detection(filepath)
        
        # 4. Get the recommendations
        key = (detected_shape, event_type)
        recommendations_list = RECOMMENDATIONS.get(key, RECOMMENDATIONS.get(('Default', 'Default')))
        
        color_palette = SEASONAL_PALETTES.get(detected_shape, SEASONAL_PALETTES['Default'])
        
        # 5. GENERATE THE FINAL VTO IMAGE FOR EVERY OUTFIT IN THE LIST
        final_vto_options = []
        for outfit in recommendations_list:
            vto_output_url = apply_virtual_try_on(filepath, outfit['overlay_img_url'])
            vto_option = outfit.copy()
            vto_option['final_vto_url'] = vto_output_url 
            
            # Generate a consistent price for this outfit name
            random.seed(outfit['name'])
            price_value = random.randint(7499, 22999)
            vto_option['price'] = f"INR {price_value:,}"
            
            final_vto_options.append(vto_option)

        # 6. Render the results (index.html is the results page)
        events = [
            "Formal Wedding", "Cocktail Party", "Casual Brunch", 
            "Office/Professional Meeting", "Music Festival/Concert"
        ]
        
        return render_template('index.html', 
                               events=events,
                               vto_options=final_vto_options, 
                               detected_shape=detected_shape,
                               selected_event=event_type,
                               color_palette=color_palette,
                               user_name=user_name,
                               user_email=user_email)

@app.route('/product')
def product_details():
    name = request.args.get('name', 'Elegant Outfit')
    tip = request.args.get('tip', '')
    material = request.args.get('material', 'Sustainable Fabric')
    img_url = request.args.get('img_url', '')
    
    # Generate dynamic price and beautiful description
    random.seed(name) # Consistent price for the same product name
    price_value = random.randint(7499, 22999)
    price = f"INR {price_value:,}"
    
    description = (f"Elevate your wardrobe with this exquisite piece. "
                   f"Thoughtfully designed to offer a flawless fit, this {name.lower()} "
                   f"combines modern aesthetics with timeless elegance. Crafted using premium {material}, "
                   f"it ensures both comfort and sustainability. Perfect for making a lasting impression.")
                   
    return render_template('product.html', name=name, tip=tip, material=material, img_url=img_url, price=price, description=description)

@app.route('/collection')
def collection():
    try:
        db_items = CollectionItem.query.order_by(CollectionItem.id.asc()).all()
        if db_items:
            collection_items = [
                {
                    'id': item.id,
                    'name': item.name,
                    'price': item.price,
                    'material': item.material,
                    'story': item.story,
                    'img_url': item.img_url,
                }
                for item in db_items
            ]
            return render_template('collection.html', items=collection_items)
    except Exception as error:
        print(f"Collection database lookup failed, using fallback data: {error}")

    collection_items = [
        {
            'id': 1,
            'name': 'The Solar Flare Gown',
            'price': 'INR 18,999',
            'material': 'Liquid Silk & Gold Thread',
            'story': 'Inspired by the celestial dance of the sun, this gown captures the essence of the golden hour. Every thread is woven with the promise of a new dawn, designed for the woman who shines from within.',
            'img_url': 'https://images.unsplash.com/photo-1539008835657-9e8e9680c956?auto=format&fit=crop&q=80&w=800'
        },
        {
            'id': 2,
            'name': 'Midnight Nebula Suit',
            'price': 'INR 24,499',
            'material': 'Stellar Velvet & Obsidian Satin',
            'story': 'A tribute to the infinite mystery of the cosmos. The Midnight Nebula Suit is more than attire; it is an aura. Crafted for those who find power in the shadows and light in the unknown.',
            'img_url': 'https://images.unsplash.com/photo-1594932224828-b4b059b6f6f9?auto=format&fit=crop&q=80&w=800'
        },
        {
            'id': 3,
            'name': 'Arctic Whisper Coat',
            'price': 'INR 15,799',
            'material': 'Glacier Wool & Recycled Cashmere',
            'story': 'Born from the hushed beauty of a winter morning. This coat offers the warmth of a fire on a frozen night, blending structural elegance with the soft touch of falling snow.',
            'img_url': 'https://images.unsplash.com/photo-1539533018447-63fcce2678e3?auto=format&fit=crop&q=80&w=800'
        },
        {
            'id': 4,
            'name': 'Emerald Eden Wrap',
            'price': 'INR 12,299',
            'material': 'Organic Bamboo Silk',
            'story': 'A love letter to the ancient forests. The Emerald Eden Wrap drapes you in the vibrant life of a tropical canopy, ensuring every step you take is in harmony with nature.',
            'img_url': 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&q=80&w=800'
        },
        {
            'id': 5,
            'name': 'Sapphire Serenity Kaftan',
            'price': 'INR 14,499',
            'material': 'Lustrous Silk Georgette',
            'story': 'A piece that mirrors the depths of the ocean. This kaftan is designed for moments of absolute peace, where elegance meets effortless grace.',
            'img_url': 'https://images.unsplash.com/photo-1490481651871-ab68625d5e21?auto=format&fit=crop&q=80&w=800'
        },
        {
            'id': 6,
            'name': 'Ivory Illusion Blouse',
            'price': 'INR 9,899',
            'material': 'Sheer Crepe de Chine',
            'story': 'A delicate play of light and shadow. The Ivory Illusion Blouse brings a touch of ethereal beauty to the modern wardrobe, perfect for transitions from day to night.',
            'img_url': 'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?auto=format&fit=crop&q=80&w=800'
        },
        {
            'id': 7,
            'name': 'Crimson Cascade Gown',
            'price': 'INR 21,999',
            'material': 'Vibrant Ruby Chiffon',
            'story': 'Bold, passionate, and unforgettable. The Crimson Cascade Gown is a statement of strength and beauty, flowing like a river of fire with every move.',
            'img_url': 'https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&q=80&w=800'
        },
        {
            'id': 8,
            'name': 'Onyx Power Blazer',
            'price': 'INR 17,299',
            'material': 'Structured Virgin Wool',
            'story': 'Precision meeting power. This blazer is the armor for the modern visionary, offering sharp lines and an impeccable silhouette that commands respect.',
            'img_url': 'https://images.unsplash.com/photo-1534030347209-467a5b0ad3e6?auto=format&fit=crop&q=80&w=800'
        },
        {
            'id': 9,
            'name': 'Rose Quartz Jumpsuit',
            'price': 'INR 13,899',
            'material': 'Blush Satin Twill',
            'story': 'Softness defined in a structured form. The Rose Quartz Jumpsuit captures the gentle strength of a morning sky, blending playful charm with sophisticated grace.',
            'img_url': 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?auto=format&fit=crop&q=80&w=800'
        }
    ]
    return render_template('collection.html', items=collection_items)

if __name__ == '__main__':
    app.run(debug=True)